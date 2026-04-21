from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from api.routes import disease, lab, qa, ocr

app = FastAPI(title="HealthGuard AI")

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

# ── Chat endpoint ─────────────────────────────────
class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "running", "message": "HealthGuard AI is live"}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "modules": {
            "disease_predictor": "ready",
            "lab_analyzer":      "ready",
            "medical_qa":        "ready",
            "ocr":               "ready"
        }
    }

@app.post("/reset")
def reset():
    return {"status": "ok"}

@app.post("/chat")
def chat(req: ChatRequest):
    msg = req.message.lower()

    # Route to disease predictor
    if any(w in msg for w in ["fever","pain","headache","cough","nausea","fatigue","symptom"]):
        return {
            "response":     f"I can see you're describing symptoms. Please use the Disease Predictor module for a detailed analysis of: '{req.message}'",
            "module_used":  "Disease Predictor",
            "confidence":   0.85,
            "raw_result":   {},
            "disclaimer":   "Not a substitute for professional medical advice."
        }

    # Route to lab analyzer
    elif any(w in msg for w in ["glucose","hemoglobin","cholesterol","hba1c","lab","test","report","mg/dl","g/dl"]):
        return {
            "response":     f"This looks like a lab value query. Please use the Lab Analyzer module for: '{req.message}'",
            "module_used":  "Lab Analyzer",
            "confidence":   0.80,
            "raw_result":   {},
            "disclaimer":   "Not a substitute for professional medical advice."
        }

    # General medical Q&A
    else:
        return {
            "response":     f"Great question! For '{req.message}' — please use the Medical Q&A module for a detailed answer from our knowledge base.",
            "module_used":  "Medical Q&A",
            "confidence":   0.75,
            "raw_result":   {},
            "disclaimer":   "Not a substitute for professional medical advice."
        }