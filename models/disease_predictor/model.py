"""BioBERT disease classifier with checkpoint-bound label metadata.

The classifier label mapping is stored beside the trained checkpoint. This prevents
an inference-time dataset mapping from silently changing the meaning or size of
the classifier head.
"""
import json
from pathlib import Path

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from models.base_model import BaseHealthModel, ModelInput, ModelOutput
from config.config import BIOBERT_MODEL, SAVED_WEIGHTS_DIR


class DiseasePredictorModel(BaseHealthModel):
    def __init__(self):
        super().__init__()
        self.disease2id = {}
        self.id2disease = {}
        self.num_labels = 0
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    @property
    def artifact_dir(self) -> Path:
        return SAVED_WEIGHTS_DIR / "disease_predictor"

    def load(self):
        """Load a Hugging Face model directory and its matching label mapping."""
        self.is_ready = False
        mapping_path = self.artifact_dir / "disease2id.json"
        config_path = self.artifact_dir / "config.json"

        if not mapping_path.is_file() or not config_path.is_file():
            print(
                "BioBERT disease artifacts are incomplete. "
                "Train with scripts/training/train_disease_predictor.py first."
            )
            return

        try:
            with mapping_path.open(encoding="utf-8") as file:
                raw_mapping = json.load(file)

            if not isinstance(raw_mapping, dict) or not raw_mapping:
                raise ValueError("disease2id.json must be a non-empty JSON object")

            self.disease2id = {
                str(name): int(label_id) for name, label_id in raw_mapping.items()
            }
            ids = sorted(self.disease2id.values())
            if ids != list(range(len(self.disease2id))):
                raise ValueError("Disease label IDs must be unique and contiguous from 0")

            self.num_labels = len(self.disease2id)
            self.id2disease = {
                label_id: name for name, label_id in self.disease2id.items()
            }

            with config_path.open(encoding="utf-8") as file:
                model_config = json.load(file)
            configured_labels = model_config.get("num_labels")
            if configured_labels != self.num_labels:
                raise ValueError(
                    "Checkpoint label count does not match disease2id.json "
                    f"({configured_labels} != {self.num_labels}). Retrain the model."
                )

            tokenizer = AutoTokenizer.from_pretrained(
                str(self.artifact_dir), local_files_only=True
            )
            model = AutoModelForSequenceClassification.from_pretrained(
                str(self.artifact_dir), local_files_only=True
            )
            if model.config.num_labels != self.num_labels:
                raise ValueError(
                    "Loaded classifier head does not match disease2id.json. "
                    "Retrain the model and replace the complete artifact directory."
                )

            self.tokenizer = tokenizer
            self.model = model.to(self.device)
            self.model.eval()
            self.is_ready = True
            print(f"BioBERT disease predictor loaded — {self.num_labels} classes")
        except Exception as exc:
            self.model = None
            self.tokenizer = None
            self.is_ready = False
            print(f"Could not load BioBERT disease predictor: {exc}")

    def predict(self, input: ModelInput) -> ModelOutput:
        if not self.is_ready or self.model is None or self.tokenizer is None:
            raise RuntimeError("BioBERT disease predictor is not loaded")
        if not isinstance(input.text, str) or not input.text.strip():
            raise ValueError("Symptoms text must be a non-empty string")

        encoded = self.tokenizer(
            input.text.strip(),
            return_tensors="pt",
            max_length=512,
            truncation=True,
            padding=True,
        )
        encoded = {key: value.to(self.device) for key, value in encoded.items()}

        with torch.inference_mode():
            outputs = self.model(**encoded)
            probabilities = torch.softmax(outputs.logits, dim=1)[0]

        top_k = min(3, self.num_labels)
        top = torch.topk(probabilities, k=top_k)
        diseases = [
            {
                "name": self.id2disease[int(index.item())],
                "confidence": round(float(score.item()), 3),
                "disease_id": int(index.item()),
            }
            for score, index in zip(top.values, top.indices)
        ]

        top_name = diseases[0]["name"] if diseases else "unknown"
        return ModelOutput(
            result={
                "diseases": diseases,
                "symptom_count": len(
                    [part for part in input.text.split(",") if part.strip()]
                ),
            },
            confidence=diseases[0]["confidence"] if diseases else 0.0,
            explanation=(
                f"BioBERT ranked {top_name} highest among its trained classes. "
                "This model output is not a diagnosis; consult a qualified clinician."
            ),
            sources=["biobert_classifier"],
        )
