from fastapi import APIRouter
from backend.config import FIGURES_DIR

router = APIRouter()

VISUALIZATION_CATALOG = [
    # Dataset Overview
    {
        "id": "01_price_distribution",
        "title": "Phân phối giá bất động sản (Price Distribution)",
        "category": "Dataset",
        "filename": "01_price_distribution.png",
        "url": "/static/figures/01_price_distribution.png",
        "description": "Thể hiện phân phối giá bất động sản thực tế. Dữ liệu lệch phải rõ rệt với phần lớn tài sản nằm ở phân khúc phổ thông và một số ít bất động sản giá trị rất cao."
    },
    {
        "id": "02_log_price_distribution",
        "title": "Phân phối giá logarit (Log Price Distribution)",
        "category": "Dataset",
        "filename": "02_log_price_distribution.png",
        "url": "/static/figures/02_log_price_distribution.png",
        "description": "Phân phối biến giá mục tiêu sau khi biến đổi log1p. Biến đổi log giúp phân phối chuẩn hóa hơn, giảm ảnh hưởng của cực trị và phù hợp hơn với giả định mô hình tuyến tính."
    },

    # Property Characteristics
    {
        "id": "03_area_vs_price",
        "title": "Diện tích vs Giá (Area vs Price)",
        "category": "Property",
        "filename": "03_area_vs_price.png",
        "url": "/static/figures/03_area_vs_price.png",
        "description": "Biểu đồ tán xạ thể hiện mối quan hệ giữa diện tích (m²) và giá trị tài sản. Giá có xu hướng tăng theo diện tích, nhưng độ tán xạ tăng mạnh ở các diện tích lớn."
    },
    {
        "id": "04_price_by_bedrooms",
        "title": "Phân phối giá theo số phòng ngủ (Price by Bedrooms)",
        "category": "Property",
        "filename": "04_price_by_bedrooms.png",
        "url": "/static/figures/04_price_by_bedrooms.png",
        "description": "Boxplot thể hiện giá theo số phòng ngủ. Số phòng ngủ có tương quan thuận với giá trị tài sản."
    },
    {
        "id": "05_price_by_area_bucket",
        "title": "Phân bố giá theo khoảng diện tích (Price by Area Bucket)",
        "category": "Property",
        "filename": "05_price_by_area_bucket.png",
        "url": "/static/figures/05_price_by_area_bucket.png",
        "description": "So sánh mức giá trung bình và trung vị giữa các nhóm diện tích bất động sản."
    },

    # Location Analysis
    {
        "id": "06_avg_price_by_district",
        "title": "Giá trung bình theo Quận/Huyện (Average Price by District)",
        "category": "Location",
        "filename": "06_avg_price_by_district.png",
        "url": "/static/figures/06_avg_price_by_district.png",
        "description": "Mức giá trung bình giữa các Quận/Huyện trên địa bàn Hà Nội và TP.HCM."
    },
    {
        "id": "07_median_price_per_m2_by_district",
        "title": "Đơn giá trung vị (Triệu VNĐ/m²) theo Quận (Median Price/m² by District)",
        "category": "Location",
        "filename": "07_median_price_per_m2_by_district.png",
        "url": "/static/figures/07_median_price_per_m2_by_district.png",
        "description": "Đơn giá trung vị trên m² hiển thị rõ mức độ đắt đỏ của các quận trung tâm so với các quận ngoại thành."
    },
    {
        "id": "08_distance_vs_price",
        "title": "Khoảng cách tới trung tâm vs Giá (Distance Proxy vs Price)",
        "category": "Location",
        "filename": "08_distance_vs_price.png",
        "url": "/static/figures/08_distance_vs_price.png",
        "description": "Khoảng cách đại diện theo địa bàn (Distance Spatial Proxy) có tương quan nghịch với giá. Bất động sản gần trung tâm có mức giá cao hơn rõ rệt."
    },
    {
        "id": "09_price_by_distance_bucket",
        "title": "Phân bố giá theo vành đai khoảng cách (Price by Distance Bucket)",
        "category": "Location",
        "filename": "09_price_by_distance_bucket.png",
        "url": "/static/figures/09_price_by_distance_bucket.png",
        "description": "Biểu đồ phân nhóm thể hiện mức giảm giá bất động sản khi bán kính khoảng cách tới trung tâm tăng dần."
    },

    # Model Performance
    {
        "id": "10_actual_vs_predicted",
        "title": "Giá thực tế vs Giá dự báo (Actual vs Predicted)",
        "category": "Model",
        "filename": "10_actual_vs_predicted.png",
        "url": "/static/figures/10_actual_vs_predicted.png",
        "description": "So sánh giữa giá thực tế (trục X) và giá dự báo của mô hình Multiple Linear Regression (trục Y). Đường chéo thể hiện dự báo hoàn hảo."
    },
    {
        "id": "11_residual_distribution",
        "title": "Phân phối phần dư (Residual Distribution)",
        "category": "Model",
        "filename": "11_residual_distribution.png",
        "url": "/static/figures/11_residual_distribution.png",
        "description": "Biểu đồ tần số phần dư (Actual - Predicted). Phần dư tập trung xung quanh 0 nhưng có đuôi dài do các điểm dữ liệu giá cao."
    },
    {
        "id": "12_residual_vs_predicted",
        "title": "Phân phối phần dư vs Giá dự báo (Residual vs Predicted)",
        "category": "Model",
        "filename": "12_residual_vs_predicted.png",
        "url": "/static/figures/12_residual_vs_predicted.png",
        "description": "Biểu đồ chẩn đoán phương sai sai số (Heteroscedasticity Diagnosis). Phương sai phần dư tăng nhẹ khi giá trị dự báo tăng."
    },

    # Error Analysis
    {
        "id": "13_absolute_error_distribution",
        "title": "Phân phối sai số tuyệt đối (Absolute Error Distribution)",
        "category": "Error",
        "filename": "13_absolute_error_distribution.png",
        "url": "/static/figures/13_absolute_error_distribution.png",
        "description": "Phân phối giá trị tuyệt đối |Actual - Predicted| trên tập kiểm thử test set."
    },
    {
        "id": "14_error_by_price_range",
        "title": "Sai số theo phân khúc giá (Error by Price Range)",
        "category": "Error",
        "filename": "14_error_by_price_range.png",
        "url": "/static/figures/14_error_by_price_range.png",
        "description": "Mức độ sai số MAE/RMSE phân tích theo từng dải phân khúc giá (từ bình dân đến cao cấp)."
    },
    {
        "id": "15_top_prediction_errors",
        "title": "Top 20 mẫu có sai số lớn nhất (Top 20 Prediction Errors)",
        "category": "Error",
        "filename": "15_top_prediction_errors.png",
        "url": "/static/figures/15_top_prediction_errors.png",
        "description": "Phân tích định tính 20 mẫu bất động sản có sai số lớn nhất để phục vụ đánh giá hạn chế mô hình học thuật."
    }
]


@router.get("/visualizations")
def get_visualizations():
    # Verify file existence dynamically
    available_items = []
    for item in VISUALIZATION_CATALOG:
        filepath = FIGURES_DIR / item["filename"]
        item_copy = dict(item)
        item_copy["exists"] = filepath.exists()
        available_items.append(item_copy)

    return {
        "visualizations": available_items,
        "categories": ["Dataset", "Property", "Location", "Model", "Error"]
    }
