import pandas as pd

from src.features import BASE_FEATURES, ENGINEERED_FEATURES, add_engineered_features, summarize_engineered_features


def test_add_engineered_features_creates_expected_indicators():
    df = pd.DataFrame([{feature: 5 for feature in BASE_FEATURES}])

    result = add_engineered_features(df)

    assert all(feature in result.columns for feature in ENGINEERED_FEATURES)
    assert result.loc[0, "risk_score_sum"] == 100
    assert result.loc[0, "risk_score_mean"] == 5
    assert result.loc[0, "water_pressure_risk"] == 5
    assert result.loc[0, "environmental_risk"] == 5
    assert result.loc[0, "infrastructure_risk"] == 5
    assert result.loc[0, "planning_risk"] == 5
    assert result.loc[0, "exposure_risk"] == 5


def test_summarize_engineered_features_returns_numeric_summary():
    df = pd.DataFrame([{feature: 3 for feature in BASE_FEATURES}])

    summary = summarize_engineered_features(df)

    assert set(summary) == set(ENGINEERED_FEATURES)
    assert summary["risk_score_sum"] == 60
    assert summary["risk_score_mean"] == 3
