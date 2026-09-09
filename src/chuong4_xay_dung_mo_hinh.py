import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def main():
    # 1. Đường dẫn tới file dữ liệu (dataset_BDS_cleaned.csv)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '..', 'data', 'processed', 'dataset_BDS_cleaned.csv')
    
    print("Đang đọc dữ liệu từ:", file_path)
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file tại {file_path}. Đảm bảo Liêm đã chạy xong Chương 3!")
        return

    # Xác định biến mục tiêu dựa trên file tiền xử lý
    TARGET_COLUMN = 'price_million_vnd' 
    
    if TARGET_COLUMN not in df.columns:
        raise ValueError(f"Không tìm thấy cột '{TARGET_COLUMN}'. Hãy kiểm tra lại file CSV!")

    # 2. Tách biến độc lập (X) và biến phụ thuộc (y)
    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]

    # 3. Chia tập dữ liệu Train / Test (Tỉ lệ 80/20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Kích thước tập Train: {X_train.shape[0]} mẫu")
    print(f"Kích thước tập Test: {X_test.shape[0]} mẫu\n")

    # 4. Chuẩn hóa dữ liệu bằng StandardScaler
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 5. Huấn luyện mô hình Hồi quy tuyến tính đa biến
    model = LinearRegression()
    model.fit(X_train_scaled, y_train)

    # 6. Dự đoán trên tập Test
    y_pred = model.predict(X_test_scaled)

    # 7. Tính toán các chỉ số đánh giá
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    # In kết quả ra Terminal
    print("="*50)
    print("KẾT QUẢ ĐÁNH GIÁ MÔ HÌNH HỒI QUY TUYẾN TÍNH")
    print("="*50)
    print(f"MAE  : {mae:,.2f} (Triệu VNĐ)")
    print(f"RMSE : {rmse:,.2f} (Triệu VNĐ)")
    print(f"R²   : {r2:.4f}")
    
    print("\n[Hệ số hồi quy - Trọng số của từng đặc trưng]")
    for feature, coef in zip(X.columns, model.coef_):
        print(f" - {feature}: {coef:,.2f}")
    print("="*50)
    
    # 8. Lưu kết quả dự đoán ra file CSV cho phần Trực quan hóa của Ngọc Anh
    output_df = pd.DataFrame({'Thuc_Te': y_test, 'Du_Doan': y_pred})
    predictions_path = os.path.join(current_dir, '..', 'data', 'processed', 'predictions.csv')
    output_df.to_csv(predictions_path, index=False)
    print(f"Đã xuất file dự đoán cho Ngọc Anh tại: {predictions_path}")

if __name__ == "__main__":
    main()