from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class LabRequest(BaseModel):
    test_name: str
    value: float
    sex: Optional[str] = None
    age: Optional[int] = None

@router.post("/analyze/lab")
def analyze_lab(request: LabRequest):
    if request.value < 0:
        raise HTTPException(status_code=400, detail="Value cannot be negative")
    return {
        "result": {"test": request.test_name, "value": request.value, "status": "pending"},
        "confidence": 0.0,
        "explanation": "Lab analyzer not yet connected",
        "disclaimer": "This is not a substitute for professional medical advice."
    }