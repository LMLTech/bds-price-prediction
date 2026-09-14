from fastapi import APIRouter
from backend.services.model_service import model_service

router = APIRouter()


@router.get("/model-info")
def get_model_info():
    return model_service.get_model_info()
