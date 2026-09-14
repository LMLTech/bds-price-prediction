import unittest
import os
import sys
import numpy as np
from fastapi.testclient import TestClient

# Ensure project root is in sys.path
from backend.config import PROJECT_ROOT, SRC_DIR
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from backend.main import app
from backend.schemas.prediction import PredictRequest
from backend.services.prediction_service import prediction_service
import src.predict as direct_predict

class TestBackendPredictionConsistency(unittest.TestCase):

    def test_health_endpoint(self):
        with TestClient(app) as client:
            response = client.get("/api/health")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["status"], "ok")
            self.assertTrue(data["model_loaded"])

    def test_model_info_endpoint(self):
        with TestClient(app) as client:
            response = client.get("/api/model-info")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["model_name"], "Multiple Linear Regression")
            self.assertIn("test_metrics", data)

    def test_locations_endpoint(self):
        with TestClient(app) as client:
            response = client.get("/api/locations")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("provinces", data)
            self.assertGreaterEqual(len(data["provinces"]), 2)

    def test_visualizations_endpoint(self):
        with TestClient(app) as client:
            response = client.get("/api/visualizations")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("visualizations", data)
            self.assertEqual(len(data["visualizations"]), 15)

    def test_prediction_validation_errors(self):
        with TestClient(app) as client:
            # Area <= 0
            resp1 = client.post("/api/predict", json={
                "area_m2": 0,
                "bedrooms": 3,
                "frontage": 5,
                "province": "TP. Hồ Chí Minh",
                "district": "Quận 7"
            })
            self.assertEqual(resp1.status_code, 422)

            # Negative bedrooms
            resp2 = client.post("/api/predict", json={
                "area_m2": 80,
                "bedrooms": -1,
                "frontage": 5,
                "province": "TP. Hồ Chí Minh",
                "district": "Quận 7"
            })
            self.assertEqual(resp2.status_code, 422)


    def test_prediction_consistency_hcmc(self):
        """
        CRITICAL CONSISTENCY TEST: Compare direct Python inference from src/predict.py
        against FastAPI Service prediction for the exact same HCMC property input.
        """
        sample_input = {
            "area_m2": 85.0,
            "bedrooms": 3,
            "frontage": 5.0,
            "province": "Hồ Chí Minh",
            "district": "Quận 7"
        }

        raw_dict_direct = {
            "area_m2": sample_input["area_m2"],
            "bedrooms": sample_input["bedrooms"],
            "frontage": sample_input["frontage"],
            "location": f"{sample_input['district']}, {sample_input['province']}"
        }
        direct_res = direct_predict.predict_price(raw_dict_direct, model_path="models/linear_regression.pkl")
        direct_val = float(direct_res[0])

        req = PredictRequest(**sample_input)
        api_res = prediction_service.predict(req)
        api_val = api_res.predicted_price_million_vnd

        self.assertTrue(
            np.isclose(direct_val, api_val, rtol=1e-5, atol=1e-2),
            f"Mismatch between direct model inference ({direct_val}) and API prediction ({api_val})"
        )

    def test_prediction_consistency_hanoi(self):
        """
        CRITICAL CONSISTENCY TEST: Compare direct Python inference against API prediction
        for a Hanoi property input.
        """
        sample_input = {
            "area_m2": 60.0,
            "bedrooms": 2,
            "frontage": 4.0,
            "province": "Hà Nội",
            "district": "Cầu Giấy"
        }

        raw_dict_direct = {
            "area_m2": sample_input["area_m2"],
            "bedrooms": sample_input["bedrooms"],
            "frontage": sample_input["frontage"],
            "location": f"{sample_input['district']}, {sample_input['province']}"
        }
        direct_res = direct_predict.predict_price(raw_dict_direct, model_path="models/linear_regression.pkl")
        direct_val = float(direct_res[0])

        req = PredictRequest(**sample_input)
        api_res = prediction_service.predict(req)
        api_val = api_res.predicted_price_million_vnd

        self.assertTrue(np.isclose(direct_val, api_val, rtol=1e-5, atol=1e-2))


if __name__ == "__main__":
    unittest.main()

