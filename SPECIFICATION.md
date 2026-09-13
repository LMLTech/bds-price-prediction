# REAL ESTATE PRICE PREDICTION

## Project Handoff Specification

---

# 1. TỔNG QUAN PROJECT

## 1.1. Tên project

**Real Estate Price Prediction**

Tên thư mục/code project:

```text
RealEstatePrediction
```

Tên đề tài học thuật có thể sử dụng trong báo cáo:

> **Real Estate Price Prediction Based on Property and Location Features Using Linear Regression**

Tên tiếng Việt:

> **Dự báo giá bất động sản dựa trên các đặc điểm tài sản và vị trí bằng phương pháp hồi quy tuyến tính**

---

# 2. BỐI CẢNH VÀ YÊU CẦU ĐỀ TÀI

Đây là project Machine Learning với yêu cầu từ giảng viên:

> Dự báo giá bất động sản dựa trên các đặc điểm như diện tích, số phòng, vị trí, khoảng cách đến trung tâm để dự báo giá bán. Sử dụng kỹ thuật hồi quy tuyến tính. Sinh viên cần thể hiện khả năng xử lý dữ liệu thực tế và đánh giá sai số của mô hình.

Do đó project phải tập trung vào:

1. Xử lý dữ liệu bất động sản thực tế tại Việt Nam.
2. Phân tích dữ liệu.
3. Làm sạch dữ liệu.
4. Xây dựng các đặc trưng phù hợp.
5. Sử dụng Linear Regression.
6. Dự báo giá bất động sản.
7. Đánh giá sai số.
8. Phân tích nguyên nhân mô hình dự đoán sai.
9. Đưa ra kết luận và hạn chế của mô hình.

**Không nên biến project thành một hệ thống AI quá phức tạp.**

Trọng tâm vẫn là:

```text
Real-world Data
        ↓
Data Understanding
        ↓
Data Cleaning
        ↓
EDA
        ↓
Feature Engineering
        ↓
Linear Regression
        ↓
Prediction
        ↓
Evaluation
        ↓
Error Analysis
        ↓
Conclusion
```

---

# 3. DATASET ĐƯỢC CHỌN

Dataset hiện tại được ưu tiên sử dụng là dataset về bất động sản Việt Nam với khoảng:

> **69.000 records**

Dataset bao gồm dữ liệu mua/bán và cho thuê được thu thập từ nhiều khu vực tại Việt Nam.

Dataset chứa các thông tin:

* Diện tích
* Số phòng ngủ
* Số phòng tắm
* Số tầng
* Frontage
* Location
* Giá
* Thời gian tin đăng
* ID
* URL
* Title

Dataset phù hợp với project vì:

* Là dữ liệu bất động sản Việt Nam.
* Số lượng records lớn.
* Có cả numerical và categorical features.
* Có location.
* Có nhiều đặc trưng liên quan trực tiếp đến giá.
* Có dữ liệu thực tế nên có thể thực hiện Data Cleaning.
* Có outlier/missing/inconsistent data để phân tích.
* Phù hợp với bài toán Regression.
* Phù hợp để sử dụng Linear Regression.

---

# 4. DATASET GLOSSARY

Dataset có các attributes chính:

## 4.1. ID

Unique identifier của listing.

Ví dụ:

```text
ID = 123456
```

Vai trò:

* Dùng để định danh record.
* Không dùng làm feature để dự đoán giá.

=> **DROP khỏi model.**

---

# 4.2. Detail URL

URL dẫn đến trang chi tiết bất động sản.

Ví dụ:

```text
https://...
```

Vai trò:

* Dùng để truy xuất/kiểm tra dữ liệu nếu cần.
* Không có ý nghĩa trực tiếp đối với Linear Regression.

=> **DROP khỏi model.**

---

# 4.3. Title

Tiêu đề của tin đăng.

Ví dụ:

```text
Bán nhà mặt tiền Quận 1
Nhà đẹp 3 tầng gần trung tâm
```

