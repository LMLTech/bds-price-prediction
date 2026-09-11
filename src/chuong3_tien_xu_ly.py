import logging
import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [TIỀN XỬ LÝ] - %(message)s",
)


def remove_outliers(data, column):
    """Loại các quan sát nằm ngoài khoảng IQR của một cột số."""
    q1 = data[column].quantile(0.25)
    q3 = data[column].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(current_dir, "..", "data", "raw", "dataset_BDS.xlsx")
    output_file = os.path.join(
        current_dir, "..", "data", "processed", "dataset_BDS_cleaned.csv"
    )
    heatmap_file = os.path.join(current_dir, "..", "images", "correlation_heatmap.png")

    logging.info("BƯỚC 1: Đọc dữ liệu thô từ file Excel...")
    try:
        df = pd.read_excel(input_file)
    except FileNotFoundError:
        logging.error("Lỗi: Không tìm thấy file %s", input_file)
        return

    logging.info("BƯỚC 2: Xóa các dòng không có giá bán...")
    df.dropna(subset=["price_million_vnd"], inplace=True)

    logging.info("BƯỚC 3: Điền dữ liệu khuyết cho các biến kết cấu...")
    features_to_fill = ["area_m2", "bedrooms", "bathrooms", "floors"]
    for feature in features_to_fill:
        df[feature] = df[feature].fillna(df[feature].median())

    df["frontage"] = df["frontage"].astype(int)

    logging.info("BƯỚC 4: Khử giá trị ngoại lệ bằng phương pháp IQR...")
    df = remove_outliers(df, "price_million_vnd")
    df = remove_outliers(df, "area_m2")

    logging.info("BƯỚC 5: Vẽ heatmap tương quan và xuất dữ liệu sạch...")
    features_list = [
        "area_m2",
        "bedrooms",
        "bathrooms",
        "floors",
        "frontage",
        "price_million_vnd",
    ]

    corr_matrix = df[features_list].corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Ma Trận Tương Quan (Pearson Correlation)")
    plt.tight_layout()
    os.makedirs(os.path.dirname(heatmap_file), exist_ok=True)
    plt.savefig(heatmap_file)
    plt.close()

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df[features_list].to_csv(output_file, index=False)
    logging.info("HOÀN TẤT CHƯƠNG 3! Dữ liệu đã sẵn sàng cho Chương 4.")


if __name__ == "__main__":
    main()
