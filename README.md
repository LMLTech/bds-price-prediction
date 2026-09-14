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
│   ├── 06_evaluation.ipynb         # Phase 7 & 8: Kiểm định chỉ số (MAE, RMSE, R², MAPE), Residual Plots & Top Errors
│   └── 07_model_audit_and_improvement.ipynb # Audit nâng cao,Root Cause, Controlled Experiments & Final Verification
│
├── src/                            # Mã nguồn mô-đun tái sử dụng
│   ├── preprocessing.py            # Hàm nạp dữ liệu & lọc sạch miền giá trị (domain knowledge)
│   ├── features.py                 # Tách chuỗi vị trí, tính khoảng cách Haversine tới CBD & chọn đặc trưng
│   ├── train.py                    # Xây dựng scikit-learn Pipeline (ColumnTransformer, StandardScaler, OneHotEncoder)
│   ├── evaluate.py                 # Đánh giá chỉ số, vẽ biểu đồ sai số Residuals & trích xuất Top lỗi dự báo
│   ├── predict.py                  # Module dự đoán giá cho dữ liệu bất động sản mới
│   └── visualization.py            # Hệ thống trực quan hóa 15 biểu đồ học thuật chuẩn mực
│
├── models/
│   └── linear_regression.pkl       # Pipeline mô hình đã huấn luyện
│
├── reports/
│   └── figures/                    # Nơi lưu 15 biểu đồ học thuật (01_price_distribution.png -> 15_top_prediction_errors.png)
│
├── SPECIFICATION.md                # Tài liệu yêu cầu kỹ thuật & quy chuẩn dự án
├── requirements.txt                # Danh sách thư viện Python cần thiết
└── README.md                       # Tài liệu hướng dẫn này
```

---

## 🎨 Lớp Trực Quan Hóa (Academic Visualization Layer)

Dự án tích hợp lớp trực quan hóa chuẩn học thuật tại `src/visualization.py` gồm 15 biểu đồ:

### Group A — Dataset Overview
- `01_price_distribution.png`: Raw Target Price Distribution (Skewness = 8.16).
- `02_log_price_distribution.png`: Log-Transformed Price Distribution (`log1p`).

### Group B — Property Characteristics
- `03_area_vs_price.png`: Property Area vs Price Scatter Plot.
- `04_price_by_bedrooms.png`: Price Distribution by Bedroom Count (Boxplot).
- `05_price_by_area_bucket.png`: Median Price and Property Count by Area Segment.

### Group C — Location & Distance
- `06_avg_price_by_district.png`: Top 10 Districts by Average Property Price in Dataset.
- `07_median_price_per_m2_by_district.png`: Top 10 Districts by Median Price/m² (EDA Only).
- `08_distance_vs_price.png`: Distance to CBD Spatial Proxy vs Price Scatter Plot.
- `09_price_by_distance_bucket.png`: Median Price and Property Count across Distance Bands.

### Group D — Model Performance
- `10_actual_vs_predicted.png`: Actual vs Predicted Price — Final Linear Regression (Raw Predictions).
- `11_residual_distribution.png`: Residual Error Distribution (`Actual - Predicted`).
- `12_residual_vs_predicted.png`: Residual vs Predicted Plot (Heteroscedasticity Check).

### Group E — Error Analysis
- `13_absolute_error_distribution.png`: Absolute Error Distribution (`|Actual - Predicted|`).
- `14_error_by_price_range.png`: Prediction Error (MAE & RMSE) by Actual Price Range.
- `15_top_prediction_errors.png`: Top 20 Largest Prediction Errors (PII Omitted).

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
Chạy lần lượt các notebook trong thư mục `notebooks/` theo thứ tự từ `01` đến `07`:
1. `notebooks/01_data_understanding.ipynb`
2. `notebooks/02_data_cleaning.ipynb`
3. `notebooks/03_eda.ipynb`
4. `notebooks/04_feature_engineering.ipynb`
5. `notebooks/05_model_training.ipynb`
6. `notebooks/06_evaluation.ipynb`
7. `notebooks/07_model_audit_and_improvement.ipynb`

---

## 📊 Kết Quả Đánh Giá Mô Hình (Final Candidate Performance)

Mô hình **Multiple Linear Regression** đạt các chỉ số kiểm định chuẩn trên tập Test ($N=9,172$):

- **Raw Model Output (Unclipped $X\beta + b$)**:
  - **$R^2$**: `0.3729` (Tăng +7.12% so với baseline cũ `0.3017`).
  - **MAE**: `8,417.93` triệu VNĐ (~8.42 tỷ VNĐ).
  - **RMSE**: `21,435.74` triệu VNĐ (~21.44 tỷ VNĐ).
  - **Negative Predictions**: 747 mẫu ($8.14\%$).

- **Post-Processed Output (`np.maximum(pred, 0)`)**:
  - **$R^2$**: `0.3839`.
  - **MAE**: `8,065.00` triệu VNĐ (~8.07 tỷ VNĐ).
  - **RMSE**: `21,247.69` triệu VNĐ (~21.25 tỷ VNĐ).
  - **Clipped Zeros**: 747 mẫu ($8.14\%$).

- **5-Fold Cross-Validation (on $X_{train}$)**:
  - **CV Mean $R^2$**: `0.3665 ± 0.0387` (Đồng nhất hoàn toàn với Test Set).

---

## 🌐 Ứng Dụng Web (Web Application: FastAPI + Angular)

Dự án được mở rộng thành ứng dụng web hoàn chỉnh gồm:
- **FastAPI Backend (Python)**: REST API thực thi pipeline ML và phục vụ tài nguyên trực quan hóa.
- **Angular Frontend (TypeScript)**: Giao diện web khoa học, hỗ trợ dự báo thời gian thực và Dashboard trực quan hóa 15 biểu đồ.

### 1. Khởi động FastAPI Backend (Port 8000)

```bash
# Từ thư mục gốc dự án:
uvicorn backend.main:app --reload --port 8000
```
- API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
- Health Check: [http://localhost:8000/api/health](http://localhost:8000/api/health)

### 2. Khởi động Angular Frontend (Port 4200)

```bash
# Di chuyển vào thư mục frontend:
cd frontend

# Khởi chạy máy chủ phát triển Angular:
npm start
```
- Web Application UI: [http://localhost:4200](http://localhost:4200)
- Các trang chính:
  - `/`: Trang chủ tổng quan & quy trình pipeline
  - `/predict`: Form nhập thuộc tính & dự báo giá bất động sản
  - `/visualization`: Dashboard trực quan hóa 15 biểu đồ học thuật
  - `/model`: Thông tin mô hình, chỉ số & hạn chế học thuật