Title có thể chứa thông tin hữu ích nhưng việc xử lý NLP/text không nằm trong phạm vi chính của project.

=> **Không đưa vào Linear Regression ở phiên bản đầu tiên.**

Có thể đề cập trong phần Future Work rằng Title có thể được xử lý bằng NLP để cải thiện model.

---

# 4.4. Location

Thông tin vị trí bất động sản.

Có thể bao gồm:

```text
Ward
District
Province
```

Đây là một trong những feature quan trọng nhất.

Location cần được kiểm tra dữ liệu thực tế trước khi quyết định cách encoding.

Ví dụ:

```text
District 1
District 7
Binh Thanh
Thu Duc
...
```

Có thể sử dụng:

* One-Hot Encoding
* hoặc tách Location thành Province/District/Ward nếu dữ liệu thực tế cho phép.

---

# 4.5. Timeline (Hours)

Số giờ listing đã được đăng tính đến ngày:

> December 29, 2025

Ví dụ:

```text
10
120
500
3000
```

Đây là feature có thể dùng để phân tích.

Tuy nhiên **không mặc định đưa vào model**.

Cần kiểm tra:

```text
Timeline ↔ Price
```

và đánh giá xem nó có khả năng giải thích giá hay không.

Nếu không hữu ích, có thể loại khỏi model.

---

# 4.6. Area (m2)

Diện tích bất động sản.

Đây là một feature quan trọng.

Ví dụ:

```text
Area = 80 m2
Area = 120 m2
```

=> **Ưu tiên giữ lại.**

---

# 4.7. Bedrooms

Số phòng ngủ.

Ví dụ:

```text
Bedrooms = 2
Bedrooms = 3
Bedrooms = 4
```

=> **Ưu tiên giữ lại.**

---

# 4.8. Bathrooms

Số phòng tắm.

Ví dụ:

```text
Bathrooms = 2
Bathrooms = 3
```

=> Có thể sử dụng làm feature.

---

# 4.9. Floors

Số tầng.

Ví dụ:

```text
Floors = 1
Floors = 3
Floors = 5
```

=> Có thể sử dụng làm feature.

---

# 4.10. Frontage

Thông tin về việc bất động sản có nằm ở mặt tiền hay không.

Đây là categorical/binary feature.

Ví dụ:

```text
Frontage = Yes
Frontage = No
```

Có thể encode thành:

```text
Yes → 1
No  → 0
```

Nhưng phải kiểm tra format thực tế trước khi preprocessing.

---

# 4.11. Price (million VND)

Đây là:

> **TARGET VARIABLE**

Giá bán bất động sản.

Đơn vị:

```text
million VND
```

Ví dụ:

```text
Price = 5000
```

có nghĩa:

```text
5,000 million VND
= 5 billion VND
```

Model sẽ dự đoán:

```text
Input features
      ↓
Linear Regression
      ↓
Predicted Price
```

---

# 5. TARGET VARIABLE

Target:

```text
Price
```

Đơn vị:

```text
million VND
```

Không được sử dụng Price để tạo feature theo cách gây data leakage.

Ví dụ không được tạo:

```text
Price_per_m2 = Price / Area
```

rồi dùng `Price_per_m2` để dự đoán `Price`.

Vì:

```text
Price_per_m2
```

đã chứa chính target Price.

Feature này chỉ có thể sử dụng trong **EDA/analysis**, không dùng làm input feature cho model dự đoán Price.

---

# 6. FEATURES DỰ KIẾN

Initial feature set:

```text
Area
Bedrooms
Bathrooms
Floors
Frontage
Location
```

Có thể bổ sung:

```text
Distance_to_Center
Timeline
```

sau khi phân tích dữ liệu.

---

# 7. DISTANCE TO CENTER

Đây là một yêu cầu quan trọng từ đề bài.

Dataset hiện tại **không cung cấp trực tiếp một cột Distance_to_Center**.

Vì vậy cần xử lý cẩn thận.

## Option A — Không tạo Distance_to_Center

Sử dụng Location để đại diện cho yếu tố vị trí:

