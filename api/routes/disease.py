from fastapi import APIRouter, HTTPException
import numpy as np
import pickle
import json
from pathlib import Path

router = APIRouter()

# paths
BASE = Path("api/models/disease")

# load once
with open(BASE / "model.pkl", "rb") as f:
    disease_model = pickle.load(f)

with open(BASE / "all_symptoms.json") as f:
    all_symptoms = json.load(f)

with open(BASE / "id2disease.json") as f:
    id2disease = json.load(f)


@router.post("/predict/disease")
def predict_disease(req: dict):
    text = req.get("text", "")
    symptoms = [s.strip().lower() for s in text.split(",")]

    vec = np.zeros(len(all_symptoms))
    matched = []

    for sym in symptoms:
        if sym in all_symptoms:
            vec[all_symptoms.index(sym)] = 1
            matched.append(sym)

    if not matched:
        raise HTTPException(status_code=400, detail="No valid symptoms found")

    proba = disease_model.predict_proba([vec])[0]
    top_indices = np.argsort(proba)[::-1][:3]

    results = []
    for idx in top_indices:
        results.append({
            "disease": id2disease[str(idx)],
            "confidence": float(proba[idx])
        })

    return {"diseases": results}