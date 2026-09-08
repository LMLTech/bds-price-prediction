import pandas as pd
import numpy as np
import os
import logging
from geopy.distance import geodesic
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import matplotlib.pyplot as plt

# Cấu hình logging để theo dõi tiến trình trên Terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [TIỀN XỬ LÝ] - %(message)s')

# Từ điển tọa độ của các quận/huyện tại Hà Nội và Hồ Chí Minh để tính khoảng cách đến trung tâm
OFFLINE_COORDS = {
    'Long Biên, Hà Nội': (21.0475, 105.8906), 'Bình Chánh, Hồ Chí Minh': (10.6874, 106.5501),
    'Gò Vấp, Hồ Chí Minh': (10.8277, 106.6660), 'Cầu Giấy, Hà Nội': (21.0305, 105.7932),
    'Hà Đông, Hà Nội': (20.9622, 105.7725), 'Thanh Xuân, Hà Nội': (20.9937, 105.8080),
    'Nam Từ Liêm, Hà Nội': (21.0125, 105.7534), 'Quận 8, Hồ Chí Minh': (10.7241, 106.6286),
    'Quận 5, Hồ Chí Minh': (10.7540, 106.6633), 'Tây Hồ, Hà Nội': (21.0694, 105.8202),
    'Quận 12, Hồ Chí Minh': (10.8671, 106.6413), 'Thủ Đức, Hồ Chí Minh': (10.8494, 106.7537),
    'Quận 4, Hồ Chí Minh': (10.7584, 106.7011), 'Hoài Đức, Hà Nội': (21.0381, 105.6983),
    'Ba Đình, Hà Nội': (21.0341, 105.8149), 'Bình Tân, Hồ Chí Minh': (10.7302, 106.5925),
    'Tân Bình, Hồ Chí Minh': (10.8014, 106.6526), 'Tân Phú, Hồ Chí Minh': (10.7872, 106.6327),
    'Quận 10, Hồ Chí Minh': (10.7743, 106.6669), 'Đông Anh, Hà Nội': (21.1444, 105.8340),
    'Hai Bà Trưng, Hà Nội': (21.0093, 105.8504), 'Quận 7, Hồ Chí Minh': (10.7339, 106.7145),
    'Quận 3, Hồ Chí Minh': (10.7843, 106.6841), 'Bắc Từ Liêm, Hà Nội': (21.0652, 105.7460),
    'Hoàng Mai, Hà Nội': (20.9654, 105.8490), 'Bình Thạnh, Hồ Chí Minh': (10.8105, 106.7091),
    'Phú Nhuận, Hồ Chí Minh': (10.7993, 106.6806), 'Quận 11, Hồ Chí Minh': (10.7629, 106.6433),
    'Quận 1, Hồ Chí Minh': (10.7756, 106.7019), 'Quận 9, Hồ Chí Minh': (10.8428, 106.8286),
    'Đống Đa, Hà Nội': (21.0129, 105.8272), 'Quận 2, Hồ Chí Minh': (10.7876, 106.7451),
    'Nhà Bè, Hồ Chí Minh': (10.6276, 106.7230), 'Hóc Môn, Hồ Chí Minh': (10.8841, 106.5926),
    'Thanh Oai, Hà Nội': (20.8656, 105.7675), 'Hoàn Kiếm, Hà Nội': (21.0287, 105.8524),
    'Đan Phượng, Hà Nội': (21.1090, 105.6792), 'Thanh Trì, Hà Nội': (20.9419, 105.8342),
    'Gia Lâm, Hà Nội': (21.0180, 105.9407), 'Quận 6, Hồ Chí Minh': (10.7480, 106.6341),
    'Sơn Tây, Hà Nội': (21.1350, 105.4981), 'Mê Linh, Hà Nội': (21.1895, 105.7088),
    'Chương Mỹ, Hà Nội': (20.8905, 105.6888), 'Sóc Sơn, Hà Nội': (21.2647, 105.8475),
    'Thường Tín, Hà Nội': (20.8821, 105.8647), 'Củ Chi, Hồ Chí Minh': (11.0066, 106.5186),
    'Cần Giờ, Hồ Chí Minh': (10.4011, 106.9400), 'Quốc Oai, Hà Nội': (20.9789, 105.6267),
    'Phú Xuyên, Hà Nội': (20.7329, 105.9038), 'Thạch Thất, Hà Nội': (21.0044, 105.5492),
    'Phúc Thọ, Hà Nội': (21.1118, 105.5843), 'Ba Vì, Hà Nội': (21.1963, 105.3995),
    'Mỹ Đức, Hà Nội': (20.7188, 105.6946), 'Ứng Hòa, Hà Nội': (20.7351, 105.7686)
}

