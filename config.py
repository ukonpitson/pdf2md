import os
import re

# =============================================================================
# 1. CẤU HÌNH ĐƯỜNG DẪN HỆ THỐNG, CÔNG CỤ & LOGS
# =============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_INPUT_DIR = os.path.join(BASE_DIR, "input")
DEFAULT_OUTPUT_DIR = os.path.join(BASE_DIR, "output")
DEFAULT_IMAGES_DIR = os.path.join(DEFAULT_OUTPUT_DIR, "images")
DEFAULT_LOGS_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(DEFAULT_INPUT_DIR, exist_ok=True)
os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)
os.makedirs(DEFAULT_IMAGES_DIR, exist_ok=True)
os.makedirs(DEFAULT_LOGS_DIR, exist_ok=True)

# Đường dẫn tới thư mục bin của Poppler
POPPLER_PATH = r"E:\sw\poppler-26.07.0\Library\bin"

# Đường dẫn tệp thực thi Tesseract OCR trên Windows
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# =============================================================================
# 2. CẤU HÌNH NGÔN NGỮ OCR & XỬ LÝ ẢNH
# =============================================================================
TESSDATA_LANG = "vie+eng"

DPI = 300
CLASSIFY_CHAR_THRESHOLD = 50  # Số ký tự tối thiểu để coi là Native Text

# =============================================================================
# 3. THAM SỐ VÙNG BỐ CỤC (LAYOUT RATIOS)
# =============================================================================
HEADER_RATIO = 0.08          # Loại bỏ 8% vùng đỉnh trang
FOOTER_RATIO = 0.08          # Loại bỏ 8% vùng đáy trang
FOOTNOTE_START_RATIO = 0.75  # Vùng quét Footnote (75% - 92%)

# =============================================================================
# 4. QUY CHUẨN ĐẶT TÊN VÀ XUẤT FOOTNOTE
# =============================================================================
IMAGE_NAMING_PATTERN = "page-{page_num}_img-{img_num}.png"
FOOTNOTE_SECTION_HEADER = "\n---\n\n## NỘI DUNG GHI CHÚ CHÂN TRANG (FOOTNOTES)\n"
FOOTNOTE_FMT = "[^fn_{idx}]: *(Trang {page})* {text}"

# =============================================================================
# 5. BIỂU THỨC CHÍNH QUY (REGEX) STRUCTURE MARKDOWN
# =============================================================================
REGEX_PATTERNS = {
    "H1": re.compile(r'^(CHƯƠNG|PHẦN|MỤC|PART|CHAPTER)\s+([IVXLCDM\d]+)[:\.]?|^[IVXLCDM]+\.\s+', re.IGNORECASE),
    "H2": re.compile(r'^\d+\.\d+\s+|^[A-Z]\.\s+'),
    "H3": re.compile(r'^\d+\.\d+\.\d+\s+|^[a-z]\)\s+'),
    "LIST_BULLET": re.compile(r'^[\bullet\-\*•]\s+'),
    "LIST_NUMBER": re.compile(r'^\d+[\.\)]\s+')
}