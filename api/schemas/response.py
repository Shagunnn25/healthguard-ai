from pydantic import BaseModel
from typing import Any, List, Optional

class PredictionResponse(BaseModel):
    result: Any
    confidence: float
    explanation: str
    sources: List[str] = []
    error: Optional[str] = None
    disclaimer: str = "This is not a substitute for professional medical advice."