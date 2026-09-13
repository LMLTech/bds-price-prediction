import os
import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def build_pipeline():
    """
    Xây dựng Pipeline chuẩn bị dữ liệu và huấn luyện Linear Regression:
    - Biến số (area_m2, bedrooms, frontage, distance_to_center_km): Imputer(median) + StandardScaler()
    - Biến phân loại (province, district): Imputer(most_frequent) + OneHotEncoder(handle_unknown='ignore')
    - Mô hình: LinearRegression()
    """
    numeric_features = ['area_m2', 'bedrooms', 'frontage', 'distance_to_center_km']
    categorical_features = ['province', 'district']

    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ]
    )

    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', LinearRegression())
    ])

    return pipeline


def train_and_save_model(X_train, y_train, output_path='models/linear_regression.pkl', use_log_target=False):
    """
    Huấn luyện pipeline trên X_train, y_train và lưu model ra file .pkl.
    Nếu use_log_target=True, target y sẽ được huấn luyện dưới dạng np.log1p(y).
    """
    pipeline = build_pipeline()

    y_train_fit = np.log1p(y_train) if use_log_target else y_train

    pipeline.fit(X_train, y_train_fit)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    joblib.dump(pipeline, output_path)
    print(f"Model saved successfully at: {output_path}")

    return pipeline
