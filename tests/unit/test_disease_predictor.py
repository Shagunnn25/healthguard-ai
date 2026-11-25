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
