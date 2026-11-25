"""BioBERT disease classifier with checkpoint-bound label metadata."""
import json
from pathlib import Path

import torch

from models.base_model import BaseHealthModel, ModelInput, ModelOutput
from config.config import BIOBERT_MODEL, DISEASE_MODEL_DIR, SAVED_WEIGHTS_DIR


class DiseasePredictorModel(BaseHealthModel):
    def __init__(self):
        super().__init__()
        self.disease2id = {}
        self.id2disease = {}
        self.num_labels = 0
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    @property
    def artifact_dir(self) -> Path:
        """Preferred Hugging Face save_pretrained() artifact directory."""
        return SAVED_WEIGHTS_DIR / "disease_predictor"

    @property
    def legacy_checkpoint_path(self) -> Path:
        """Pre-existing state-dict checkpoint downloaded from the project README."""
        return SAVED_WEIGHTS_DIR / "disease_predictor.pt"

    @property
    def legacy_mapping_path(self) -> Path:
        """Tracked 41-class mapping used by the original BioBERT notebook."""
        return DISEASE_MODEL_DIR / "disease2id.json"

    @staticmethod
    def _read_label_mapping(path):
        with Path(path).open(encoding="utf-8") as file:
            raw_mapping = json.load(file)
        if not isinstance(raw_mapping, dict) or not raw_mapping:
            raise ValueError("disease2id.json must be a non-empty JSON object")

        mapping = {str(name): int(label_id) for name, label_id in raw_mapping.items()}
        ids = sorted(mapping.values())
        if ids != list(range(len(mapping))):
            raise ValueError("Disease label IDs must be unique and contiguous from 0")
        return mapping

    def _set_mapping(self, mapping):
        self.disease2id = mapping
        self.num_labels = len(mapping)
        self.id2disease = {
            label_id: name for name, label_id in mapping.items()
        }

    def _load_preferred_artifacts(self):
        from transformers import AutoModelForSequenceClassification, AutoTokenizer

        mapping_path = self.artifact_dir / "disease2id.json"
        config_path = self.artifact_dir / "config.json"
        mapping = self._read_label_mapping(mapping_path)

        with config_path.open(encoding="utf-8") as file:
            model_config = json.load(file)
        configured_labels = model_config.get("num_labels")
        if configured_labels != len(mapping):
            raise ValueError(
                "Checkpoint label count does not match disease2id.json "
                f"({configured_labels} != {len(mapping)}). Retrain the model."
            )

        tokenizer = AutoTokenizer.from_pretrained(
            str(self.artifact_dir), local_files_only=True
        )
        model = AutoModelForSequenceClassification.from_pretrained(
            str(self.artifact_dir), local_files_only=True
        )
        if model.config.num_labels != len(mapping):
            raise ValueError(
                "Loaded classifier head does not match disease2id.json. "
                "Retrain the model and replace the complete artifact directory."
            )

        self._set_mapping(mapping)
        self.tokenizer = tokenizer
        self.model = model.to(self.device)
        self.model.eval()

    def _load_legacy_checkpoint(self):
        """Load the old .pt checkpoint only against its tracked 41-class mapping.

        Strict state-dict loading checks classifier tensor dimensions. If the
        downloaded checkpoint is not the 41-class notebook checkpoint, loading
        fails closed instead of guessing the label order.
        """
        from transformers import AutoModelForSequenceClassification, AutoTokenizer

        mapping = self._read_label_mapping(self.legacy_mapping_path)
        tokenizer = AutoTokenizer.from_pretrained(BIOBERT_MODEL)
        model = AutoModelForSequenceClassification.from_pretrained(
            BIOBERT_MODEL, num_labels=len(mapping)
        )

        try:
            state_dict = torch.load(
                self.legacy_checkpoint_path,
                map_location="cpu",
                weights_only=True,
            )
        except TypeError as exc:
            raise RuntimeError(
                "This PyTorch version does not support safe weights_only loading. "
                "Upgrade PyTorch before loading the legacy model checkpoint."
            ) from exc

        if isinstance(state_dict, dict) and isinstance(state_dict.get("state_dict"), dict):
            state_dict = state_dict["state_dict"]
        if not isinstance(state_dict, dict):
            raise ValueError("Legacy BioBERT checkpoint is not a state dictionary")

        model.load_state_dict(state_dict, strict=True)
        if model.config.num_labels != len(mapping):
            raise ValueError("Legacy BioBERT classifier head does not match its label map")

        self._set_mapping(mapping)
        self.tokenizer = tokenizer
        self.model = model.to(self.device)
        self.model.eval()
        print(
            "Loaded legacy BioBERT checkpoint against the tracked "
            f"{self.num_labels}-class mapping"
        )

    def load(self):
        """Prefer self-contained artifacts, then safely try the legacy checkpoint."""
        self.is_ready = False
        self.model = None
        self.tokenizer = None
        self.disease2id = {}
        self.id2disease = {}
        self.num_labels = 0

        mapping_path = self.artifact_dir / "disease2id.json"
        config_path = self.artifact_dir / "config.json"
        try:
            if mapping_path.is_file() and config_path.is_file():
                self._load_preferred_artifacts()
            elif (
                self.legacy_checkpoint_path.is_file()
                and self.legacy_mapping_path.is_file()
            ):
                self._load_legacy_checkpoint()
            else:
                print(
                    "BioBERT disease artifacts are missing. Download the legacy "
                    "checkpoint or train with scripts/training/train_disease_predictor.py."
                )
                return

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