```text
Location
   ↓
Encoding
   ↓
Linear Regression
```

Trong báo cáo giải thích:

> Dataset không cung cấp trực tiếp khoảng cách đến trung tâm, do đó nghiên cứu sử dụng thông tin khu vực (ward/district/province) để đại diện cho yếu tố vị trí.

---

## Option B — Tạo Distance_to_Center

Nếu Location trong dataset đủ chính xác, có thể xây dựng feature:

```text
Location
    ↓
Geocoding
    ↓
Latitude / Longitude
    ↓
Distance to selected city center
    ↓
Distance_to_Center
```

Ví dụ:

```text
District 1 → x km
District 7 → y km
Thu Duc → z km
```

Tuy nhiên **không được tự ý giả định khoảng cách**.

Phải kiểm tra dataset thực tế trước.

Nếu project bao gồm nhiều tỉnh/thành phố, cần xác định rõ:

* "center" là trung tâm nào?
* Có phải trung tâm của province không?
* Có phải trung tâm của thành phố không?
* Có một center chung hay mỗi province có center riêng?

Nếu không thể xác định chính xác thì **không tạo feature giả**.

---

# 8. DATA PROCESSING PIPELINE

Pipeline chính:

```text
RAW DATA
   ↓
Data Understanding
   ↓
Data Cleaning
   ↓
Missing Value Handling
   ↓
Duplicate Removal
   ↓
Invalid Value Handling
   ↓
Outlier Analysis
   ↓
EDA
   ↓
Feature Engineering
   ↓
Categorical Encoding
   ↓
Train/Test Split
   ↓
Linear Regression
   ↓
Prediction
   ↓
Evaluation
   ↓
Error Analysis
   ↓
Conclusion
```

---

# 9. STEP 1 — DATA UNDERSTANDING

Notebook:

```text
notebooks/01_data_understanding.ipynb
```

Mục tiêu:

Hiểu dataset trước khi xử lý.

Cần thực hiện:

```python
df.shape
df.head()
df.tail()
df.info()
df.describe()
df.columns
```

Kiểm tra:

### Dataset size

```text
Number of rows
Number of columns
```

### Data types

Phân loại:

```text
Numerical
Categorical
Text
Identifier
Target
```

### Missing values

```python
df.isnull().sum()
```

Tính:

```text
missing count
missing percentage
```

### Duplicate

```python
df.duplicated().sum()
```

### Unique values

Đối với categorical:

```python
df["Location"].nunique()
df["Frontage"].unique()
```

### Target distribution

Kiểm tra:

```text
Price min
Price max
Price mean
Price median
Price std
```

---

# 10. STEP 2 — DATA CLEANING

Notebook:

```text
notebooks/02_data_cleaning.ipynb
```

Mục tiêu:

Biến dữ liệu raw thành dữ liệu có thể sử dụng cho ML.

---

## 10.1. Remove duplicate

Kiểm tra duplicate dựa trên:

```text
ID
```

hoặc toàn bộ row tùy cấu trúc thực tế.

Không được tự động xóa trước khi kiểm tra.

---

# 10.2. Missing Values

Kiểm tra missing từng cột.

Ví dụ:

```text
Area
Bedrooms
Bathrooms
Floors
Frontage
Location
Price
```

Chiến lược:

### Numerical

Có thể sử dụng:

```text
Median
```

thay vì mean nếu dữ liệu có outlier mạnh.

Ví dụ:

```text
Area
Bedrooms
Bathrooms
Floors
Timeline
```

### Categorical

Có thể sử dụng:

```text
Mode
```

hoặc:

```text
Unknown
```

Tùy tỷ lệ missing.

### Price

Nếu target Price bị missing:

=> **Không nên impute target một cách tùy tiện.**

Thông thường:

```text
Price == missing
        ↓
Remove row
```

---

# 10.3. Invalid Values

Phải kiểm tra các giá trị vô lý.

Ví dụ:

```text
Area <= 0
Bedrooms < 0
Bathrooms < 0
Floors <= 0
Price <= 0
```

