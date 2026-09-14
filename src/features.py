import numpy as np
import pandas as pd

# Tọa độ tham chiếu Trung tâm Thành phố (CBD - Central Business District)
CBD_COORDINATES = {
    'Hà Nội': (21.0285, 105.8542),       # Hồ Hoàn Kiếm, Hà Nội
    'Hồ Chí Minh': (10.7769, 106.7009),   # Chợ Bến Thành / Quận 1, TP.HCM
}

# Bảng tọa độ trung tâm đại diện cấp Quận/Huyện (District Representative Coordinates)
# Ghi chú học thuật: Đây là vị trí trung tâm địa bàn Quận/Huyện đại diện (District Spatial Proxy),
# không phải tọa độ chính xác từng căn nhà.
DISTRICT_COORDINATES = {
    # --- THÀNH PHỐ HỒ CHÍ MINH ---
    'Quận 1': (10.7756, 106.7004),
    'Quận 3': (10.7844, 106.6844),
    'Quận 4': (10.7578, 106.7012),
    'Quận 5': (10.7542, 106.6633),
    'Quận 6': (10.7481, 106.6353),
    'Quận 7': (10.7340, 106.7218),
    'Quận 8': (10.7242, 106.6286),
    'Quận 10': (10.7725, 106.6678),
    'Quận 11': (10.7631, 106.6508),
    'Quận 12': (10.8672, 106.6414),
    'Bình Thạnh': (10.8106, 106.7091),
    'Gò Vấp': (10.8383, 106.6653),
    'Tân Bình': (10.8014, 106.6531),
    'Tân Phú': (10.7900, 106.6283),
    'Bình Tân': (10.7653, 106.6039),
    'Thủ Đức': (10.8494, 106.7537),
    'Phú Nhuận': (10.7992, 106.6803),
    'Bình Chánh': (10.6873, 106.5938),
    'Hóc Môn': (10.8842, 106.5912),
    'Củ Chi': (11.0067, 106.5136),
    'Nhà Bè': (10.6483, 106.7319),
    'Cần Giờ': (10.4114, 106.9547),

    # --- THÀNH PHỐ HÀ NỘI ---
    'Hoàn Kiếm': (21.0285, 105.8542),
    'Ba Đình': (21.0341, 105.8242),
    'Đống Đa': (21.0125, 105.8278),
    'Hai Bà Trưng': (21.0078, 105.8525),
    'Cầu Giấy': (21.0361, 105.7906),
    'Thanh Xuân': (20.9936, 105.8117),
    'Tây Hồ': (21.0664, 105.8178),
    'Long Biên': (21.0367, 105.8925),
    'Hoàng Mai': (20.9783, 105.8453),
    'Nam Từ Liêm': (21.0142, 105.7644),
    'Bắc Từ Liêm': (21.0667, 105.7583),
    'Hà Đông': (20.9719, 105.7744),
    'Thanh Trì': (20.9414, 105.8508),
    'Gia Lâm': (21.0144, 105.9558),
    'Đông Anh': (21.1364, 105.8475),
    'Hoài Đức': (21.0236, 105.6983),
    'Đan Phượng': (21.1114, 105.6708),
    'Thường Tín': (20.8719, 105.8583),
    'Phúc Thọ': (21.1042, 105.5392),
    'Sơn Tây': (21.1378, 105.5058),
    'Thạch Thất': (21.0136, 105.5292),
    'Chương Mỹ': (20.8983, 105.6983),
    'Quốc Oai': (20.9878, 105.6414),
    'Mê Linh': (21.1764, 105.7175),
    'Sóc Sơn': (21.2583, 105.8525),
}


