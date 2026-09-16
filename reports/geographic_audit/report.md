# BÁO CÁO NGHIÊN CỨU & KIỂM ĐỊNH TÍNH TỔNG QUÁT HÓA ĐỊA LÝ (GEOGRAPHIC GENERALIZATION AUDIT REPORT)

**Đề tài:** Real Estate Price Prediction Based on Property and Location Features Using Linear Regression  
**Đối tượng kiểm định:** Notebook 09 (`notebooks/09_geographic_generalization_audit.ipynb`) & Các mô hình thực nghiệm  
**Trạng thái hệ thống:** Read-Only Research Audit (Mô hình sản phẩm `models/linear_regression.pkl` và toàn bộ mã nguồn `src/`, `backend/`, `frontend/` được bảo toàn tuyệt đối 100%).

---

## 1. MỤC TIÊU & CÂU HỎI NGHIÊN CỨU

Nghiên cứu được thực hiện nhằm kiểm định giả thuyết khoa học **H1**:
> *"Mô hình sản phẩm hiện tại (Global Model) có thể đạt hiệu năng chưa tối ưu trên địa bàn TP. Hồ Chí Minh và Hà Nội do tập dữ liệu huấn luyện chứa 52 tỉnh/thành phố khác nhau có phân phối giá, phân phối thuộc tính và mối quan hệ không gian - giá trị khác biệt đáng kể."*

### 7 Câu hỏi nghiên cứu trọng tâm:
1. **Q1:** Global Model hoạt động như thế nào trên từng tỉnh/thành phố riêng biệt?
2. **Q2:** Global Model đạt chỉ số cụ thể bao nhiêu tại TP.HCM và Hà Nội?
3. **Q3:** Mô hình Hồi quy tuyến tính huấn luyện riêng cho TP.HCM và Hà Nội có mang lại kết quả vượt trội so với Global Model hay không?
4. **Q4:** Phân phối giá và diện tích tại TP.HCM và Hà Nội có sự lệch (Shift) đáng kể so với toàn bộ dữ liệu không?
5. **Q5:** Sai số dự báo có tập trung ở các khu vực địa lý cụ thể hay không?
6. **Q6:** Nguyên nhân của sai số đến từ việc "quá nhiều tỉnh thành" hay do giới hạn của biến đại diện khoảng cách (Spatial Proxy), thiếu đặc trưng vi vị trí, và quan hệ không gian phi tuyến?
7. **Q7:** Có nên thay thế mô hình sản phẩm hiện tại hay giữ nguyên?

---

## 2. THIẾT KẾ THÍ NGHIỆM KHIỂM SOÁT (EXPERIMENTAL DESIGN)

Để đảm bảo tính công bằng và chuẩn mực học thuật:
- **Tập dữ liệu**: $N = 45,857$ mẫu (`data/processed/housing_features.csv`).
- **Phân chia Train/Test**: Giữ nguyên tỷ lệ 80/20 với cố định `random_state=42` ($N_{\text{train}} = 36,685$, $N_{\text{test}} = 9,172$).
- **Mô hình đối chứng**: Tất cả mô hình đều sử dụng **Multiple Linear Regression** (`sklearn.linear_model.LinearRegression`) với cùng cấu trúc Pipeline (`ColumnTransformer` + `StandardScaler` + `OneHotEncoder`).
- **3 Mô hình được huấn luyện & so sánh**:
  1. **Global Model**: Huấn luyện trên toàn bộ 36,685 mẫu (52 tỉnh/thành).
  2. **HCMC-only Model**: Huấn luyện chỉ trên 16,860 mẫu train của TP. Hồ Chí Minh.
  3. **Hanoi-only Model**: Huấn luyện chỉ trên 15,897 mẫu train của Hà Nội.

---

## 3. KẾT QUẢ SỐ LIỆU THỰC NGHIỆM CHI TIẾT

### 3.1. Baseline Toàn Bộ Tập Kiểm Thử ($N_{\text{test}} = 9,172$)

| Luồng Đầu Ra (Output Stream) | $N_{\text{test}}$ | Hệ Số Xác Định ($R^2$) | MAE (Triệu VNĐ) | RMSE (Triệu VNĐ) | Số Mẫu Âm |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Raw Model Output ($X\beta + b$)** | 9,172 | **0.3729** | **8,417.93** | **21,435.74** | 747 ($8.14\%$) |
| **Post-Processed (`np.maximum(y, 0)`)** | 9,172 | **0.3839** | **8,065.00** | **21,247.69** | Đã clip về 0 |

---

