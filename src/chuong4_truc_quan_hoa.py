import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 1. Đọc dữ liệu dự đoán từ file của bạn Thái
current_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(current_dir, '..', 'data', 'processed', 'predictions.csv')
images_dir = os.path.join(current_dir, '..', 'images')
os.makedirs(images_dir, exist_ok=True)

df = pd.read_csv(input_path)

# 2. Đổi đơn vị sang TỶ VNĐ để số liệu gọn đẹp (1 Tỷ = 1,000 Triệu)
y_true = df['Thuc_Te'] / 1000.0
y_pred = df['Du_Doan'] / 1000.0
residuals = y_true - y_pred

# 3. Tính toán và in các chỉ số đánh giá mô hình (MAE, RMSE, R²)
mae = mean_absolute_error(y_true, y_pred)
rmse = np.sqrt(mean_squared_error(y_true, y_pred))
r2 = r2_score(y_true, y_pred)

print("=" * 45)
print("   KẾT QUẢ ĐÁNH GIÁ MÔ HÌNH HỒI QUY")
print("=" * 45)
print(f"• MAE  : {mae:,.2f} tỷ VNĐ ({mae * 1000:,.1f} triệu VNĐ)")
print(f"• RMSE : {rmse:,.2f} tỷ VNĐ ({rmse * 1000:,.1f} triệu VNĐ)")
print(f"• R²   : {r2:.4f} (Mô hình giải thích {r2 * 100:.2f}% biến động)")
print("=" * 45)

# Cài đặt giao diện chung cho biểu đồ
sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'DejaVu Sans']

# ---------------------------------------------------------
# BIỂU ĐỒ 1: Scatter plot (Giá thực tế vs Giá dự đoán)
# Trục tự động co giãn theo toàn bộ dữ liệu thật
# ---------------------------------------------------------
plt.figure(figsize=(7, 6))
plt.scatter(y_true, y_pred, alpha=0.3, color='#1f77b4', s=20, label='Mẫu BĐS kiểm thử')

# Đường chéo lý tưởng y = x tự động lấy theo min, max dữ liệu thật
min_val = min(y_true.min(), y_pred.min())
max_val = max(y_true.max(), y_pred.max())
plt.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Dự đoán hoàn hảo (y = x)')

plt.xlabel('Giá thực tế (Tỷ VNĐ)')
plt.ylabel('Giá dự đoán (Tỷ VNĐ)')
plt.title(f'Biểu đồ Scatter: Giá thực tế vs Giá dự đoán (R² = {r2:.4f})')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(images_dir, '01_scatter_thuc_te_vs_du_doan.png'), dpi=120)
plt.close()

# ---------------------------------------------------------
# BIỂU ĐỒ 2: Residuals vs Predicted (Không cắt bất kỳ residual nào)
# ---------------------------------------------------------
plt.figure(figsize=(7.5, 5))
plt.scatter(y_pred, residuals, alpha=0.3, color='#2ca02c', s=20)
plt.axhline(0, color='red', linestyle='--', linewidth=2, label='Đường sai số = 0')

plt.xlabel('Giá dự đoán (Tỷ VNĐ)')
plt.ylabel('Phần dư (Thực tế - Dự đoán) (Tỷ VNĐ)')
plt.title('Biểu đồ phần dư: Residuals vs Predicted Values')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(images_dir, '02_residuals_vs_predicted.png'), dpi=120)
plt.close()

# ---------------------------------------------------------
# BIỂU ĐỒ 3: Phân phối phần dư toàn bộ dữ liệu (Histogram & KDE)
# ---------------------------------------------------------
plt.figure(figsize=(7.5, 5))
sns.histplot(residuals, kde=True, bins=50, color='#4c72b0')
plt.axvline(0, color='red', linestyle='--', linewidth=2, label='Sai số = 0')

plt.xlabel('Phần dư (Tỷ VNĐ)')
plt.ylabel('Số lượng căn nhà')
plt.title('Phân phối của toàn bộ phần dư sai số (Residuals)')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(images_dir, '03_histogram_residuals.png'), dpi=120)
plt.close()

print("✓ Đã vẽ và lưu xong 3 biểu đồ vào thư mục images/ thành công!")