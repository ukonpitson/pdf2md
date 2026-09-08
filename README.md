# 📄 PDF to Markdown Converter (Automated Hybrid Pipeline)

Hệ thống tự động chuyển đổi tài liệu PDF (dạng **Native Text** hoặc **Scanned Image**) sang định dạng **Markdown (.md)** chuẩn hóa. Phần mềm áp dụng mô hình kiến trúc phân luồng đa nhánh dựa trên thị giác máy tính (OpenCV) và biểu thức chính quy (Regex).

---

## 🚀 TÍNH NĂNG NỔI BẬT

- **Phân luồng đa nhánh thông minh (Hybrid Engine):**
  - **Nhánh A (Native Text PDF):** Trích xuất văn bản trực tiếp từ lớp vector với tốc độ cao và độ chính xác 100%.
  - **Nhánh B (Scanned Image PDF):** Khử nhiễu, nhị phân hóa ảnh thích ứng (OpenCV) và nhận diện chữ bằng OCR (Tesseract / PaddleOCR).
- **Chuẩn hóa văn bản:** Loại bỏ toàn bộ định dạng font/style phức tạp của PDF gốc, mặc định toàn bộ nội dung xuất ra dạng phông **Sans-Serif, Kích thước 14pt**.
- **Cấu trúc hóa bằng Regex:** Tự động nhận diện các cấp tiêu đề (`# Heading 1`, `## Heading 2`, `### Heading 3`), danh sách liệt kê (`-`, `1.`) và trích dẫn dựa trên biểu thức chính quy.
- **Tự động bóc tách Hình ảnh & Bảng:**
  - Tự động phát hiện và cắt mọi hình ảnh, sơ đồ trong tài liệu.
  - **Coi Bảng như 1 hình ảnh:** Cắt trọn vẹn khối Bảng thành ảnh riêng biệt thay vì OCR lại cấu trúc dòng/cột, giúp bảo toàn tính trực quan.
  - Quy chuẩn đặt tên lưu trữ đồng nhất: `page-#_img-#.png`.
- **Quản lý Footnote tập trung:** Gom toàn bộ ghi chú chân trang (Footnote) về cuối tập tin Markdown, kèm theo thẻ đánh dấu rõ xuất xứ từ **Trang gốc nào (Page #)** giúp dễ dàng rà soát và đối chiếu.

---

## 🛠️ YÊU CẦU MÔI TRƯỜNG & HỆ THỐNG

### 1. Công nghệ sử dụng (Tech Stack)
* **Ngôn ngữ:** Python 3.10+
* **Thư viện chính:**
  * `PyMuPDF` (`fitz`): Đọc và xử lý cấu trúc PDF vector.
  * `pdf2image`: Render trang PDF thành ảnh bitmap.
  * `opencv-python` & `Pillow`: Xử lý ảnh, cắt bảng và hình ảnh.
  * `pytesseract`: Giao tiếp với công cụ Tesseract OCR.

### 2. Công cụ phụ thuộc ngoài (External Dependencies)
Để hệ thống chạy trọn vẹn cả Nhánh B (OCR), máy tính cần được cài đặt sẵn:
1. **Poppler:** Phục vụ cho thư viện `pdf2image`.
2. **Tesseract-OCR:** Cài đặt phần mềm Tesseract và tải thêm gói ngôn ngữ Tiếng Việt (`vie.traineddata`).

---

## 📥 HƯỚNG DẪN CÀI ĐẶT

Cài đặt Poppler

``` Bash
winget install oschwartz10612.Poppler
```

Cài đặt biến môi trường (Environment Variables)


### Bước 1: Clone repository và tạo môi trường ảo
```bash
git clone [https://github.com/your-username/pdf-to-markdown-converter.git](https://github.com/your-username/pdf-to-markdown-converter.git)
cd pdf-to-markdown-converter

# Tạo và kích hoạt môi trường ảo (Khuyên dùng)
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Bước 2: Cài đặt các thư viện Python
```bash
pip install -r requirements.txt
```
Nội dung tệp requirements.txt:
```Plaintext
PyMuPDF>=1.23.0
pdf2image>=1.16.3
opencv-python>=4.8.0
Pillow>=10.0.0
pytesseract>=0.3.10
numpy>=1.24.0
```

## 💻 HƯỚNG DẪN SỬ DỤNG

### 1. Cấu trúc thư mục dự án
```Plaintext
├── input/                  # Thư mục chứa các file PDF đầu vào
├── output/                 # Thư mục chứa file .md và ảnh xuất ra
│   ├── images/             # Chứa các file page-#_img-#.png (Bảng & Ảnh cắt)
│   └── result.md           # Tệp Markdown hoàn chỉnh
├── converter.py            # Mã nguồn xử lý chính (Pipeline Engine)
├── main.py                 # File thực thi chương trình
├── requirements.txt        # Danh sách thư viện cần thiết
└── README.md               # Tài liệu hướng dẫn
```

### Chạy chương trình qua Python
```Python
from converter import PDFToMarkdownConverter

# Khởi tạo converter với file PDF đầu vào
converter = PDFToMarkdownConverter(
    pdf_path="./input/tai_lieu_mau.pdf",
    output_dir="./output"
)

# Tiến hành chuyển đổi
converter.convert(output_md_filename="ket_qua.md")
```

## 📂 KẾT QUẢ ĐẦU RA MẪU (OUTPUT STRUCTURE)

Tệp .md sau khi xuất sẽ có định dạng tương tự mẫu dưới đây:
```Markdown
# CHƯƠNG I: TỔNG QUAN HỆ THỐNG

Tài liệu này mô tả chi tiết quy trình chuyển đổi tài liệu PDF sang dạng định dạng Markdown chuẩn [^fn_1].

## 1.1 PHÂN TÍCH THÔNG SỐ

Dưới đây là sơ đồ kiến trúc hệ thống được trích xuất từ tài liệu gốc:

![Nội dung trích xuất tại trang 1](./images/page-1_img-1.png)

### a) Bảng dữ liệu thực nghiệm

Toàn bộ dữ liệu đo đạc được đóng gói dưới dạng bảng hình ảnh [^fn_2]:

![Nội dung trích xuất tại trang 2](./images/page-2_img-1.png)

- Đã hoàn tất công đoạn cắt ảnh.
- Đã lưu file đúng định dạng đặt tên.

---

## NỘI DUNG GHI CHÚ CHÂN TRANG (FOOTNOTES)

[^fn_1]: *(Trang 1)* Quy trình này áp dụng cho các tài liệu kỹ thuật phát hành từ năm 2024.
[^fn_2]: *(Trang 2)* Bảng số liệu được tổng hợp từ thiết bị đo tự động.
```

## ⚙️ BẢNG THAM SỐ CẤU HÌNH (CONFIGURATION)

|Tham số | Giá trị mặc định | Mô tả|
|--------------------|------|------|
|DEFAULT_FONT_SIZE | 14pt | Kích thước chữ mặc định cho toàn bộ text|
|DPI | 300 | Độ phân giải render khi xuất và cắt ảnh|
|HEADER_RATIO | 0.08 | Vùng đỉnh trang (8%) dành cho Header (bị loại bỏ)|
|FOOTER_RATIO | 0.08 | Vùng đáy trang (8%) dành cho Footer (bị loại bỏ)|
|FOOTNOTE_REGION | 0.25 | Vùng đáy trang (25%) để tìm kiếm Footnote|

## 📝 LICENSE & DỰ ÁN

Dự án được phát hành dưới bản quyền MIT License. Mọi đóng góp, báo lỗi (Issues) hoặc yêu cầu tính năng mới (Pull Requests) đều được chào đón!