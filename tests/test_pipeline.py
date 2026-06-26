import pandas as pd

from src.features import BASE_FEATURES, ENGINEERED_FEATURES
from src.pipeline import build_retraining_dataset


def test_build_retraining_dataset_keeps_only_validated_rows():
    validated = {feature: 5 for feature in BASE_FEATURES}
    pending = {feature: 2 for feature in BASE_FEATURES}
    df = pd.DataFrame(
        [
            {**validated, "prediction_id": "valid", "actual_value": 0.7, "prediction": 0.65},
            {**pending, "prediction_id": "pending", "actual_value": None, "prediction": 0.25},
        ]
    )

    result = build_retraining_dataset(df, BASE_FEATURES)

    assert len(result) == 1
    assert result.loc[0, "FloodProbability"] == 0.7
    assert all(feature in result.columns for feature in BASE_FEATURES)
    assert all(feature in result.columns for feature in ENGINEERED_FEATURES)
    assert "prediction" not in result.columns


def test_build_retraining_dataset_returns_empty_when_target_is_missing():
    df = pd.DataFrame([{feature: 5 for feature in BASE_FEATURES}])

    result = build_retraining_dataset(df, BASE_FEATURES)

    assert result.empty
