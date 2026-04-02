# config/config.py
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
LOGS_DIR = BASE_DIR / "logs"

# Data paths
RAW_DATA = DATA_DIR / "raw"
CLEANED_DATA = DATA_DIR / "cleaned"

# Model paths
SAVED_WEIGHTS = MODELS_DIR / "saved_weights"

# Model configs
DISEASE_MODEL_NAME = "dmis-lab/biobert-v1.1"
QA_MODEL_NAME = "google/flan-t5-base"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# API configs
API_HOST = "0.0.0.0"
API_PORT = 8000
MAX_INPUT_LENGTH = 512

# Create dirs if they don't exist
for d in [DATA_DIR, MODELS_DIR, LOGS_DIR, RAW_DATA, CLEANED_DATA, SAVED_WEIGHTS]:
    d.mkdir(parents=True, exist_ok=True)