import pandas as pd


BASE_FEATURES = [
    "MonsoonIntensity",
    "TopographyDrainage",
    "RiverManagement",
    "Deforestation",
    "Urbanization",
    "ClimateChange",
    "DamsQuality",
    "Siltation",
    "AgriculturalPractices",
    "Encroachments",
    "IneffectiveDisasterPreparedness",
    "DrainageSystems",
    "CoastalVulnerability",
    "Landslides",
    "Watersheds",
    "DeterioratingInfrastructure",
    "PopulationScore",
    "WetlandLoss",
    "InadequatePlanning",
    "PoliticalFactors",
]

ENGINEERED_FEATURES = [
    "risk_score_sum",
    "risk_score_mean",
    "water_pressure_risk",
    "environmental_risk",
    "infrastructure_risk",
    "planning_risk",
    "exposure_risk",
]


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create domain features from the original flood-risk factors."""
    engineered_df = df.copy()
    available_base = [col for col in BASE_FEATURES if col in engineered_df.columns]
    if not available_base:
        return engineered_df

    engineered_df[available_base] = engineered_df[available_base].apply(pd.to_numeric, errors="coerce")
    engineered_df["risk_score_sum"] = engineered_df[available_base].sum(axis=1)
    engineered_df["risk_score_mean"] = engineered_df[available_base].mean(axis=1)

    engineered_df["water_pressure_risk"] = _mean_available(
        engineered_df,
        ["MonsoonIntensity", "TopographyDrainage", "RiverManagement", "Siltation", "Watersheds"],
    )
    engineered_df["environmental_risk"] = _mean_available(
        engineered_df,
        ["Deforestation", "WetlandLoss", "ClimateChange", "AgriculturalPractices"],
    )
    engineered_df["infrastructure_risk"] = _mean_available(
        engineered_df,
        ["DamsQuality", "DrainageSystems", "DeterioratingInfrastructure"],
    )
    engineered_df["planning_risk"] = _mean_available(
        engineered_df,
        ["Urbanization", "InadequatePlanning", "Encroachments", "PoliticalFactors"],
    )
    engineered_df["exposure_risk"] = _mean_available(
        engineered_df,
        ["PopulationScore", "CoastalVulnerability", "Landslides", "IneffectiveDisasterPreparedness"],
    )
    return engineered_df


def summarize_engineered_features(df: pd.DataFrame) -> dict[str, float]:
    engineered_df = add_engineered_features(df)
    return {
        feature: float(engineered_df[feature].iloc[0])
        for feature in ENGINEERED_FEATURES
        if feature in engineered_df.columns and pd.notna(engineered_df[feature].iloc[0])
    }


def _mean_available(df: pd.DataFrame, columns: list[str]) -> pd.Series:
    available = [col for col in columns if col in df.columns]
    if not available:
        return pd.Series([0.0] * len(df), index=df.index)
    return df[available].mean(axis=1)