def haversine_distance(coord1, coord2):
    """
    Tính khoảng cách Haversine (km) giữa 2 tọa độ (lat, lon).
    """
    if coord1 is None or coord2 is None or np.isnan(coord1[0]) or np.isnan(coord2[0]):
        return np.nan

    R = 6371.0  # Bán kính Trái Đất theo km

    lat1, lon1 = np.radians(coord1[0]), np.radians(coord1[1])
    lat2, lon2 = np.radians(coord2[0]), np.radians(coord2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat / 2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    return R * c


def process_location(df):
    """
    Tách cột location thành province, district và tính khoảng cách haversine tới CBD.
    Ghi chú: distance_to_center_km được tính từ tọa độ trung tâm Quận/Huyện (District Spatial Proxy)
    tới trung tâm thành phố (Hà Nội: Hoàn Kiếm, TP.HCM: Quận 1).
    Đối với các tỉnh thành ngoài HN/HCM, khoảng cách được để NaN (không gán giá trị giả).
    """
    df_feat = df.copy()

    if 'location' in df_feat.columns:
        split_loc = df_feat['location'].astype(str).str.split(',')

        # Province là phần tử cuối cùng
        df_feat['province'] = split_loc.apply(lambda x: x[-1].strip() if isinstance(x, list) else None)

        # District là phần tử áp chót
        df_feat['district'] = split_loc.apply(lambda x: x[-2].strip() if isinstance(x, list) and len(x) >= 2 else None)

    # Tính khoảng cách tới CBD nếu có thông tin district & province
    distances = []
    for idx, row in df_feat.iterrows():
        prov = row.get('province')
        dist = row.get('district')

        if prov in CBD_COORDINATES and dist in DISTRICT_COORDINATES:
            cbd_coord = CBD_COORDINATES[prov]
            dist_coord = DISTRICT_COORDINATES[dist]
            d = haversine_distance(dist_coord, cbd_coord)
            distances.append(round(d, 2))
        else:
            distances.append(np.nan)

    df_feat['distance_to_center_km'] = distances
    return df_feat


def add_engineered_features(df):
    """
    Tạo các đặc trưng phi tuyến và tương quan miền (Domain Feature Engineering):
    - log_area: log1p(area_m2) bắt quan hệ tiệm cận
    - area_sq: area_m2^2 đặc trưng bậc 2 trong khuôn khổ Linear Regression
    - log_distance: log1p(distance_to_center_km)
    - area_dist_inter: area_m2 * distance_to_center_km
    """
    df_eng = df.copy()

    if 'area_m2' in df_eng.columns:
        df_eng['log_area'] = np.log1p(df_eng['area_m2'])
        df_eng['area_sq'] = df_eng['area_m2'] ** 2

    if 'distance_to_center_km' in df_eng.columns:
        med_dist = df_eng['distance_to_center_km'].median()
        dist_filled = df_eng['distance_to_center_km'].fillna(med_dist)
        df_eng['log_distance'] = np.log1p(dist_filled)

        if 'area_m2' in df_eng.columns:
            df_eng['area_dist_inter'] = df_eng['area_m2'] * dist_filled

    return df_eng


def select_model_features(df):
    """
    Lựa chọn tập đặc trưng mô hình:
    - Loại bỏ các cột không dùng hoặc đa cộng tuyến (bathrooms, floors, timeline_hours)
    - Giữ các biến số: area_m2, log_area, area_sq, bedrooms, frontage, distance_to_center_km, log_distance, area_dist_inter
    - Giữ các biến phân loại: province, district
    """
    df_feat = df.copy()

    if 'province' not in df_feat.columns or 'district' not in df_feat.columns:
        df_feat = process_location(df_feat)

    df_feat = add_engineered_features(df_feat)

    cols_to_drop = ['bathrooms', 'floors', 'timeline_hours', 'location']
    df_feat = df_feat.drop(columns=[col for col in cols_to_drop if col in df_feat.columns])

    # Bỏ các dòng thiếu province/district
    if 'province' in df_feat.columns and 'district' in df_feat.columns:
        df_feat = df_feat.dropna(subset=['province', 'district'])

    return df_feat


