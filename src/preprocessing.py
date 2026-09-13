import os
import numpy as np
import pandas as pd


def load_raw_data(file_path):
    """
    Nạp dữ liệu thô từ file CSV hoặc Excel.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Không tìm thấy file dữ liệu tại: {file_path}")

    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Định dạng file không hỗ trợ. Sử dụng .csv hoặc .xlsx")

    return df


def clean_domain_bounds(df):
    """
    Làm sạch cơ bản theo miền giá trị vật lý (Domain Knowledge):
    - Đổi các chuỗi '<null>' thành NaN
    - Loại bỏ các dòng thiếu Target (`price_million_vnd`)
    - Diện tích `area_m2` phải > 0 và <= 2,000 m2
    - Giá bán `price_million_vnd` phải > 0 và <= 500,000 triệu VNĐ (500 tỷ VNĐ)
    - Số phòng ngủ `bedrooms`, số phòng tắm `bathrooms`, số tầng `floors` phải >= 0 nếu có.
    """
    df_clean = df.copy()

    # Chuẩn hóa giá trị thiếu từ chuỗi văn bản
    df_clean = df_clean.replace('<null>', np.nan)

    # Loại bỏ các dòng không có giá mục tiêu
    if 'price_million_vnd' in df_clean.columns:
        df_clean['price_million_vnd'] = pd.to_numeric(df_clean['price_million_vnd'], errors='coerce')
        df_clean = df_clean.dropna(subset=['price_million_vnd'])
        df_clean = df_clean[df_clean['price_million_vnd'] > 0]

    # Kiểm tra diện tích
    if 'area_m2' in df_clean.columns:
        df_clean['area_m2'] = pd.to_numeric(df_clean['area_m2'], errors='coerce')

    # Chuyển đổi kiểu dữ liệu cho các biến kết cấu
    for col in ['bedrooms', 'bathrooms', 'floors']:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

    # Lọc ngưỡng vật lý miền bất động sản (tránh lỗi gõ gõ nhầm 62 triệu m2 hay 772 triệu tầng)
    if 'area_m2' in df_clean.columns:
        df_clean = df_clean[(df_clean['area_m2'] > 0) & (df_clean['area_m2'] <= 2000)]

    if 'price_million_vnd' in df_clean.columns:
        df_clean = df_clean[df_clean['price_million_vnd'] <= 500000]

    # Chuẩn hóa biến Frontage về dạng 0/1 integer
    if 'frontage' in df_clean.columns:
        df_clean['frontage'] = df_clean['frontage'].astype(str).str.lower()
        df_clean['frontage'] = df_clean['frontage'].map({'true': 1, 'false': 0, '1': 1, '0': 0}).fillna(0).astype(int)

    # Drop các cột định danh không có giá trị nội suy
    cols_to_drop = ['id', 'detail_url', 'title']
    df_clean = df_clean.drop(columns=[c for c in cols_to_drop if c in df_clean.columns])

    # Xóa dữ liệu trùng lặp hoàn toàn
    df_clean = df_clean.drop_duplicates()

    return df_clean
