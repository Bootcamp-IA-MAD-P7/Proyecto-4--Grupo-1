from __future__ import annotations

import pandas as pd

from src.features import add_engineered_features


def build_retraining_dataset(new_data_df: pd.DataFrame, feature_columns: list[str]) -> pd.DataFrame:
    if new_data_df.empty:
        return pd.DataFrame()

    required_cols = [*feature_columns, "actual_value"]
    missing_cols = [col for col in required_cols if col not in new_data_df.columns]
    if missing_cols:
        return pd.DataFrame()

    validated_df = new_data_df.dropna(subset=["actual_value"]).copy()
    if "record_status" in validated_df.columns:
        validated_df = validated_df[
            validated_df["record_status"].astype(str) != "ingested_for_retraining"
        ].copy()

    if validated_df.empty:
        return pd.DataFrame()

    retraining_df = add_engineered_features(validated_df[feature_columns].copy())
    retraining_df["FloodProbability"] = validated_df["actual_value"].astype(float)
    return retraining_df
