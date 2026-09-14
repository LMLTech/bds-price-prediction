from fastapi import APIRouter
from backend.api.health import router as health_router
from backend.api.predict import router as predict_router
from backend.api.model_info import router as model_info_router
from backend.api.locations import router as locations_router
from backend.api.visualizations import router as visualizations_router

api_router = APIRouter(prefix="/api")

api_router.include_router(health_router, tags=["Health"])
api_router.include_router(predict_router, tags=["Prediction"])
api_router.include_router(model_info_router, tags=["Model Info"])
api_router.include_router(locations_router, tags=["Locations"])
api_router.include_router(visualizations_router, tags=["Visualizations"])
