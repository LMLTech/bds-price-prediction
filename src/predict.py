import os
import joblib
import numpy as np
import pandas as pd
from features import process_location, add_engineered_features


def predict_price(input_data, model_path='models/linear_regression.pkl', is_log_target=False):
    """
    Dự đoán giá bất động sản dựa trên dictionary hoặc DataFrame đầu vào.
    Ví dụ input_data:
    {
        'area_m2': 80,
        'bedrooms': 3,
        'frontage': 1,
        'location': 'Quận 7, Hồ Chí Minh'
    }
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Không tìm thấy file mô hình tại: {model_path}")

    pipeline = joblib.load(model_path)

    if isinstance(input_data, dict):
        df_input = pd.DataFrame([input_data])
    elif isinstance(input_data, pd.DataFrame):
        df_input = input_data.copy()
    else:
        raise ValueError("input_data phải là dict hoặc pandas DataFrame")

    # Xử lý vị trí & tính khoảng cách tới CBD (spatial proxy)
    df_proc = process_location(df_input)
    df_proc = add_engineered_features(df_proc)

    # Dự đoán
    y_pred_raw = pipeline.predict(df_proc)


    if is_log_target:
        y_pred = np.expm1(y_pred_raw)
    else:
        y_pred = y_pred_raw

    y_pred = np.clip(y_pred, a_min=0, a_max=None)

    return y_pred
