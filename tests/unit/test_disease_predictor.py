import json

import pytest

from models.disease_predictor.model import DiseasePredictorModel


def test_model_not_ready_without_checkpoint_metadata(tmp_path, monkeypatch):
    monkeypatch.setattr(
        DiseasePredictorModel,
        "artifact_dir",
        property(lambda self: tmp_path),
    )
    predictor = DiseasePredictorModel()
    predictor.load()
    assert predictor.is_ready is False
    assert predictor.model is None


def test_rejects_non_contiguous_label_ids(tmp_path, monkeypatch):
    monkeypatch.setattr(
        DiseasePredictorModel,
        "artifact_dir",
        property(lambda self: tmp_path),
    )
    (tmp_path / "disease2id.json").write_text(
        json.dumps({"condition-a": 0, "condition-b": 2}),
        encoding="utf-8",
    )
    (tmp_path / "config.json").write_text(
        json.dumps({"num_labels": 2}),
        encoding="utf-8",
    )

    predictor = DiseasePredictorModel()
    predictor.load()

    assert predictor.is_ready is False
    assert predictor.model is None
    assert "condition-a" not in predictor.id2disease.values()


def test_rejects_label_count_mismatch_before_loading_transformers(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(
        DiseasePredictorModel,
        "artifact_dir",
        property(lambda self: tmp_path),
    )
    (tmp_path / "disease2id.json").write_text(
        json.dumps({"condition-a": 0, "condition-b": 1}),
        encoding="utf-8",
    )
    (tmp_path / "config.json").write_text(
        json.dumps({"num_labels": 41}),
        encoding="utf-8",
    )

    predictor = DiseasePredictorModel()
    predictor.load()

    assert predictor.is_ready is False
    assert predictor.model is None


def test_loads_legacy_checkpoint_only_with_matching_tracked_mapping(
    tmp_path, monkeypatch
):
    import sys
    import types
    import torch

    from types import SimpleNamespace

    class FakeModel(torch.nn.Module):
        def __init__(self, num_labels):
            super().__init__()
            self.classifier = torch.nn.Linear(2, num_labels)
            self.config = SimpleNamespace(num_labels=num_labels)

        def forward(self, **inputs):
            return SimpleNamespace(logits=torch.zeros(1, self.config.num_labels))

    class FakeAutoModel:
        @staticmethod
        def from_pretrained(model_name, num_labels):
            return FakeModel(num_labels)

    class FakeAutoTokenizer:
        @staticmethod
        def from_pretrained(model_name):
            return object()

    fake_transformers = types.ModuleType("transformers")
    fake_transformers.AutoModelForSequenceClassification = FakeAutoModel
    fake_transformers.AutoTokenizer = FakeAutoTokenizer
    monkeypatch.setitem(sys.modules, "transformers", fake_transformers)

    mapping_path = tmp_path / "disease2id.json"
    mapping_path.write_text(
        json.dumps({"condition-a": 0, "condition-b": 1}),
        encoding="utf-8",
    )
    checkpoint_path = tmp_path / "disease_predictor.pt"
    torch.save(
        {
            "classifier.weight": torch.zeros(2, 2),
            "classifier.bias": torch.zeros(2),
        },
        checkpoint_path,
    )

    monkeypatch.setattr(
        DiseasePredictorModel,
        "artifact_dir",
        property(lambda self: tmp_path / "new-format-does-not-exist"),
    )
    monkeypatch.setattr(
        DiseasePredictorModel,
        "legacy_mapping_path",
        property(lambda self: mapping_path),
    )
    monkeypatch.setattr(
        DiseasePredictorModel,
        "legacy_checkpoint_path",
        property(lambda self: checkpoint_path),
    )

    predictor = DiseasePredictorModel()
    predictor.load()

    assert predictor.is_ready is True
    assert predictor.num_labels == 2
    assert predictor.id2disease == {0: "condition-a", 1: "condition-b"}
