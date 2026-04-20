from fastapi import APIRouter
import pickle
import pandas as pd
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity

router = APIRouter()

BASE = Path("api/models/qa")

with open(BASE / "vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open(BASE / "tfidf_matrix.pkl", "rb") as f:
    tfidf_matrix = pickle.load(f)

qa_df = pd.read_csv(BASE / "qa_database.csv")


@router.post("/qa")
def answer_question(req: dict):
    question = req.get("question", "")

    query_vec = vectorizer.transform([question])
    scores = cosine_similarity(query_vec, tfidf_matrix).flatten()

    idx = scores.argmax()

    return {
        "answer": qa_df.iloc[idx]["answer"]
    }