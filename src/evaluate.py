import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def evaluate_predictions(y_true, y_pred):
    """
    Tính toán các chỉ số đánh giá mô hình: MAE, RMSE, R2, MAPE.
    Các giá trị y_true và y_pred phải được đưa về đơn vị triệu VNĐ ban đầu.
    """
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)

    # Tính MAPE an toàn (bỏ qua nếu y_true <= 0)
    valid_mask = y_true > 0
    mape = np.mean(np.abs((y_true[valid_mask] - y_pred[valid_mask]) / y_true[valid_mask])) * 100

    metrics = {
        'MAE': mae,
        'RMSE': rmse,
        'R2': r2,
        'MAPE': mape
    }

    return metrics


def evaluate_model(pipeline, X_test, y_test, is_log_target=False):
    """
    Dự đoán trên tập Test và đánh giá hiệu năng mô hình.
    Nếu is_log_target=True, y_pred sẽ được nghịch đảo biến đổi bằng np.expm1().
    """
    y_pred_raw = pipeline.predict(X_test)

    if is_log_target:
        y_pred = np.expm1(y_pred_raw)
    else:
        y_pred = y_pred_raw

    # Giới hạn giá trị dự đoán không bị âm (giá bất động sản >= 0)
    y_pred = np.clip(y_pred, a_min=0, a_max=None)

    metrics = evaluate_predictions(y_test, y_pred)

    return metrics, y_pred


def plot_actual_vs_predicted(y_true, y_pred, save_path=None):
    """
    Vẽ biểu đồ So sánh Giá thực tế vs Giá dự đoán (có đường chéo y=x tham chiếu).
    """
    plt.figure(figsize=(9, 6))
    plt.scatter(y_true, y_pred, alpha=0.4, color='royalblue', edgecolors='none', s=25)

    # Đường tham chiếu y = x
    max_val = max(y_true.max(), y_pred.max())
    min_val = min(y_true.min(), y_pred.min())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Tham chiếu lý tưởng (y = x)')

    plt.title('Giá Thực Tế vs Giá Dự Đoán (Million VND)')
    plt.xlabel('Giá Thực Tế (Triệu VNĐ)')
    plt.ylabel('Giá Dự Đoán (Triệu VNĐ)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
    plt.close()


def plot_residuals(y_true, y_pred, save_path=None):
    """
    Vẽ biểu đồ Phân phối Sai số (Residual Distribution) và Sai số vs Giá dự đoán.
    """
    residuals = y_true - y_pred

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # 1. Phân phối sai số (Residual Distribution)
    sns.histplot(residuals, bins=50, kde=True, color='crimson', ax=axes[0])
    axes[0].set_title('Phân Phối Sai Số Dư (Residual Distribution)')
    axes[0].set_xlabel('Sai số = Giá thực tế - Giá dự đoán (Triệu VNĐ)')
    axes[0].set_ylabel('Tần suất')
    axes[0].grid(True, linestyle='--', alpha=0.5)

    # 2. Scatter plot Sai số vs Giá dự đoán
    axes[1].scatter(y_pred, residuals, alpha=0.4, color='purple', edgecolors='none', s=25)
    axes[1].axhline(y=0, color='r', linestyle='--', linewidth=2)
    axes[1].set_title('Sai Số Dư vs Giá Dự Đoán (Residuals vs Fitted)')
    axes[1].set_xlabel('Giá Dự Đoán (Triệu VNĐ)')
    axes[1].set_ylabel('Sai số Dư (Triệu VNĐ)')
    axes[1].grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
    plt.close()


def get_top_prediction_errors(df_test, y_true, y_pred, top_n=20):
    """
    Trích xuất Top N bản ghi có sai số tuyệt đối lớn nhất để phân tích nguyên nhân sai lệch.
    """
    df_err = df_test.copy()
    df_err['Thuc_Te'] = y_true.values if isinstance(y_true, pd.Series) else y_true
    df_err['Du_Doan'] = y_pred
    df_err['Sai_So_Tuyet_Doi'] = np.abs(df_err['Thuc_Te'] - df_err['Du_Doan'])
    df_err['Phan_Tram_Sai_So'] = np.abs((df_err['Thuc_Te'] - df_err['Du_Doan']) / df_err['Thuc_Te']) * 100

    top_errors = df_err.sort_values(by='Sai_So_Tuyet_Doi', ascending=False).head(top_n)

    return top_errors
