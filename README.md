# DỰ ÁN PDF2MD - CHUYỂN ĐỔI PDF TIẾNG VIỆT SANG MARKDOWN

Công cụ hỗ trợ trích xuất tài liệu PDF (Native Text & Scanned PDF) sang định dạng Markdown chuẩn, hỗ trợ OCR Tiếng Việt chính xác, tách bảng, cắt ảnh và tự động tổng hợp Footnote.

---

## 1. YÊU CẦU NỀN TẢNG (PREREQUISITES)

* **Hệ điều hành:** Windows 10 / Windows 11 (64-bit).
* **Môi trường:** Python 3.9 trở lên (Khuyên dùng Python 3.10 hoặc 3.11).

---

## 2. NƠI TẢI PHẦN MỀM & DỮ LIỆU CẦN THIẾT

### A. Công cụ Poppler for Windows (Bắt buộc)
* **Link tải:** [Poppler for Windows - Release 24.08.0](https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0-0/Release-24.08.0-0.zip)

### B. Các Mô hình OCR EasyOCR (Nếu cài cho MÁY OFFLINE)
Tải 3 tệp nén đính kèm dưới đây từ máy có kết nối Internet (giữ nguyên định dạng `.zip` không giải nén):
1. **Mô hình phát hiện văn bản (Craft Model):** [craft_mlt_25k.zip](https://github.com/JaidedAI/EasyOCR/releases/download/v1.3/craft_mlt_25k.zip)
2. **Mô hình nhận diện Tiếng Việt (Vietnamese Model):** [vietnamese.zip](https://github.com/JaidedAI/EasyOCR/releases/download/v1.3/vietnamese.zip)
3. **Mô hình nhận diện Tiếng Anh (English Model):** [latin.zip](https://github.com/JaidedAI/EasyOCR/releases/download/v1.0.8/latin.zip)

---

## 3. HƯỚNG DẪN CÀI ĐẶT DÙNG CHO MÁY ONLINE (CÓ INTERNET)

### Bước 1: Cài đặt Poppler
1. Giải nén file `Release-24.08.0-0.zip` đã tải vào ổ `C:\poppler\`.
2. Đảm bảo đường dẫn tới các tệp thực thi là: `C:\poppler\Release-24.08.0-0\poppler-24.08.0\Library\bin`.

### Bước 2: Cài đặt thư viện Python
Mở Terminal/CMD tại thư mục dự án và chạy:
```bash
pip install -r requirements.txt

```

### Bước 3: Cấu hình chế độ Online

Trong file `config.py`, cài đặt tham số:

```python
OFFLINE_MODE = False

```

*(EasyOCR sẽ tự động tải các tệp model về máy ở lần chạy đầu tiên).*

---

## 4. HƯỚNG DẪN CÀI ĐẶT DÙNG CHO MÁY OFFLINE (KHÔNG CÓ INTERNET)

### Bước 1: Cài đặt Poppler

Giải nén Poppler vào ổ `C:\poppler\` tương tự như trên máy Online.

### Bước 2: Cài đặt Python Packages Offline

* **Trên máy Online:** Tải toàn bộ các wheel package về thư mục:
```bash
pip download -r requirements.txt -d ./wheels

```


* **Trên máy Offline:** Copy thư mục `wheels` sang máy offline và cài đặt:
```bash
pip install --no-index --find-links=./wheels -r requirements.txt

```



### Bước 3: Đặt mô hình EasyOCR vào đúng thư mục hệ thống

1. Copy 3 file `.zip` (`craft_mlt_25k.zip`, `vietnamese.zip`, `latin.zip`) sang máy Offline.
2. Truy cập vào đường dẫn sau trên Windows (Tự tạo folder nếu chưa có):
```text
C:\Users\<Tên_User_Windows>\.EasyOCR\model\

```


*(Ví dụ: `C:\Users\Admin\.EasyOCR\model\`)*
3. **Dán (Paste) cả 3 file `.zip` vào thư mục `model` này (KHÔNG GIẢI NÉN).**

### Bước 4: Cấu hình chế độ Offline

Trong tệp `config.py`, chuyển biến cấu hình sang `True`:

```python
OFFLINE_MODE = True

```

---

## 5. HƯỚNG DẪN SỬ DỤNG DỰ ÁN

1. Sao chép file PDF cần chuyển đổi vào thư mục `./input/`.
2. Mở file `main.py` và chỉnh sửa tên tệp đầu vào ở dòng:
```python
input_pdf_name = "ten_file_cua_ban.pdf"

```


3. Chạy chương trình:
```bash
python main.py

```


4. Kết quả xuất ra sẽ nằm ở thư mục `./output/result.md` và toàn bộ hình ảnh/bảng biểu nằm tại `./output/images/`.