Các giá trị này cần được xử lý.

---

# 10.4. Outliers

Outlier là phần quan trọng của project.

Có thể sử dụng:

```text
IQR
Boxplot
Z-score
```

Đặc biệt kiểm tra:

```text
Area
Price
Bedrooms
Bathrooms
Floors
```

Không được mặc định:

```text
Outlier = remove
```

Vì bất động sản thực tế có thể thực sự có những căn:

```text
giá rất cao
diện tích rất lớn
```

Cần phân biệt:

```text
True high-value property
```

với:

```text
Data entry error
```

Ví dụ:

```text
Area = 5000 m2
Price = 1000000000
```

cần kiểm tra xem đó là dữ liệu thật hay lỗi.

---

# 11. STEP 3 — EDA

Notebook:

```text
notebooks/03_eda.ipynb
```

Mục tiêu:

Tìm hiểu mối quan hệ giữa các feature và Price.

---

## 11.1. Distribution

Vẽ histogram:

```text
Price
Area
Bedrooms
Bathrooms
Floors
```

---

## 11.2. Area vs Price

Biểu đồ:

```text
X = Area
Y = Price
```

Mục tiêu:

Kiểm tra:

> Diện tích càng lớn thì giá có xu hướng tăng không?

---

## 11.3. Location vs Price

Phân tích giá theo:

```text
Province
District
Ward
```

Nếu số lượng category quá lớn thì chọn:

```text
Top N locations
```

để visualization.

---

## 11.4. Bedrooms vs Price

Kiểm tra:

```text
Bedrooms ↔ Price
```

---

## 11.5. Bathrooms vs Price

Kiểm tra:

```text
Bathrooms ↔ Price
```

---

## 11.6. Floors vs Price

Kiểm tra:

```text
Floors ↔ Price
```

---

## 11.7. Frontage vs Price

So sánh:

```text
Frontage = Yes
Frontage = No
```

---

## 11.8. Correlation Matrix

Đối với numerical features:

```text
Area
Bedrooms
Bathrooms
Floors
Timeline
Price
```

Tạo correlation matrix.

Mục tiêu:

Xác định feature nào có correlation với Price.

---

# 12. STEP 4 — FEATURE ENGINEERING

Notebook:

```text
notebooks/04_feature_engineering.ipynb
```

Feature engineering phải có lý do rõ ràng.

Không tạo feature chỉ để làm project phức tạp.

---

## 12.1. Location Encoding

Location là categorical feature.

Có thể sử dụng:

```text
One-Hot Encoding
```

Ví dụ:

```text
District 1
District 7
District 3
Thu Duc
```

thành:

```text
Location_District1
Location_District7
Location_District3
Location_ThuDuc
```

Nếu dataset có:

```text
Province
District
Ward
```

thì có thể xử lý riêng.

---

# 13. FEATURE ENGINEERING CÓ THỂ CÓ

Các feature tiềm năng:

```text
Distance_to_Center
Property_Age
```

Nhưng:

**Không được tạo Property_Age nếu dataset không có Year_Built hoặc thông tin tương đương.**

Không được tự bịa dữ liệu.

---

# 14. PRICE PER M2

Có thể tạo:

```text
Price_per_m2 = Price / Area
```

nhưng chỉ dùng cho:

* EDA
* Visualization
* Market analysis

**Không dùng làm feature input cho model Price Prediction.**

Lý do:

```text
Price_per_m2 = Price / Area
```

nên nó đã chứa target Price.

Nếu đưa vào model sẽ gây:

> Data Leakage

---

# 15. DATA LEAKAGE

Đây là yêu cầu quan trọng.

Không được để thông tin từ test set ảnh hưởng đến training.

Ví dụ:

Không được:

```text
Impute toàn bộ dataset
       ↓
Train/Test Split
```

mà nên:

```text
Train/Test Split
      ↓
Fit preprocessing trên Train
      ↓
Transform Train
      ↓
Transform Test
```

Đặc biệt với:

