from pydantic import BaseModel, Field, field_validator


class PredictRequest(BaseModel):
    area_m2: float = Field(..., gt=0, description="Diện tích căn nhà (m²), phải lớn hơn 0")
    bedrooms: int = Field(..., ge=0, description="Số phòng ngủ, phải >= 0")
    frontage: float = Field(..., ge=0, description="Mặt tiền (m), phải >= 0")
    province: str = Field(..., min_length=1, description="Tỉnh/Thành phố")
    district: str = Field(..., min_length=1, description="Quận/Huyện")

    @field_validator("province")

    def validate_province(cls, v):
        v_clean = v.strip()
        if not v_clean:
            raise ValueError("Tỉnh/Thành phố không được để trống")
        return v_clean

    @field_validator("district")

    def validate_district(cls, v):
        v_clean = v.strip()
        if not v_clean:
            raise ValueError("Quận/Huyện không được để trống")
        return v_clean


class DerivedFeaturesSchema(BaseModel):
    log_area: float
    area_sq: float
    distance_to_center_km: float
    log_distance: float
    area_dist_inter: float


class PredictResponse(BaseModel):
    predicted_price_million_vnd: float
    predicted_price_vnd: int
    predicted_price_formatted: str
    inputs: dict
    derived_features: DerivedFeaturesSchema
    model_name: str = "Multiple Linear Regression"
