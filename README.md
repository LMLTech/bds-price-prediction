# 🏡 Dự Báo Giá Bất Động Sản (Real Estate Price Prediction)

> **Đề tài:** Dự báo giá bất động sản dựa trên các đặc điểm tài sản và vị trí bằng phương pháp Hồi quy tuyến tính (Real Estate Price Prediction Based on Property and Location Features Using Linear Regression).

---

## 📂 Cấu Trúc Dự Án (Project Structure)

Dự án được tổ chức theo cấu trúc Data Science tiêu chuẩn:

```text
RealEstatePrediction/
│
├── data/
│   ├── raw/                        # Chứa dữ liệu gốc (house_buying_dec29th_2025.csv / dataset_BDS.xlsx)
│   └── processed/                  # Chứa dữ liệu đã xử lý (housing_clean.csv, housing_features.csv, predictions.csv)
│
├── notebooks/
│   ├── 01_data_understanding.ipynb # Phase 1: Thống kê mô tả & khám phá cấu trúc dữ liệu thô
│   ├── 02_data_cleaning.ipynb      # Phase 2: Làm sạch, lọc ngưỡng vật lý domain & tránh rò rỉ dữ liệu
│   ├── 03_eda.ipynb                # Phase 3: Khám phá quan hệ thuộc tính, ma trận tương quan & heteroscedasticity
│   ├── 04_feature_engineering.ipynb # Phase 4: Trích xuất Vị trí (Province/District) & Khoảng cách Haversine tới CBD
│   ├── 05_model_training.ipynb     # Phase 5 & 6: Train/Test Split (80/20) & Huấn luyện Pipeline Linear Regression
│   └── 06_evaluation.ipynb         # Phase 7 & 8: Kiểm định chỉ số (MAE, RMSE, R², MAPE), Residual Plots & Top Errors
│
├── src/                            # Mã nguồn mô-đun tái sử dụng
│   ├── preprocessing.py            # Hàm nạp dữ liệu & lọc sạch miền giá trị (domain knowledge)
│   ├── features.py                 # Tách chuỗi vị trí, tính khoảng cách Haversine tới CBD & chọn đặc trưng
│   ├── train.py                    # Xây dựng scikit-learn Pipeline (ColumnTransformer, StandardScaler, OneHotEncoder)
│   ├── evaluate.py                 # Đánh giá chỉ số, vẽ biểu đồ sai số Residuals & trích xuất Top lỗi dự báo
│   └── predict.py                  # Module dự đoán giá cho dữ liệu bất động sản mới
│
├── models/
│   └── linear_regression.pkl       # Pipeline mô hình đã huấn luyện
│
├── reports/
│   └── figures/                    # Nơi tự động lưu các biểu đồ (actual_vs_predicted.png, residual_plots.png)
│
├── SPECIFICATION.md                # Tài liệu yêu cầu kỹ thuật & quy chuẩn dự án
├── requirements.txt                # Danh sách thư viện Python cần thiết
└── README.md                       # Tài liệu hướng dẫn này
```

---

## ⚙️ Cài Đặt Môi Trường (Setup)

Yêu cầu máy tính đã cài đặt Python 3.8+ và pip.

Cài đặt toàn bộ thư viện phụ thuộc:

```bash
pip install -r requirements.txt
```

---

## 🚀 Quy Trình Thực Thi Dự Án (Data Pipeline & Execution)

### 1. Thực thi theo các Notebooks (Khám phá & Trực quan hóa)
Chạy lần lượt các notebook trong thư mục `notebooks/` theo thứ tự từ `01` đến `06`:
1. `notebooks/01_data_understanding.ipynb`
2. `notebooks/02_data_cleaning.ipynb`
3. `notebooks/03_eda.ipynb`
4. `notebooks/04_feature_engineering.ipynb`
5. `notebooks/05_model_training.ipynb`
6. `notebooks/06_evaluation.ipynb`

### 2. Thực thi qua Mô-đun Python (`src/`)
Có thể chạy trực tiếp các mô-đun Python trong thư mục `src/` để tái tạo toàn bộ pipeline huấn luyện và dự báo.

---

## 📊 Kết Quả Đánh Giá Mô Hình (Model Performance)

Mô hình **Multiple Linear Regression** đạt các chỉ số kiểm định trên tập Test (20% dữ liệu):

- **$R^2$**: `0.3017` (Giải thích được 30.17% sự biến thiên của giá bất động sản dựa trên đặc điểm kết cấu và vị trí).
- **MAE**: `8,417.96` triệu VNĐ (~8.42 tỷ VNĐ).
- **RMSE**: `22,620.56` triệu VNĐ (~22.62 tỷ VNĐ).

Biểu đồ so sánh Giá thực tế vs Giá dự đoán và Phân phối sai số dư được tự động xuất ra tại thư mục `reports/figures/`.