* Imputation
* Scaling
* Encoding có học từ data

Nên ưu tiên sử dụng:

```text
Pipeline
ColumnTransformer
```

của scikit-learn.

---

# 16. TRAIN / TEST SPLIT

Ví dụ:

```text
80% Train
20% Test
```

Sử dụng:

```python
train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)
```

`random_state=42` để kết quả có thể reproduce.

Test set được xem như:

> dữ liệu mà model chưa từng nhìn thấy.

---

# 17. MODEL

Model chính:

> **Multiple Linear Regression**

Sử dụng:

```python
from sklearn.linear_model import LinearRegression
```

Mô hình có dạng:

```text
Price =
β0
+ β1 × Area
+ β2 × Bedrooms
+ β3 × Bathrooms
+ β4 × Floors
+ β5 × Frontage
+ β6 × Location
+ ...
```

Trong đó:

```text
β0 = intercept
β1...βn = coefficients
```

Mục tiêu:

> Tìm coefficients sao cho sai số dự đoán trên training data được tối thiểu hóa.

---

# 18. MODEL TRAINING

Notebook:

```text
notebooks/05_linear_regression.ipynb
```

Flow:

```text
Processed Dataset
       ↓
Select X
       ↓
Select y = Price
       ↓
Train/Test Split
       ↓
Preprocessing
       ↓
Linear Regression
       ↓
Fit
```

Sau khi train:

```python
model.fit(X_train, y_train)
```

---

# 19. MODEL OUTPUT

Model phải tạo:

```text
y_pred
```

Ví dụ:

```text
Actual Price     Predicted Price
5000             4700
8000             8500
12000            11000
```

Đơn vị:

```text
million VND
```

---

# 20. MODEL EVALUATION

Notebook:

```text
notebooks/06_evaluation.ipynb
```

Bắt buộc sử dụng:

## MAE

Mean Absolute Error.

Công thức:

```text
MAE = mean(|y_actual - y_pred|)
```

Ý nghĩa:

> Trung bình mô hình dự đoán lệch bao nhiêu triệu VND.

Ví dụ:

```text
MAE = 800
```

có thể diễn giải:

> Trung bình dự đoán của model lệch khoảng 800 triệu VND so với giá thực tế.

---

# 21. RMSE

Root Mean Squared Error.

Công thức:

```text
RMSE = sqrt(mean((y_actual - y_pred)^2))
```

RMSE nhạy hơn với những prediction error lớn.

Ví dụ:

Nếu model dự đoán sai cực lớn một số căn:

```text
Actual = 30 billion
Predicted = 10 billion
```

RMSE sẽ phản ánh những sai số lớn này mạnh hơn MAE.

---

# 22. R²

Coefficient of Determination.

Ý nghĩa:

> Mô hình giải thích được bao nhiêu phần biến thiên của giá dựa trên các feature được sử dụng.

Ví dụ:

```text
R² = 0.70
```

có thể diễn giải:

> Các biến trong model giải thích khoảng 70% mức biến thiên của Price trên tập dữ liệu được đánh giá.

**Không được gọi R² là "accuracy 70%".**

---

# 23. METRICS BẮT BUỘC

Báo cáo cuối cùng nên có:

```text
MAE
RMSE
R²
```

Có thể bổ sung:

```text
MAPE
```

nhưng không bắt buộc.

MAPE cần cẩn thận nếu Price có giá trị bằng hoặc gần 0.

---

# 24. ERROR ANALYSIS

Đây là phần quan trọng vì đề bài yêu cầu:

> "đánh giá sai mô hình."

Không chỉ đưa:

```text
MAE = ...
RMSE = ...
R² = ...
```

mà phải phân tích model sai ở đâu.

---

## 24.1. Actual vs Predicted

Vẽ:

```text
Actual Price
vs
Predicted Price
```

Nếu model tốt, các điểm sẽ nằm tương đối gần đường:

```text
y = x
```

---

# 25. RESIDUAL ANALYSIS

Residual:

```text
Residual = Actual - Predicted
```

