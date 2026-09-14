import os
import sys
from pathlib import Path

# Resolve base directories
BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent

# Ensure project root and src directory are in sys.path
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# Paths to ML artifacts and static files
MODEL_PATH = PROJECT_ROOT / "models" / "linear_regression.pkl"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

# CORS configuration
CORS_ORIGINS = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]
