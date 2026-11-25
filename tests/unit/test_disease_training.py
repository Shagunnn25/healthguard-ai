import pandas as pd
import pytest

from scripts.training.train_disease_predictor import load_training_data


def test_training_data_builds_deterministic_mapping(tmp_path, monkeypatch):
    import scripts.training.train_disease_predictor as training

    csv_path = tmp_path / "symptoms_diseases_clean.csv"
    pd.DataFrame(
        {
            "disease": ["zeta", "alpha", "zeta", "alpha"],
            "symptoms_text": ["cough", "rash", "fever", "itching"],
        }
    ).to_csv(csv_path, index=False)
    monkeypatch.setattr(training, "CLEANED_SYMPTOM", tmp_path)

    frame, mapping = load_training_data()

    assert mapping == {"alpha": 0, "zeta": 1}
    assert frame["label"].tolist() == [1, 0, 1, 0]


def test_training_data_rejects_singleton_class(tmp_path, monkeypatch):
    import scripts.training.train_disease_predictor as training

    csv_path = tmp_path / "symptoms_diseases_clean.csv"
    pd.DataFrame(
        {
            "disease": ["alpha", "alpha", "beta"],
            "symptoms_text": ["rash", "itching", "cough"],
        }
    ).to_csv(csv_path, index=False)
    monkeypatch.setattr(training, "CLEANED_SYMPTOM", tmp_path)

    with pytest.raises(ValueError, match="at least two rows per disease"):
        load_training_data()


def test_training_data_reports_missing_dataset(tmp_path, monkeypatch):
    import scripts.training.train_disease_predictor as training

    monkeypatch.setattr(training, "CLEANED_SYMPTOM", tmp_path)

    with pytest.raises(FileNotFoundError, match="Run scripts/data_cleaning"):
        load_training_data()
