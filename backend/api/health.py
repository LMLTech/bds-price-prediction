from fastapi import APIRouter
from backend.services.model_service import model_service

router = APIRouter()


@router.get("/health")
def health_check():
    model_loaded = model_service.model is not None
    return {
        "status": "ok" if model_loaded else "warning",
        "model_loaded": model_loaded,
        "model_name": "Multiple Linear Regression"
    }
