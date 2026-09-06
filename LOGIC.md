Dưới đây là mô tả quy trình chuyển đổi tài liệu PDF sang định dạng Markdown theo đúng logic thuật toán xử lý dữ liệu và hình ảnh, không đề cập đến tên công cụ hay mã nguồn.

---

### TỔNG QUAN LUỒNG XỬ LÝ (PIPELINE)

```
[Mở tệp PDF và phân tích từng trang]
                 │
                 ▼
     [Phân loại tính chất trang]
                 │
  ┌──────────────┴──────────────┐
  ▼                             ▼
[Dạng A: Văn bản gốc]       [Dạng B: Bản quét / Ảnh]
  │                             │
  ├─ Cắt xuất Ảnh/Bảng          ├─ Số hóa trang thành Ảnh
  ├─ Loại bỏ Header/Footer      ├─ Tiền xử lý & Khử nhiễu
  ├─ Lọc bóc tách Footnote      ├─ Tìm & Cắt xuất Bảng/Ảnh
  └─ Gộp đoạn & Gán cấu trúc    ├─ Xóa vùng thừa & Trích Footnote
                                └─ Phân tích ký tự OCR & Gán cấu trúc
  │                             │
  └──────────────┬──────────────┘
                 ▼
[Tổng hợp và Xuất tệp Markdown chuẩn]

```

---

### CHI TIẾT CÁC BƯỚC THỰC HIỆN

#### BƯỚC 1: KHỞI TẠO VÀ PHÂN LOẠI TRANG

1. **Khởi tạo:** Thiết lập hệ thống lưu trữ đầu ra (thư mục chứa ảnh và tệp văn bản đích).
2. **Đọc và Phân loại:**
* Hệ thống quét từng trang PDF và đếm số lượng ký tự văn bản có thể trích xuất trực tiếp.
* **Trang văn bản gốc (Dạng A):** Nếu số ký tự đạt từ threshold tối thiểu (ví dụ: $\ge 50$ ký tự), trang được chuyển sang nhánh xử lý văn bản gốc.
* **Trang bản quét/ảnh (Dạng B):** Nếu số ký tự quá ít hoặc bằng 0, trang được coi là ảnh scan và chuyển sang nhánh xử lý hình ảnh OCR.



---

#### BƯỚC 2: XỬ LÝ TRANG VĂN BẢN GỐC (DẠNG A)

1. **Trích xuất & Lưu trữ Hình ảnh / Bảng biểu:**
* Quét và trích xuất toàn bộ ảnh nhúng (Raster/Vector) trong trang, lưu thành tệp hình ảnh độc lập và chèn đường dẫn ảnh vào luồng văn bản.
* Nhận diện tọa độ vùng chứa bảng, chụp/cắt riêng vùng bảng biểu thành hình ảnh độ phân giải cao và chèn cú pháp hiển thị ảnh tương ứng.


2. **Lọc bỏ Vùng Tạp nhiễu (Header / Footer):**
* Xác định ranh giới hình học của trang.
* Loại bỏ toàn bộ nội dung nằm ở vùng đỉnh trang (8% trên cùng - tiêu đề trang, logo) và vùng đáy trang (8% dưới cùng - số trang, thông tin chân trang).


3. **Bóc tách Ghi chú chân trang (Footnotes):**
* Quét vùng sát đáy trang (từ 75% đến 92% chiều cao trang).
* Nếu phát hiện các đoạn văn bản ngắn mang đặc trưng của ghi chú, tách riêng nội dung này ra khỏi luồng chính, đánh dấu vị trí tham chiếu dạng `[^fn_x]` và đưa ghi chú vào danh sách chờ tổng hợp.


4. **Tái cấu trúc Đoạn văn & Nhận diện Cấu trúc:**
* Gom nhóm các dòng chữ theo từng khối văn bản (Text Block) để nối liền các câu bị ngắt dòng lắt léo thành một đoạn văn hoàn chỉnh.
* Phân tích các quy tắc ký tự ở đầu dòng (Regex):
* Nhận diện các tiêu đề lớn (`CHƯƠNG`, `PHẦN`, chữ số La Mã) $\rightarrow$ Đổi thành tiêu đề Cấp 1 (`#`).
* Nhận diện các tiểu mục số (`1.1`, `A.`) $\rightarrow$ Đổi thành tiêu đề Cấp 2 (`##`).
* Nhận diện các ký hiệu đầu dòng (dấu gạch ngang, chấm tròn, số thứ tự) $\rightarrow$ Đổi thành danh sách Markdown (`-` hoặc `1.`).





---

#### BƯỚC 3: XỬ LÝ TRANG BẢN QUÉT / ẢNH (DẠNG B)

1. **Chuyển đổi Trang sang Hình ảnh độ phân giải cao:**
* Render toàn bộ trang PDF thành một mảng hình ảnh màu ở độ phân giải 300 DPI để đảm bảo độ sắc nét cho việc nhận diện.


2. **Tiền xử lý Hình ảnh (Image Preprocessing):**
* Chuyển đổi ảnh sang dạng ảnh xám (Grayscale).
* Áp dụng thuật toán nhị phân hóa động (Adaptive Thresholding) để tách biệt rõ ràng giữa nét chữ (màu đen) và nền giấy (màu trắng), loại bỏ hiện tượng bóng đổ hoặc vết nhòe.


3. **Tách & Cắt các Khối Bảng / Hình ảnh:**
* Tìm kiếm các đường viền hình học (Contour) của các khối nội dung trên trang.
* Tách riêng các khung có diện tích lớn (ví dụ: rộng $> 30\%$ và cao $> 10\%$ trang) đại diện cho bảng biểu hoặc sơ đồ, lưu thành tệp ảnh độc lập và chèn liên kết vào văn bản.
* **Tô lấp vùng đã cắt (Masking):** Tô màu trắng đè lên các vùng ảnh/bảng vừa cắt để công đoạn đọc chữ tiếp theo không bị lặp lại nội dung trong bảng.


4. **Xóa Header/Footer & Trích Footnote từ Ảnh:**
* Tô màu trắng đè lên vùng Header (8% đỉnh) và Footer (8% đáy) để xóa bỏ hoàn toàn thông tin thừa.
* Cắt riêng khung vùng Footnote (75% - 92% đáy trang), thực hiện đọc chữ riêng cho vùng này, đưa nội dung vào danh sách Footnotes và tô trắng vùng đó trên ảnh chính.


5. **Đọc & Phân tích Ký tự (OCR):**
* Quét toàn bộ vùng văn bản còn lại trên bức ảnh đã qua xử lý.
* Trích xuất danh sách các dòng chữ nhận diện được.
* Áp dụng bộ lọc quy tắc cấu trúc (Regex) tương tự Nhánh A để chuyển đổi các dòng tiêu đề và danh sách về đúng cú pháp Markdown.



---

#### BƯỚC 4: TỔNG HỢP VÀ XUẤT TỆP KẾT QUẢ

1. **Gộp Nội dung các Trang:** Nối toàn bộ nội dung văn bản đã được chuẩn hóa của từng trang theo đúng thứ tự xuất hiện, ngăn cách giữa các trang bằng đường phân cách (`---`).
2. **Tổng hợp Footnotes:** Gom toàn bộ các ghi chú chân trang đã bóc tách trong suốt quá trình xử lý, định dạng lại thành phần ghi chú cuối tài liệu theo chuẩn Markdown (`[^fn_x]: Nội dung...`).
3. **Xuất tệp hoàn chỉnh:** Ghi toàn bộ dữ liệu văn bản ra tệp định dạng `.md` cùng hệ thống thư mục hình ảnh đính kèm.