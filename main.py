import os
import time
import config
from logger import logger
from converter import PDFToMarkdownConverter

def process_batch():
    """Xử lý toàn bộ các file PDF nằm trong thư mục input/"""
    total_batch_start_time = time.time()

    # Kiểm tra sự tồn tại của Tesseract Executable
    if not os.path.exists(config.TESSERACT_PATH):
        logger.error(f"Chưa cài đặt Tesseract OCR hoặc sai đường dẫn: {config.TESSERACT_PATH}")
        return

    # Lấy danh sách tất cả các file .pdf trong thư mục input
    pdf_files = [f for f in os.listdir(config.DEFAULT_INPUT_DIR) if f.lower().endswith('.pdf')]

    if not pdf_files:
        logger.warning(f"Không tìm thấy tệp .pdf nào trong thư mục: {config.DEFAULT_INPUT_DIR}")
        return

    logger.info("==================================================================")
    logger.info(f"BẮT ĐẦU TIẾN TRÌNH XỬ LÝ BATCH: Tìm thấy {len(pdf_files)} tệp PDF")
    logger.info("==================================================================")

    processed_summary = []

    for idx, pdf_file in enumerate(pdf_files, start=1):
        input_pdf_path = os.path.join(config.DEFAULT_INPUT_DIR, pdf_file)
        
        # Định dạng tên file xuất .md tương ứng với tên file PDF
        output_md_name = f"{os.path.splitext(pdf_file)[0]}.md"

        logger.info(f"\n[{idx}/{len(pdf_files)}] Đang tiến hành xử lý: {pdf_file}")

        try:
            converter = PDFToMarkdownConverter(
                pdf_path=input_pdf_path,
                output_dir=config.DEFAULT_OUTPUT_DIR
            )
            file_time = converter.convert(output_md_filename=output_md_name)
            processed_summary.append({"file": pdf_file, "status": "Thành công", "time": file_time})

        except Exception as e:
            logger.error(f"Xảy ra lỗi khi xử lý tệp {pdf_file}: {str(e)}", exc_info=True)
            processed_summary.append({"file": pdf_file, "status": f"Lỗi ({str(e)})", "time": 0})

    total_batch_elapsed = time.time() - total_batch_start_time

    # Báo cáo tổng kết tiến trình
    logger.info("\n==================================================================")
    logger.info("BÁO CÁO TỔNG HỢP TỔNG THỜI GIAN XỬ LÝ")
    logger.info("==================================================================")
    for item in processed_summary:
        logger.info(f"- {item['file']}: {item['status']} ({item['time']:.2f}s)")
    
    logger.info("------------------------------------------------------------------")
    logger.info(f"Tổng số tệp đã xử lý: {len(pdf_files)}")
    logger.info(f"TỔNG THỜI GIAN TOÀN BỘ TIẾN TRÌNH: {total_batch_elapsed:.2f}s ({total_batch_elapsed / 60:.2f} phút)")
    logger.info("==================================================================\n")

if __name__ == "__main__":
    process_batch()