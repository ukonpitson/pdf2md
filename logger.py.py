import os
import logging
from datetime import datetime
import config

def setup_logger():
    """Tạo và cấu hình logger ghi ra file theo ngày (log_YYYY-MM-DD.log) và console"""
    today_str = datetime.now().strftime("%Y-%m-%d")
    log_filename = f"log_{today_str}.log"
    log_file_path = os.path.join(config.DEFAULT_LOGS_DIR, log_filename)

    logger = logging.getLogger("PDF2MD_Logger")
    logger.setLevel(logging.INFO)

    # Tránh nhân đôi log nếu hàm được gọi nhiều lần
    if logger.hasHandlers():
        logger.handlers.clear()

    # Formatter chung cho Log
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s", 
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File Handler - Ghi log vào file trong thư mục logs/
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console Handler - In log ra màn hình Terminal
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

logger = setup_logger()