Phân tích:

```text
Residual distribution
```

và:

```text
Residual vs Predicted
```

Mục tiêu:

Kiểm tra model có pattern sai lệch hay không.

---

# 26. TOP PREDICTION ERRORS

Tìm những record model dự đoán sai nhiều nhất.

Ví dụ:

```text
Actual     Predicted     Error
30,000     10,000        20,000
25,000     12,000        13,000
...
```

Sau đó kiểm tra:

```text
Location
Area
Bedrooms
Bathrooms
Floors
Frontage
```

để tìm nguyên nhân.

---

# 27. CÁC NGUYÊN NHÂN CÓ THỂ KHIẾN MODEL SAI

Ví dụ:

### 1. Location quá phức tạp

Hai căn cùng diện tích:

```text
100 m²
```

nhưng:

```text
District 1
```

và:

```text
ngoại thành
```

có thể có giá rất khác.

---

### 2. Missing important features

Dataset không có đầy đủ các yếu tố:

```text
View
Condition
Interior quality
Legal status
Exact distance to center
Nearby amenities
Road quality
Project reputation
...
```

Linear Regression không thể biết các yếu tố này.

---

### 3. Non-linear relationship

Quan hệ:

```text
Area → Price
```

có thể không hoàn toàn tuyến tính.

Ví dụ:

```text
Area tăng 20%
```

không nhất thiết:

```text
Price tăng 20%
```

---

### 4. Outliers

Bất động sản cao cấp có thể có:

```text
Price rất cao
```

so với phần lớn dataset.

Linear Regression dễ bị ảnh hưởng.

---

# 28. LIMITATIONS

Báo cáo cần thừa nhận:

Model chỉ sử dụng một tập feature giới hạn.

Ví dụ:

```text
Area
Bedrooms
Bathrooms
Floors
Frontage
Location
```

Trong thực tế giá bất động sản còn phụ thuộc:

```text
Legal status
Interior
Road width
View
Neighborhood
Infrastructure
Distance to school
Distance to metro
Distance to CBD
Developer
Project
Economic conditions
Time
...
```

Do đó Linear Regression có thể chưa đạt độ chính xác cao.

---

# 29. FUTURE WORK

Có thể đề xuất:

### Feature Engineering tốt hơn

```text
Distance to CBD
Price per m2 analysis
Location hierarchy
Property age
Nearby amenities
```

---

### Advanced models

Sau khi hoàn thành Linear Regression, có thể thử:

```text
Decision Tree
Random Forest
Gradient Boosting
XGBoost
CatBoost
```

Mục đích:

> So sánh Linear Regression với các mô hình phi tuyến.

**Tuy nhiên model chính của project vẫn phải là Linear Regression theo yêu cầu của giảng viên.**

---

# 30. PROJECT STRUCTURE

Cấu trúc được thống nhất:

