import fitz  # PyMuPDF
import re
import os
import cv2
import numpy as np
from PIL import Image
from pdf2image import convert_from_path
import easyocr

import config

class PDFToMarkdownConverter:
    def __init__(self, pdf_path, output_dir=None):
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
        self.output_dir = output_dir if output_dir else config.DEFAULT_OUTPUT_DIR
        self.images_dir = os.path.join(self.output_dir, "images")
        
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)
        
        print(f"Đang khởi tạo EasyOCR với ngôn ngữ: {config.OCR_LANGUAGES}...")
        self.reader = easyocr.Reader(config.OCR_LANGUAGES, gpu=False)
        
        self.footnotes = []
        self.markdown_lines = []

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
            
            # Loại bỏ Header/Footer
            if y1 < config.HEADER_RATIO * page_height or y0 > (1 - config.FOOTER_RATIO) * page_height:
                continue
                
            # Trích xuất Footnote
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
    # NHÁNH B: SCANNED IMAGE (EASYOCR TIẾNG VIỆT)
    # =========================================================================
    # =========================================================================
    # NHÁNH B: SCANNED IMAGE (EASYOCR TIẾNG VIỆT TỐI ƯU NÉT CHỮ)
    # =========================================================================
    # =========================================================================
    # NHÁNH B: SCANNED IMAGE (EASYOCR TIẾNG VIỆT TỐI ƯU NÉT CHỮ)
    # =========================================================================
    def process_scanned_page(self, page_num):
        # 1. Chuyển PDF sang Ảnh với DPI cao (300)
        images = convert_from_path(
            self.pdf_path, 
            first_page=page_num, 
            last_page=page_num, 
            dpi=config.DPI,
            poppler_path=config.POPPLER_PATH
        )
        
        orig_img = np.array(images[0])
        h_orig, w_orig = orig_img.shape[:2]

        # Phóng to ảnh 1.5 lần nếu ảnh gốc nhỏ để EasyOCR nhận diện dấu tiếng Việt tốt hơn
        if w_orig < 2000:
            scale_factor = 1.5
            orig_img = cv2.resize(orig_img, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
        
        gray = cv2.cvtColor(orig_img, cv2.COLOR_RGB2GRAY)
        h, w = gray.shape

        # Tăng cường độ tương phản (CLAHE) giúp chữ và dấu đậm nét hơn hẳn
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)

        # 2. Phát hiện & Cắt Bảng/Ảnh trên bản Threshold
        thresh = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 8)
        img_count = 1
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for cnt in contours:
            x, y, box_w, box_h = cv2.boundingRect(cnt)
            # Lọc bỏ khung hình ảnh/bảng biểu
            if (box_w > w * 0.35 and box_h > h * 0.12) and not (box_w > w * 0.9 and box_h > h * 0.9):
                crop_img = orig_img[y:y+box_h, x:x+box_w]
                img_filename = self._get_image_filename(page_num, img_count)
                cv2.imwrite(os.path.join(self.images_dir, img_filename), cv2.cvtColor(crop_img, cv2.COLOR_RGB2BGR))
                
                self.markdown_lines.append(f"\n![Nội dung trích xuất tại trang {page_num}](./images/{image_filename if 'image_filename' in locals() else img_filename})\n")
                img_count += 1
                
                # Xóa vùng ảnh đã cắt khỏi bản gray để không đọc OCR đè lên
                cv2.rectangle(enhanced, (x, y), (x + box_w, y + box_h), (255, 255, 255), -1)

        # 3. Masking Header / Footer (Xóa lề trên/dưới)
        enhanced[0:int(h * config.HEADER_RATIO), :] = 255
        enhanced[int(h * (1 - config.FOOTER_RATIO)):h, :] = 255

        # 4. Trích Footnote
        fn_start_y = int(h * config.FOOTNOTE_START_RATIO)
        fn_end_y = int(h * (1 - config.FOOTER_RATIO))
        footnote_crop = enhanced[fn_start_y:fn_end_y, :]
        
        fn_results = self.reader.readtext(footnote_crop, detail=0)
        fn_text = " ".join(fn_results).strip()
        
        if fn_text and len(fn_text) < 200:
            self.footnotes.append({"page": page_num, "text": fn_text})
            fn_idx = len(self.footnotes)
            self.markdown_lines.append(f"[^fn_{fn_idx}]")
            enhanced[fn_start_y:fn_end_y, :] = 255

        # 5. Đọc chữ trực tiếp từ ảnh Grayscale đã tăng tương phản (KHÔNG DÙNG THRESHOLD NỮA)
        ocr_results = self.reader.readtext(enhanced, detail=0)
        for line in ocr_results:
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
                print(f"  -> Nhánh B (Scanned Image - EasyOCR Tiếng Việt)")
                self.process_scanned_page(page_num)
                
            self.markdown_lines.append("\n---\n")

        # Gom Footnotes về cuối tài liệu
        if self.footnotes:
            self.markdown_lines.append(config.FOOTNOTE_SECTION_HEADER)
            for idx, fn in enumerate(self.footnotes, 1):
                formatted_fn = config.FOOTNOTE_FMT.format(idx=idx, page=fn['page'], text=fn['text'])
                self.markdown_lines.append(formatted_fn)

        with open(output_md_path, "w", encoding="utf-8") as f:
            f.write("\n\n".join(self.markdown_lines))
            
        print(f"\n==========================================")
        print(f"HOÀN THÀNH! Tệp xuất tại: {output_md_path}")