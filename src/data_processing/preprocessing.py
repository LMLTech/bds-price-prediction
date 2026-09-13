import pandas as pd
import numpy as np


def clean_real_estate_data(df):
    """
    Data cleaning
    """
    df_clean = df.copy()

    # 1. Drop các cột định danh không có giá trị nội suy cho Linear Regression
    cols_to_drop = ['id', 'detail_url', 'title']
    df_clean = df_clean.drop(columns=[col for col in cols_to_drop if col in df_clean.columns])

    # 2. Xử lý Missing Values
    # Đổi chuỗi "<null>" thành NaN chuẩn của Pandas
    df_clean = df_clean.replace('<null>', np.nan)

    # Xóa ngay các dòng không có giá
    df_clean = df_clean.dropna(subset=['price_million_vnd'])

    # Dùng Median để điền các biến số
    num_cols = ['area_m2', 'bedrooms', 'bathrooms', 'floors']
    for col in num_cols:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
            df_clean[col] = df_clean[col].fillna(df_clean[col].median())
            # Ép về int vì không thể có 2.5 phòng ngủ
            df_clean[col] = df_clean[col].astype(int)

    # 3. Chuẩn hóa Categorical / Boolean
    if 'frontage' in df_clean.columns:
        # Map True/False về 1/0
        df_clean['frontage'] = df_clean['frontage'].astype(str).str.lower()
        df_clean['frontage'] = df_clean['frontage'].map({'true': 1, 'false': 0}).fillna(0).astype(int)

    # 4. Xử lý Outlier & Giá trị vô lý (Hybrid Approach)
    # Lọc vật lý: Diện tích và giá phải > 0
    df_clean = df_clean[(df_clean['area_m2'] > 0) & (df_clean['price_million_vnd'] > 0)]

    # Ngưỡng trần (Hard Threshold) cắt các ca lỗi nhập liệu > 500 tỷ VNĐ
    df_clean = df_clean[df_clean['price_million_vnd'] < 500000]

    # Lọc IQR qua biến trung gian (price_per_m2)
    df_clean['price_per_m2'] = df_clean['price_million_vnd'] / df_clean['area_m2']
    Q1 = df_clean['price_per_m2'].quantile(0.25)
    Q3 = df_clean['price_per_m2'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    df_clean = df_clean[(df_clean['price_per_m2'] >= lower_bound) & (df_clean['price_per_m2'] <= upper_bound)]

    df_clean = df_clean.drop(columns=['price_per_m2'])

    return df_clean