```text
RealEstatePrediction/
│
├── data/
│   ├── raw/
│   │   └── vietnam_housing.csv
│   │
│   └── processed/
│       └── housing_clean.csv
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_feature_engineering.ipynb
│   ├── 05_linear_regression.ipynb
│   └── 06_evaluation.ipynb
│
├── src/
│   ├── __init__.py
│   │
│   ├── preprocessing.py
│   ├── features.py
│   ├── train.py
│   ├── evaluate.py
│   └── predict.py
│
├── models/
│   └── linear_regression.pkl
│
├── reports/
│   └── figures/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 31. VAI TRÒ CỦA SRC

## `src/preprocessing.py`

Chứa các hàm xử lý dữ liệu:

```text
load_data()
check_missing_values()
remove_duplicates()
handle_missing_values()
handle_invalid_values()
```

Không nên viết toàn bộ preprocessing trực tiếp trong notebook nếu có thể tái sử dụng.

---

## `src/features.py`

Chứa:

```text
create_distance_to_center()
create_other_features()
encode_features()
```

Chỉ implement những feature thực sự cần thiết.

---

## `src/train.py`

Chịu trách nhiệm:

```text
load processed data
↓
select features
↓
train/test split
↓
build preprocessing pipeline
↓
train Linear Regression
↓
save model
```

Model lưu:

```text
models/linear_regression.pkl
```

---

## `src/evaluate.py`

Chịu trách nhiệm:

```text
MAE
RMSE
R²
Residual analysis
```

---

## `src/predict.py`

Dùng model đã train để dự đoán giá cho dữ liệu mới.

Ví dụ:

```text
Area = 80
Bedrooms = 3
Bathrooms = 2
Floors = 3
Location = District 7
Frontage = Yes
```

→ Model trả về:

```text
Predicted Price = XXXX million VND
```

---

# 32. NOTEBOOK VÀ SRC KHÁC NHAU NHƯ THẾ NÀO?

Notebook dùng để:

> **Khám phá + phân tích + visualization + trình bày quá trình ML.**

`src/` dùng để:

> **Chứa code có thể tái sử dụng và chạy lại.**

Không nên biến notebook thành một file code khổng lồ.

---

# 33. REQUIREMENTS

Ban đầu có thể sử dụng:

```text
pandas
numpy
scikit-learn
matplotlib
seaborn
jupyter
joblib
```

`requirements.txt`:

```text
pandas
numpy
scikit-learn
matplotlib
seaborn
jupyter
joblib
```

Nếu sau này có thêm geocoding/map hoặc công cụ khác thì mới bổ sung dependency.

---

# 34. GIT STRUCTURE

Repository:

```text
RealEstatePrediction
```

Branch chính:

```text
main
```

Có thể chia branch:

```text
feature/data-understanding
feature/data-cleaning
feature/eda
feature/feature-engineering
feature/model
feature/evaluation
```

Không nên tất cả thành viên cùng sửa trực tiếp `main`.

---

# 35. GITIGNORE

Không commit:

```text
.venv/
__pycache__/
.ipynb_checkpoints/
*.pyc
.env
```

Có thể cân nhắc không commit dataset raw nếu file quá lớn hoặc license/source yêu cầu.

---

# 36. WORKFLOW LÀM PROJECT

Đội code phải làm theo thứ tự:

```text
PHASE 1
Data Understanding
        ↓
PHASE 2
Data Cleaning
        ↓
PHASE 3
EDA
        ↓
PHASE 4
Feature Engineering
        ↓
PHASE 5
Train/Test Split
        ↓
PHASE 6
Linear Regression
        ↓
PHASE 7
Evaluation
        ↓
PHASE 8
Error Analysis
        ↓
