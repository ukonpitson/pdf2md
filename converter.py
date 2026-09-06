import fitz  # PyMuPDF
import re
import os
import cv2
import asyncio
import numpy as np
from PIL import Image
from pdf2image import convert_from_path
import winocr

import config

class PDFToMarkdownConverter:
    def __init__(self, pdf_path, output_dir=None):
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
        self.output_dir = output_dir if output_dir else config.DEFAULT_OUTPUT_DIR
        self.images_dir = os.path.join(self.output_dir, "images")
        
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)
        
        self.footnotes = []
        self.markdown_lines = []

    def _run_winocr(self, pil_image):
        """Hàm bọc gọi winocr (bất đồng bộ) xử lý ảnh PIL với ngôn ngữ Tiếng Việt"""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        result = loop.run_until_complete(
            winocr.recognize_pil(pil_image, lang=config.WIN_OCR_LANG)
        )
        return result.get("text", "")

    def classify_page(self, page):
        """Phân loại trang: Native Text hay Scan OCR"""
        text = page.get_text()
        return len(text.strip()) >= config.CLASSIFY_CHAR_THRESHOLD

    def parse_regex_structure(self, line):
        """Nhận diện cấu trúc Heading & List qua Regex"""
        line_clean = line.strip()
        if not line_clean:
            return ""
        
        if config.REGEX_PATTERNS["H1"].match(line_clean):
            return f"# {line_clean}"
        elif config.REGEX_PATTERNS["H2"].match(line_clean):
            return f"## {line_clean}"
        elif config.REGEX_PATTERNS["H3"].match(line_clean):
            return f"### {line_clean}"
        elif config.REGEX_PATTERNS["LIST_BULLET"].match(line_clean):
            cleaned_bullet = config.REGEX_PATTERNS["LIST_BULLET"].sub('', line_clean)
            return f"- {cleaned_bullet}"
        elif config.REGEX_PATTERNS["LIST_NUMBER"].match(line_clean):
            return line_clean
        else:
            return line_clean

    def _get_image_filename(self, page_num, img_num):
        return config.IMAGE_NAMING_PATTERN.format(page_num=page_num, img_num=img_num)

    # =========================================================================
    # NHÁNH A: NATIVE TEXT
    # =========================================================================
    def process_text_page(self, page, page_num):
        img_count = 1
        page_height = page.rect.height
        
        # 1. Cắt ảnh Vector/Raster
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = self.doc.extract_image(xref)
            image_filename = self._get_image_filename(page_num, img_count)
            image_path = os.path.join(self.images_dir, image_filename)
            
            with open(image_path, "wb") as f:
                f.write(base_image["image"])
                
            self.markdown_lines.append(f"\n![Hình ảnh tại trang {page_num}](./images/{image_filename})\n")
            img_count += 1
            
        # 2. Cắt Bảng
        tables = page.find_tables()
        if tables.tables:
            for table in tables.tables:
                pix = page.get_pixmap(clip=table.bbox, dpi=config.DPI)
                table_filename = self._get_image_filename(page_num, img_count)
                pix.save(os.path.join(self.images_dir, table_filename))
                
                self.markdown_lines.append(f"\n![Bảng tại trang {page_num}](./images/{table_filename})\n")
                img_count += 1

        # 3. Trích xuất Text & Gộp đoạn
        blocks = page.get_text("blocks")
        for b in blocks:
            x0, y0, x1, y1, text, block_no, block_type = b
            
            if y1 < config.HEADER_RATIO * page_height or y0 > (1 - config.FOOTER_RATIO) * page_height:
                continue
                
            if y0 > config.FOOTNOTE_START_RATIO * page_height and len(text.strip()) < 200:
                self.footnotes.append({"page": page_num, "text": text.strip()})
                fn_idx = len(self.footnotes)
                self.markdown_lines.append(f"[^fn_{fn_idx}]")
                continue

            raw_lines = [line.strip() for line in text.split('\n') if line.strip()]
            if not raw_lines:
                continue

            current_paragraph = []
            for line in raw_lines:
                is_heading_or_list = any([
                    config.REGEX_PATTERNS["H1"].match(line),
                    config.REGEX_PATTERNS["H2"].match(line),
                    config.REGEX_PATTERNS["H3"].match(line),
                    config.REGEX_PATTERNS["LIST_BULLET"].match(line),
                    config.REGEX_PATTERNS["LIST_NUMBER"].match(line)
                ])

                if is_heading_or_list:
                    if current_paragraph:
                        self.markdown_lines.append(" ".join(current_paragraph))
                        current_paragraph = []
                    self.markdown_lines.append(self.parse_regex_structure(line))
                else:
                    current_paragraph.append(line)

            if current_paragraph:
                self.markdown_lines.append(" ".join(current_paragraph))

    # =========================================================================
    # NHÁNH B: SCANNED IMAGE (DÙNG WINOCR THUẦN TIẾNG VIỆT)
    # =========================================================================
    def process_scanned_page(self, page_num):
        # 1. Chuyển PDF sang Ảnh có kèm poppler_path
        images = convert_from_path(
            self.pdf_path, 
            first_page=page_num, 
            last_page=page_num, 
            dpi=config.DPI,
            poppler_path=config.POPPLER_PATH
        )
        
        open_cv_image = np.array(images[0])
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2GRAY)
        h, w = gray.shape

        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
        # 2. Cắt Bảng/Ảnh
        img_count = 1
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for cnt in contours:
            x, y, box_w, box_h = cv2.boundingRect(cnt)
            if (box_w > w * 0.3 and box_h > h * 0.1) and not (box_w > w * 0.9 and box_h > h * 0.9):
                crop_img = open_cv_image[y:y+box_h, x:x+box_w]
                img_filename = self._get_image_filename(page_num, img_count)
                cv2.imwrite(os.path.join(self.images_dir, img_filename), cv2.cvtColor(crop_img, cv2.COLOR_RGB2BGR))
                
                self.markdown_lines.append(f"\n![Nội dung trích xuất tại trang {page_num}](./images/{img_filename})\n")
                img_count += 1
                cv2.rectangle(thresh, (x, y), (x + box_w, y + box_h), (255, 255, 255), -1)

        # 3. Masking Header / Footer
        thresh[0:int(h * config.HEADER_RATIO), :] = 255
        thresh[int(h * (1 - config.FOOTER_RATIO)):h, :] = 255

        # 4. Trích Footnote qua WinOCR
        fn_start_y = int(h * config.FOOTNOTE_START_RATIO)
        fn_end_y = int(h * (1 - config.FOOTER_RATIO))
        footnote_crop = thresh[fn_start_y:fn_end_y, :]
        fn_pil = Image.fromarray(footnote_crop)
        
        fn_text = self._run_winocr(fn_pil).strip()
        if fn_text and len(fn_text) < 200:
            self.footnotes.append({"page": page_num, "text": fn_text})
            fn_idx = len(self.footnotes)
            self.markdown_lines.append(f"[^fn_{fn_idx}]")
            thresh[fn_start_y:fn_end_y, :] = 255

        # 5. Đọc chữ toàn bộ trang bằng WinOCR (Mặc định vi-VN)
        full_pil = Image.fromarray(thresh)
        ocr_text = self._run_winocr(full_pil)
        
        for line in ocr_text.split('\n'):
            formatted = self.parse_regex_structure(line)
            if formatted:
                self.markdown_lines.append(formatted)

    def convert(self, output_md_filename="result.md"):
        output_md_path = os.path.join(self.output_dir, output_md_filename)
        
        for i, page in enumerate(self.doc):
            page_num = i + 1
            print(f"Đang xử lý Trang {page_num}/{len(self.doc)}...")
            
            if self.classify_page(page):
                print(f"  -> Nhánh A (Native Text)")
                self.process_text_page(page, page_num)
            else:
                print(f"  -> Nhánh B (Scanned Image - WinOCR Tiếng Việt)")
                self.process_scanned_page(page_num)
                
            self.markdown_lines.append("\n---\n")

        if self.footnotes:
            self.markdown_lines.append(config.FOOTNOTE_SECTION_HEADER)
            for idx, fn in enumerate(self.footnotes, 1):
                formatted_fn = config.FOOTNOTE_FMT.format(idx=idx, page=fn['page'], text=fn['text'])
                self.markdown_lines.append(formatted_fn)

        with open(output_md_path, "w", encoding="utf-8") as f:
            f.write("\n\n".join(self.markdown_lines))
            
        print(f"\n==========================================")
        print(f"HOÀN THÀNH! Tệp xuất tại: {output_md_path}")