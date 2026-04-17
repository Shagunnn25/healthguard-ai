from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class SymptomRequest(BaseModel):
    text: str
    age: Optional[int] = None
    sex: Optional[str] = None

@router.post("/predict/disease")
def predict_disease(request: SymptomRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Symptoms cannot be empty")
    return {
        "result": {"diseases": [], "symptoms_received": request.text},
        "confidence": 0.0,
        "explanation": "Model not yet connected",
        "disclaimer": "This is not a substitute for professional medical advice."
    }