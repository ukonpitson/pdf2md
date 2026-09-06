import os
import re
 
# =============================================================================
# 1. CẤU HÌNH ĐƯỜNG DẪN HỆ THỐNG
# =============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_INPUT_DIR = os.path.join(BASE_DIR, "input")
DEFAULT_OUTPUT_DIR = os.path.join(BASE_DIR, "output")
DEFAULT_IMAGES_DIR = os.path.join(DEFAULT_OUTPUT_DIR, "images")

os.makedirs(DEFAULT_INPUT_DIR, exist_ok=True)
os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)
os.makedirs(DEFAULT_IMAGES_DIR, exist_ok=True)

# =============================================================================
# 2. CHUẨN HÓA VĂN BẢN & OCR
# =============================================================================
DEFAULT_FONT_FAMILY = "Sans-serif"
DEFAULT_FONT_SIZE = "14pt"
DPI = 300

# Ngôn ngữ OCR cho Windows Media OCR ('vi': Tiếng Việt, 'en': Tiếng Anh)
OCR_LANG = 'vi'

# Ngưỡng ký tự phân loại trang (>= 50 ký tự -> Native Text, < 50 -> Scan OCR)
CLASSIFY_CHAR_THRESHOLD = 50

# =============================================================================
# 3. THAM SỐ VÙNG BỐ CỤC (LAYOUT RATIOS)
# =============================================================================
HEADER_RATIO = 0.08        # Loaị bỏ 8% vùng đỉnh trang
FOOTER_RATIO = 0.08        # Loại bỏ 8% vùng đáy trang
FOOTNOTE_START_RATIO = 0.75 # Vùng tìm kiếm Footnote (75% - 92%)

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