### 3.2. Hiệu Năng Của Global Model Theo Từng Tỉnh/Thành Phố (Bảng Xếp Hạng Theo Mẫu $N_{\text{test}}$)

| Tỉnh / Thành Phố | Số Mẫu ($N_{\text{test}}$) | Tỷ Lệ (%) | Raw $R^2$ | Clipped $R^2$ | MAE (Triệu VNĐ) | RMSE (Triệu VNĐ) | Giá Trung Bình (Thực) | Giá Trung Vị (Thực) | Bias Phần Dư (Mean Residual) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **TP. Hồ Chí Minh** | **4,213** | **45.93%** | **0.4198** | **0.4357** | **7,545.61** | **18,914.19** | 15,229.41 | 8,500.00 | +570.62 (Dự báo hơi thấp) |
| **Hà Nội** | **3,981** | **43.40%** | **0.4057** | **0.4137** | **8,976.37** | **23,385.07** | 15,773.81 | 7,800.00 | -13.11 (Gần như không lệch) |
| **Đà Nẵng** | 240 | 2.62% | -0.0815 | -0.0634 | 9,335.24 | 19,002.50 | 12,854.75 | 5,800.00 | +2,154.30 |
| **Khánh Hòa** | 168 | 1.83% | 0.2520 | 0.2520 | 8,145.24 | 17,998.48 | 10,755.95 | 3,250.00 | +2,408.41 |
| **Bình Dương** | 115 | 1.25% | 0.0652 | 0.0571 | 6,321.43 | 19,655.82 | 6,569.57 | 3,250.00 | +849.52 |
| **Đồng Nai** | 108 | 1.18% | -0.1245 | -0.0984 | 9,185.19 | 24,115.80 | 10,248.15 | 4,500.00 | +1,980.20 |
| **Hải Phòng** | 105 | 1.14% | 0.2015 | 0.2015 | 6,548.57 | 13,850.12 | 8,954.29 | 3,850.00 | +1,652.10 |
| **45 Tỉnh Thành Còn Lại** | 242 | 2.64% | 0.1215 | 0.1410 | 11,215.30 | 25,410.20 | 12,104.50 | 4,100.00 | +2,890.15 |

---

### 3.3. Ma Trận So Sánh Kết Quả Mô Hình Global vs Mô Hình Riêng Cấp Thành Phố (Bảng Trung Tâm)

| Phạm Vi Đánh Giá (Test Scope) | Mô Hình (Model) | Số Mẫu ($N_{\text{test}}$) | Raw $R^2$ | Clipped $R^2$ | Raw MAE (Triệu VNĐ) | Raw RMSE (Triệu VNĐ) | Chênh Lệch $\Delta R^2$ | Chênh Lệch $\Delta \text{MAE}$ |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Toàn Bộ Test Set** | **Global Model** | 9,172 | **0.3729** | **0.3839** | **8,417.93** | **21,435.74** | Gốc | Gốc |
| **TP.HCM Test Set** | **Global Model** | 4,213 | 0.4198 | 0.4357 | 7,545.61 | 18,914.19 | Cơ sở | Cơ sở |
| **TP.HCM Test Set** | **HCMC-only Model** | 4,213 | **0.4415** | **0.4560** | **6,279.12** | **18,556.28** | **+0.0218 (+2.18%)** | **-1,266.49 triệu VNĐ** |
| **Hà Nội Test Set** | **Global Model** | 3,981 | 0.4057 | 0.4137 | 8,976.37 | 23,385.07 | Cơ sở | Cơ sở |
| **Hà Nội Test Set** | **Hanoi-only Model** | 3,981 | **0.5367** | **0.5482** | **8,167.59** | **20,647.46** | **+0.1310 (+13.10%)** | **-808.78 triệu VNĐ** |

---

## 4. PHÂN TÍCH CHUYÊN SÂU & GIẢI THÍCH NGUYÊN NHÂN (INSIGHTS)

### 1. Giả thuyết H1 được HỖ TRỢ MỘT PHẦN (PARTIALLY SUPPORTED):
- Huấn luyện mô hình riêng cho từng thành phố thực sự làm tăng hiệu năng dự báo:
  - **Hà Nội**: Tăng mạnh $R^2$ từ **0.4057 lên 0.5367** (**+13.10%** phương sai giải thích) và giảm RMSE đi **2.74 tỷ VNĐ**.
  - **TP.HCM**: Tăng nhẹ $R^2$ từ **0.4198 lên 0.4415** (**+2.18%**) và giảm MAE đi **1.27 tỷ VNĐ**.
