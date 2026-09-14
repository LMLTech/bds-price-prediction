import numpy as np
import pandas as pd
import src.features as features
from backend.services.model_service import model_service
from backend.schemas.prediction import PredictRequest, PredictResponse, DerivedFeaturesSchema


def format_vietnamese_currency(price_million_vnd: float) -> str:
    """Format price in million VND into Vietnamese currency display text (tỷ / triệu)."""
    if price_million_vnd >= 1000:
        ty_val = price_million_vnd / 1000.0
        return f"{ty_val:,.2f} tỷ VNĐ".replace(",", " ")
    else:
        return f"{price_million_vnd:,.2f} triệu VNĐ".replace(",", " ")


class PredictionService:
    def predict(self, req: PredictRequest) -> PredictResponse:
        pipeline = model_service.get_model()

        # Construct single-row DataFrame matching training input format
        # location column format expected by src.features.process_location: 'District, Province'
        location_str = f"{req.district}, {req.province}"
        raw_dict = {
            "area_m2": req.area_m2,
            "bedrooms": req.bedrooms,
            "frontage": req.frontage,
            "province": req.province,
            "district": req.district,
            "location": location_str
        }

        df_input = pd.DataFrame([raw_dict])

        # Step 1: Spatial proxy distance processing
        df_proc = features.process_location(df_input)

        # Step 2: Feature Engineering (log_area, area_sq, log_distance, area_dist_inter)
        df_proc = features.add_engineered_features(df_proc)

        # Extract derived feature values
        distance_km = float(df_proc["distance_to_center_km"].iloc[0]) if not pd.isna(df_proc["distance_to_center_km"].iloc[0]) else 0.0
        log_dist = float(df_proc["log_distance"].iloc[0]) if "log_distance" in df_proc.columns else 0.0
        area_dist = float(df_proc["area_dist_inter"].iloc[0]) if "area_dist_inter" in df_proc.columns else 0.0

        derived = DerivedFeaturesSchema(
            log_area=round(float(df_proc["log_area"].iloc[0]), 4),
            area_sq=round(float(df_proc["area_sq"].iloc[0]), 2),
            distance_to_center_km=round(distance_km, 2),
            log_distance=round(log_dist, 4),
            area_dist_inter=round(area_dist, 2)
        )

        # Step 3: Inference via loaded pipeline
        y_pred_raw = pipeline.predict(df_proc)[0]

        # Step 4: Post-processing non-negativity constraint
        y_pred_clipped = float(np.maximum(y_pred_raw, 0.0))

        # Format outputs
        price_million = round(y_pred_clipped, 2)
        price_vnd = int(round(price_million * 1_000_000))
        price_formatted = format_vietnamese_currency(price_million)

        return PredictResponse(
            predicted_price_million_vnd=price_million,
            predicted_price_vnd=price_vnd,
            predicted_price_formatted=price_formatted,
            inputs={
                "area_m2": req.area_m2,
                "bedrooms": req.bedrooms,
                "frontage": req.frontage,
                "province": req.province,
                "district": req.district
            },
            derived_features=derived,
            model_name="Multiple Linear Regression"
        )


prediction_service = PredictionService()
