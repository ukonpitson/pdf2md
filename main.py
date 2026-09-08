import os
import config
from converter import PDFToMarkdownConverter

def main():
    # Đặt tên tệp PDF đầu vào cần chuyển đổi (nằm trong thư mục input)
    input_pdf_name = "pdf_scan.pdf"  # Thay tên file PDF của bạn vào đây
    input_pdf = os.path.join(config.DEFAULT_INPUT_DIR, input_pdf_name)
    
    if not os.path.exists(input_pdf):
        print(f"[LỖI]: Không tìm thấy tệp PDF đầu vào!")
        print(f"Vui lòng copy tệp PDF vào thư mục: {input_pdf}")
        return

    converter = PDFToMarkdownConverter(
        pdf_path=input_pdf,
        output_dir=config.DEFAULT_OUTPUT_DIR
    )
    
    converter.convert(output_md_filename="result.md")

if __name__ == "__main__":
    main()