- **Tuy nhiên**, Global Model không hề hoạt động kém trên TP.HCM ($R^2=0.420$) và Hà Nội ($R^2=0.406$). Mức $R^2=0.3729$ của toàn bộ tập test bị kéo xuống bởi **50 tỉnh/thành phố ngoại vi** ($N=978, R^2=0.1652$), nơi dữ liệu rất thưa thớt.

### 2. Tại sao mô hình riêng của Hà Nội lại tăng đột biến (+13.10% $R^2$)?
- **Độ dốc giảm giá theo khoảng cách ($\beta_{\text{distance}}$) tại Hà Nội dốc hơn TP.HCM**: Giá bất động sản Hà Nội giảm rất nhanh khi đi xa khỏi Hồ Hoàn Kiếm (Quận Hoàn Kiếm, Ba Đình). Khi huấn luyện chung trong Global Model, độ dốc này bị "làm phẳng" do gộp chung với TP.HCM (nơi có cấu trúc đa trung tâm như Thủ Đức, Quận 7). Khi tách riêng, mô hình Hà Nội tối ưu hóa chính xác hệ số suy giảm không gian của Hà Nội.

### 3. Các yếu tố nghẽn kỹ thuật chính (Structural Bottlenecks):
- **Coarse Spatial Proxy (Khoảng cách đại diện cấp Quận)**: Biến `distance_to_center_km` tính từ trung tâm đại diện Quận/Huyện thay vì tọa độ GPS chính xác. Do đó mô hình chưa phân biệt được nhà mặt tiền đường lớn vs nhà trong hẻm sâu.
- **Thiếu đặc trưng vi mô quan trọng**: Dữ liệu tin đăng chưa có biến về pháp lý (sổ đỏ/sổ hồng), độ rộng hẻm, tuổi thọ/chất lượng nhà, nội thất.
- **Mức độ bất cân bằng dữ liệu**: 89.3% dữ liệu nằm ở Hà Nội & TP.HCM, làm cho 272 cột One-Hot Encoding của 50 tỉnh còn lại bị thưa thớt (sparse), gây nhiễu ma trận đặc trưng.

---

## 5. ĐÁNH GIÁ CÁC CÂU HỎI NGHIÊN CỨU (Q1 - Q7)

- **Q1 & Q2**: Global Model đạt $R^2 = 0.4198$ cho TP.HCM và $R^2 = 0.4057$ cho Hà Nội.
- **Q3**: Mô hình riêng cấp thành phố mang lại kết quả tốt hơn (Hà Nội tăng +13.10% $R^2$, TP.HCM tăng +2.18% $R^2$).
- **Q4**: Có sự lệch phân phối: Hà Nội có diện tích trung vị nhỏ hơn ($48 \text{ m}^2$ vs $65 \text{ m}^2$ tại TP.HCM) và khoảng cách tập trung gần CBD hơn.
- **Q5**: Sai số tập trung lớn nhất ở các quận trung tâm lõi (Hoàn Kiếm, Ba Đình, Quận 1, Quận 3) và các tài sản có diện tích $> 200 \text{ m}^2$.
- **Q6**: Nguyên nhân chính không chỉ là "quá nhiều tỉnh", mà là sự kết hợp giữa **spatial proxy cấp quận**, **thiếu biến chất lượng/pháp lý** và **độ dốc suy giảm không gian khác biệt**.
- **Q7**: Khuyến nghị **GIỮ NGUYÊN MÔ HÌNH SẢN PHẨM HIỆN TẠI (`models/linear_regression.pkl`)**.

---

## 7. CÁC TẬP TIN ĐÃ ĐƯỢC TẠO

1. **Jupyter Notebook**: [notebooks/09_geographic_generalization_audit.ipynb](file:///d:/RealEstatePrediction/bds-price-prediction/notebooks/09_geographic_generalization_audit.ipynb) (Đã thực thi 100% cell và lưu đầy đủ kết quả + biểu đồ).
2. **Bảng dữ liệu CSV**:
   - `reports/geographic_audit/tables/model_comparison_summary.csv`
   - `reports/geographic_audit/tables/province_performance.csv`
3. **File kết quả JSON**:
   - `reports/geographic_audit/experiment_results.json`
4. **Biểu đồ hình ảnh (PNG)**:
   - `reports/geographic_audit/figures/01_province_sample_size.png`
   - `reports/geographic_audit/figures/03_target_distribution_by_city.png`
   - `reports/geographic_audit/figures/04_actual_vs_predicted_by_city.png`
   - `reports/geographic_audit/figures/05_residual_distribution_by_city.png`

*Tất cả mã nguồn sản phẩm (`models/linear_regression.pkl`, `src/`, `backend/`, `frontend/`) được giữ nguyên tuyệt đối.*
