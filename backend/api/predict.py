from fastapi import APIRouter, HTTPException, status
from backend.schemas.prediction import PredictRequest, PredictResponse
from backend.services.prediction_service import prediction_service

router = APIRouter()


@router.post("/predict", response_model=PredictResponse)
def predict_price(request: PredictRequest):
    try:
        response = prediction_service.predict(request)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi dự đoán giá bất động sản: {str(e)}"
        )
