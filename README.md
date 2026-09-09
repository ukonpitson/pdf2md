# DỰ ÁN PDF2MD - CHUYỂN ĐỔI PDF TIẾNG VIỆT SANG MARKDOWN (CẬP NHẬT 2026)

Công cụ trích xuất tài liệu PDF (Native Text & Scan) sang định dạng Markdown chuẩn, tích hợp công nghệ **Tesseract OCR (Google)** tối ưu chuyên dụng cho Tiếng Việt. Đã tương thích hoàn toàn với bộ thư viện mới nhất năm 2026 (`NumPy 2.5+`, `PyMuPDF 1.28+`, `Pillow 12.3+`, `OpenCV 5.0+`).

---

## 1. YÊU CẦU NỀN TẢNG (PREREQUISITES)

* **Hệ điều hành:** Windows 10 / Windows 11 (64-bit).
* **Môi trường:** Python 3.10 trở lên.

---

## 2. DÂN SÁCH PHẦN MỀM CẦN TẢI & CÀI ĐẶT

### A. Công cụ Poppler for Windows (Bắt buộc)
* **Link tải:** [Poppler Release 24.08.0](https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0-0/Release-24.08.0-0.zip)
* **Giải nén vào:** `C:\poppler\` (Thư mục chứa file thực thi: `C:\poppler\Release-24.08.0-0\poppler-24.08.0\Library\bin`).

### B. Bộ Engine Tesseract OCR for Windows (Bắt buộc)
* **Link tải:** [Tesseract-OCR Installer (UB-Mannheim)](https://github.com/UB-Mannheim/tesseract/wiki)
* **Cài đặt:** Chạy file `.exe`, cài đặt mặc định vào: `C:\Program Files\Tesseract-OCR`.

### C. Gói Dữ Liệu Ngôn Ngữ Tiếng Việt (`vie.traineddata`)
* **Link tải chính thức:** [vie.traineddata (GitHub)](https://github.com/tesseract-ocr/tessdata_fast/raw/main/vie.traineddata)
* **Thao tác:** Copy tệp `vie.traineddata` vào thư mục tessdata:
  ```text
  C:\Program Files\Tesseract-OCR\tessdata\

```

---

## 3. HƯỚNG DẪN CÀI ĐẶT MÔI TRƯỜNG PYTHON

### Dùng cho máy Online (Có Internet)

Mở Terminal tại thư mục dự án và chạy:

```bash
pip install -r requirements.txt

```

### Dùng cho máy Offline (Không có Internet)

1. **Trên máy Online:** Tải toàn bộ package về thư mục `wheels`:
```bash
pip download -r requirements.txt -d ./wheels

```


2. **Trên máy Offline:** Copy thư mục `wheels` sang máy offline và cài đặt:
```bash
pip install --no-index --find-links=./wheels -r requirements.txt

```



---

## 4. QUY TRÌNH CHẠY DỰ ÁN

1. Đặt file PDF cần chuyển đổi vào thư mục `./input/tai_lieu_mau.pdf`.
2. Chạy ứng dụng bằng lệnh:
```bash
python main.py

```


3. Kết quả xuất ra tại:
* **Tệp Markdown:** `./output/result.md`
* **Hình ảnh & Bảng biểu trích xuất:** `./output/images/`