def main():
    # Bước 1: Khởi tạo và nạp dữ liệu thô
    logging.info("BƯỚC 1: Đọc dữ liệu thô từ file Excel...")
    input_file = "../data/raw/dataset_BDS.xlsx"
    output_file = "../data/processed/dataset_BDS_cleaned.csv"
    
    try:
        df = pd.read_excel(input_file)
    except FileNotFoundError:
        logging.error(f"Lỗi: Không tìm thấy file {input_file}")
        return

    # Bước 2: Khoanh vùng khu vực (Chỉ lấy HN & HCM) và xóa dòng khuyết giá
    logging.info("BƯỚC 2: Lọc dữ liệu HN & HCM, xóa các dòng không có giá bán...")
    df = df[df['location'].str.contains('Hà Nội|Hồ Chí Minh', na=False, regex=True)].copy()
    df.dropna(subset=['price_million_vnd'], inplace=True)

    # Bước 3: Điền khuyết dữ liệu (Imputation)
    logging.info("BƯỚC 3: Điền khuyết các biến kết cấu bằng Trung vị (Median)...")
    features_to_fill = ['area_m2', 'bedrooms', 'bathrooms', 'floors']
    for feature in features_to_fill:
        df[feature] = df[feature].fillna(df[feature].median())
    
    # Mã hóa biến mặt tiền từ dạng logic (True/False) sang nhị phân (1/0)
    df['frontage'] = df['frontage'].astype(int)

    # Bước 4: Lượng hóa khoảng cách địa lý
    logging.info("BƯỚC 4: Tính khoảng cách đến trung tâm bằng công thức Haversine...")
    center_hn = (21.028511, 105.854165)
    center_hcm = (10.779785, 106.699017)
    
    def get_haversine_distance(row):
        coords = OFFLINE_COORDS.get(row['location'], (np.nan, np.nan))
        if pd.isna(coords[0]):
            return np.nan
        if 'Hà Nội' in row['location']:
            return geodesic(coords, center_hn).km
        return geodesic(coords, center_hcm).km

    df['distance_to_center_km'] = df.apply(get_haversine_distance, axis=1)
    if df['distance_to_center_km'].isna().sum() > 0:
        df['distance_to_center_km'] = df['distance_to_center_km'].fillna(df['distance_to_center_km'].median())

    # Bước 5: Mã hóa tên quận huyện
    logging.info("BƯỚC 5: Mã hóa tên khu vực (Label Encoding)...")
    le = LabelEncoder()
    df['location_encoded'] = le.fit_transform(df['location'])

    # Bước 6: Khử giá trị ngoại lệ (Outliers)
    logging.info("BƯỚC 6: Khử ngoại lệ bằng phương pháp thống kê IQR...")
    def remove_outliers(data, column):
        Q1 = data[column].quantile(0.25)
        Q3 = data[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        return data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]

    df = remove_outliers(df, 'price_million_vnd')
    df = remove_outliers(df, 'area_m2')

    # Bước 7: Trực quan hóa tương quan và xuất dữ liệu sạch
    logging.info("BƯỚC 7: Vẽ Heatmap tương quan và đóng gói dữ liệu...")
    features_list = ['area_m2', 'bedrooms', 'bathrooms', 'floors', 'frontage', 
                     'distance_to_center_km', 'location_encoded', 'price_million_vnd']
    
    corr_matrix = df[features_list].corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title('Ma Tran Tuong Quan (Pearson Correlation)')
    plt.tight_layout()
    plt.savefig('../images/correlation_heatmap.png')
    
    df_clean = df[features_list].copy()
    df_clean.to_csv(output_file, index=False)
    
    logging.info("HOÀN TẤT CHƯƠNG 3! Dữ liệu đã sẵn sàng cho Chương 4.")

if __name__ == "__main__":
    main()