from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from config.config import APP_NAME, API_VERSION, API_HOST, API_PORT
from api.routes import disease, lab, qa, ocr

app = FastAPI(
    title=APP_NAME,
    description="AI-powered medical assistant — self hosted, no external APIs",
    version=API_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(disease.router)
app.include_router(lab.router)
app.include_router(qa.router)
app.include_router(ocr.router)

@app.get("/")
def root():
    return {
        "app": APP_NAME,
        "version": API_VERSION,
        "status": "running",
        "endpoints": [
            "/predict/disease",
            "/analyze/lab",
            "/qa",
            "/ocr",
            "/health"
        ]
    }

@app.get("/health")
def health():
    return {
        "status": "ok",
        "version": API_VERSION,
        "modules": {
            "disease_predictor": "not loaded",
            "lab_analyzer":      "not loaded",
            "qa_engine":         "not loaded",
            "summarizer":        "not loaded",
            "ocr_module":        "not loaded"
        }
    }

if __name__ == "__main__":
    uvicorn.run("api.main:app", host=API_HOST, port=API_PORT, reload=True)