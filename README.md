🏡 Dự Báo Giá Bất Động Sản (Hà Nội & TP.HCM)

> **Đề tài:** Ứng dụng mô hình Hồi quy tuyến tính đa biến (Multiple Linear Regression) trong việc dự báo giá bán bất động sản dựa trên đặc điểm kết cấu và vị trí không gian địa lý.

Dự án này tập trung phân tích và mô hình hóa dữ liệu bất động sản tại hai thị trường trọng điểm là **Hà Nội** và **Thành phố Hồ Chí Minh**. Bằng việc loại bỏ nhiễu từ các tỉnh lẻ, mô hình hướng tới việc đạt được độ chính xác (R²) cao nhất.

---

## 📂 Cấu Trúc Dự Án (Project Structure)

Nhóm thống nhất sử dụng cấu trúc thư mục dưới đây để không bị xung đột mã nguồn (conflict) trong quá trình ráp code:

```text
bds-price-prediction/
│
├── data/
│   ├── raw/                        # Chứa dữ liệu gốc tải từ Kaggle (dataset_BDS.xlsx)
│   └── processed/                  # Chứa dữ liệu SẠCH sau khi Chương 3 chạy xong (dataset_BDS_cleaned.csv)
│
├── src/
│   ├── chuong3_tien_xu_ly.py       # Code: Làm sạch, Geocoding, tính khoảng cách (Liêm)
│   ├── chuong4_xay_dung_mo_hinh.py # Code: Train/Test Split, Hồi quy tuyến tính (Thái)
│   └── chuong4_truc_quan_hoa.py    # Code: Đánh giá sai số, vẽ biểu đồ (Ngọc Anh)
│
├── images/                         # Nơi tự động lưu các biểu đồ (Heatmap, Scatter plot...)
├── requirements.txt                # Danh sách thư viện Python cần thiết
└── README.md                       # Tài liệu hướng dẫn này
⚙️ Cài Đặt Môi Trường (Setup)
Yêu cầu máy tính đã cài đặt sẵn Python 3.8+ và Visual Studio Code.

Bước 1: Mở thư mục dự án bằng Visual Studio Code.

Bước 2: Mở Terminal (Phím tắt: Ctrl + `).

Bước 3: Cài đặt toàn bộ thư viện đồng nhất cho cả nhóm bằng lệnh:

Bash
pip install -r requirements.txt
🚀 Hướng Dẫn Chạy Mã Nguồn (Quy Trình Pipeline)
⚠️ LƯU Ý: Các thành viên phải chạy code theo đúng thứ tự dưới đây để luồng dữ liệu (Data Pipeline) không bị đứt gãy.

1️⃣ Giai đoạn Tiền xử lý (Thực hiện bởi: Lê Minh Liêm)
Thao tác: Chạy file src/chuong3_tien_xu_ly.py.

Nhiệm vụ: Đọc file Excel gốc, lọc riêng HN & HCM, điền khuyết (Median), tính khoảng cách Haversine đến trung tâm, loại bỏ ngoại lệ (IQR), và sinh ra ma trận tương quan.

Đầu ra (Output): Tạo ra file dữ liệu hoàn toàn sạch data/processed/dataset_BDS_cleaned.csv đưa cho Thái.

2️⃣ Giai đoạn Huấn luyện Mô hình (Thực hiện bởi: Vũ Nguyên Quốc Thái)
Thao tác: Chạy file src/chuong4_xay_dung_mo_hinh.py.

Nhiệm vụ: Đọc file .csv sạch ở bước 1, thực hiện chia tập train_test_split (80/20), chuẩn hóa StandardScaler và huấn luyện mô hình Hồi quy tuyến tính (Linear Regression).

Đầu ra (Output): Các chỉ số đánh giá mô hình: MAE, RMSE, R² và các hệ số hồi quy (Coefficients).

3️⃣ Giai đoạn Trực quan hóa (Thực hiện bởi: Ngọc Anh)
Thao tác: Chạy file src/chuong4_truc_quan_hoa.py (sau khi Thái đã code xong mô hình).

Nhiệm vụ: Vẽ biểu đồ so sánh Giá thực tế vs. Giá dự đoán, biểu đồ phân phối sai số (Residuals).

Đầu ra (Output): Hình ảnh .png lưu vào thư mục images/ để chèn vào báo cáo Word.

Dự án thực hiện phục vụ bài tập lớn môn học.