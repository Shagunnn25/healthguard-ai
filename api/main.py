python id="5v44rs"
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.config import APP_NAME, API_VERSION
from api.routes import disease, lab, qa, ocr

app = FastAPI(title=APP_NAME, version=API_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# attach routes
app.include_router(disease.router)
app.include_router(lab.router)
app.include_router(qa.router)
app.include_router(ocr.router)

@app.get("/")
def root():
    return {
        "app": APP_NAME,
        "version": API_VERSION,
        "status": "running"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
