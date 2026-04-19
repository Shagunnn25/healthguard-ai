import json
import numpy as np
import faiss
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from config.config import CLEANED_QA, EMBEDDING_MODEL

print("Loading QA records...")
records = []
for fname in ["medquad_clean.jsonl", "medqa_usmle_clean.jsonl", "medmcqa_clean.jsonl"]:
    fpath = CLEANED_QA / fname
    if fpath.exists():
        with open(fpath) as f:
            for line in f:
                try:
                    records.append(json.loads(line))
                except:
                    pass
        print(f"Loaded {fname}: {len(records)} total so far")

print(f"\nTotal records to index: {len(records)}")

print("Loading embedding model...")
embedder = SentenceTransformer(EMBEDDING_MODEL)

print("Encoding records...")
texts = [
    r.get("question", "") + " " + r.get("answer", "")
    for r in records
]
embeddings = embedder.encode(
    texts,
    show_progress_bar=True,
    normalize_embeddings=True,
    batch_size=64
)

print("Building FAISS index...")
dim = embeddings.shape[1]
index = faiss.IndexFlatIP(dim)
index.add(np.array(embeddings).astype("float32"))

faiss.write_index(index, str(CLEANED_QA / "qa_faiss.index"))
print(f"FAISS index saved — {index.ntotal} vectors")

with open(CLEANED_QA / "qa_records.jsonl", "w") as f:
    for r in records:
        f.write(json.dumps(r) + "\n")

print("✅ All done! FAISS index ready.")