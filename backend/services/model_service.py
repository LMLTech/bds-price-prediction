import logging
import joblib
from pathlib import Path
from backend.config import MODEL_PATH

logger = logging.getLogger("uvicorn.error")

class ModelService:
    def __init__(self):
        self.model = None
        self.model_path = MODEL_PATH

    def load_model(self):
        if not self.model_path.exists():
            error_msg = f"Model file not found at: {self.model_path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        logger.info(f"Loading ML model from {self.model_path}...")
        self.model = joblib.load(self.model_path)
        logger.info("ML model loaded successfully into memory.")

    def get_model(self):
        if self.model is None:
            self.load_model()
        return self.model

    def get_model_info(self):
        return {
            "model_name": "Multiple Linear Regression",
            "algorithm": "sklearn.linear_model.LinearRegression",
            "model_path": str(self.model_path),
            "test_metrics": {
                "raw": {
                    "r2": 0.3729,
                    "mae_million_vnd": 8417.93,
                    "rmse_million_vnd": 21435.74
                },
                "clipped": {
                    "r2": 0.3839,
                    "mae_million_vnd": 8065.00,
                    "rmse_million_vnd": 21247.69
                }
            },
            "test_samples": 9172,
            "total_features": 280,
            "numerical_features": [
                "area_m2", "log_area", "area_sq", "bedrooms",
                "frontage", "distance_to_center_km", "log_distance", "area_dist_inter"
            ],
            "categorical_features": ["province", "district"],
            "target_unit": "Million VND (Triệu VNĐ)"
        }

model_service = ModelService()
