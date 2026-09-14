import os
import sys
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Resolve backend directory and project root
BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.config import FIGURES_DIR, CORS_ORIGINS
from backend.services.model_service import model_service
from backend.api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event: Load ML pipeline serialized model once into memory
    print("[FastAPI Startup] Loading ML pipeline model...")
    model_service.load_model()
    print("[FastAPI Startup] ML model ready for inference.")
    yield
    # Shutdown event
    print("[FastAPI Shutdown] Server shutting down...")


app = FastAPI(
    title="Real Estate Price Prediction API",
    description="FastAPI Backend for Real Estate Price Prediction using Multiple Linear Regression",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount pre-generated static visualization figure files
if FIGURES_DIR.exists():
    app.mount("/static/figures", StaticFiles(directory=str(FIGURES_DIR)), name="figures")

# Register API Router
app.include_router(api_router)


@app.get("/")
def root_redirect():
    return {
        "message": "Real Estate Price Prediction API is running",
        "docs": "/docs",
        "health": "/api/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
