import os
import config
from converter import PDFToMarkdownConverter

def main():
    # File PDF mẫu nằm trong thư mục input mặc định
    input_pdf = os.path.join(config.DEFAULT_INPUT_DIR, "pdf_scan.pdf")
    
    if not os.path.exists(input_pdf):
        print(f"Vui lòng chép file PDF cần chuyển đổi vào: {input_pdf}")
        return

    # Khởi tạo bộ chuyển đổi với cấu hình tự động
    converter = PDFToMarkdownConverter(
        pdf_path=input_pdf,
        output_dir=config.DEFAULT_OUTPUT_DIR
    )
    
    # Tiến hành chuyển đổi
    converter.convert(output_md_filename="result.md")

if __name__ == "__main__":
    main()