import pandas as pd


def process_location(df):
    """
    Tách cột location thành district và province.
    Xử lý từ phía đuôi chuỗi để đảm bảo lấy đúng Tỉnh/Thành phố.
    """
    df_feat = df.copy()

    if 'location' in df_feat.columns:
        # Tách chuỗi theo dấu phẩy
        split_loc = df_feat['location'].astype(str).str.split(',')

        # Province luôn là phần tử cuối cùng
        df_feat['province'] = split_loc.apply(lambda x: x[-1].strip() if isinstance(x, list) else None)

        # District là phần tử áp chót (nếu địa chỉ có đủ cấu trúc)
        df_feat['district'] = split_loc.apply(lambda x: x[-2].strip() if isinstance(x, list) and len(x) >= 2 else None)

        # Drop cột location gốc
        df_feat = df_feat.drop(columns=['location'])

    return df_feat


def select_model_features(df):
    """
    Loại bỏ các đặc trưng gây nhiễu (floors) và đa cộng tuyến (bathrooms).
    """
    df_feat = df.copy()
    cols_to_drop = ['bathrooms', 'floors']
    df_feat = df_feat.drop(columns=[col for col in cols_to_drop if col in df_feat.columns])

    # Drop luôn các dòng bị thiếu district/province sau khi tách chuỗi
    df_feat = df_feat.dropna(subset=['province', 'district'])

    return df_feat