PHASE 9
Report
```

**Không nhảy thẳng vào training model.**

---

# 37. QUY TẮC QUAN TRỌNG CHO TEAM CODE

## Rule 1

Không tự ý đổi dataset nếu chưa đánh giá dataset hiện tại.

---

## Rule 2

Không tự ý xóa outlier.

Phải chứng minh:

```text
Why is this an outlier?
Why should it be removed?
```

---

## Rule 3

Không tự ý tạo feature dựa trên Target.

Tránh:

```text
Data Leakage
```

---

## Rule 4

Không gọi:

```text
R² = Accuracy
```

R² không phải accuracy percentage.

---

## Rule 5

Không chỉ báo metrics.

Phải phân tích:

```text
Why model performs this way?
Where does model fail?
Why does it fail?
```

---

## Rule 6

Không dùng các model phức tạp để thay thế Linear Regression.

Nếu thử Random Forest/XGBoost/CatBoost thì chỉ dùng ở:

> Future Work / Comparison

Model chính:

```text
Multiple Linear Regression
```

---

# 38. OUTPUT CUỐI CÙNG CẦN CÓ

Project hoàn chỉnh cần tạo được:

### Dataset

```text
Raw dataset
Processed dataset
```

### Code

```text
Data preprocessing
Feature engineering
Training
Prediction
Evaluation
```

### Model

```text
linear_regression.pkl
```

### Visualizations

Ít nhất nên có:

```text
Price distribution
Area vs Price
Correlation matrix
Location vs Price
Actual vs Predicted
Residual plot
Prediction error distribution
```

### Metrics

```text
MAE
RMSE
R²
```

### Error Analysis

Top những prediction sai nhiều nhất.

### Report

Bao gồm:

```text
Introduction
Dataset
Data Understanding
Data Cleaning
EDA
Feature Engineering
Methodology
Linear Regression
Evaluation
Error Analysis
Limitations
Conclusion
Future Work
```

---

# 39. TIÊU CHÍ ĐÁNH GIÁ PROJECT

Project nên chứng minh được 5 năng lực:

## 1. Data Understanding

Hiểu dữ liệu trước khi model.

## 2. Data Cleaning

Biết xử lý dữ liệu thực tế.

## 3. Feature Engineering

Biết lựa chọn/tạo feature hợp lý.

## 4. Machine Learning

Biết xây dựng và train Linear Regression.

## 5. Model Evaluation

Biết đánh giá và giải thích sai số.

---

# 40. ĐIỂM KHÔNG ĐƯỢC LÀM ẨU

Đặc biệt chú ý:

```text
❌ Không train trước khi hiểu data
❌ Không xóa outlier hàng loạt
❌ Không encode tùy tiện
❌ Không leakage
❌ Không dùng Price-derived feature để predict Price
❌ Không gọi R² là accuracy
❌ Không chỉ báo MAE/RMSE/R² rồi kết thúc
❌ Không giả lập Distance_to_Center
❌ Không bịa dữ liệu
❌ Không dùng model phức tạp để né yêu cầu Linear Regression
```

---

# 41. MỤC TIÊU CUỐI CÙNG

Mục tiêu không phải chỉ tạo ra một model có metric đẹp.

Mục tiêu của project là chứng minh:

> **Có thể sử dụng dữ liệu bất động sản thực tế tại Việt Nam để xây dựng một mô hình hồi quy tuyến tính dự báo giá dựa trên các đặc điểm của bất động sản và vị trí, đồng thời hiểu được cách dữ liệu thực tế ảnh hưởng đến chất lượng dự đoán và phân tích nguyên nhân khiến mô hình mắc sai số.**

---

# 42. BƯỚC HIỆN TẠI

Hiện tại **chưa được phép nhảy sang Model Training**.

Task đầu tiên của team:

```text
01_data_understanding.ipynb
```

Cần trả lời:

```text
1. Dataset có bao nhiêu dòng?
2. Có bao nhiêu cột?
3. Ý nghĩa từng cột?
4. Kiểu dữ liệu từng cột?
5. Có bao nhiêu missing values?
6. Missing percentage?
7. Có duplicate không?
8. Price có phân phối như thế nào?
9. Các numerical features có range như thế nào?
10. Location có bao nhiêu category?
11. Frontage có những giá trị nào?
12. Có giá trị bất thường nào ngay từ đầu không?
13. Dataset thực tế có đúng như Dataset Glossary mô tả không?
```

Sau khi hoàn thành bước này mới quyết định chính xác:

```text
Feature nào giữ?
Feature nào bỏ?
Missing xử lý thế nào?
Outlier xử lý thế nào?
Location encode thế nào?
Có thể tạo Distance_to_Center hay không?
```

---

# 43. NGUYÊN TẮC LÀM VIỆC

Project sẽ được thực hiện theo kiểu:

```text
UNDERSTAND
    ↓
CLEAN
    ↓
ANALYZE
    ↓
ENGINEER
    ↓
TRAIN
    ↓
EVALUATE
    ↓
EXPLAIN
```

**Mỗi quyết định preprocessing phải có lý do dựa trên dữ liệu.**

Không làm theo kiểu:

```text
"Machine Learning thường làm vậy"
```

mà phải giải thích:

```text
"Dữ liệu của project cho thấy vấn đề X,
do đó chúng ta chọn phương pháp Y."
```

Đây là điểm quan trọng để project thể hiện khả năng **xử lý dữ liệu thực tế**, đúng với yêu cầu của giảng viên.
