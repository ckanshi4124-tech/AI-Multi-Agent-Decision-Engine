import pandas as pd
from scipy.stats import ks_2samp


def detect_drift(reference_data: pd.Series,
                 current_data: pd.Series,
                 threshold: float = 0.05):
    """
    Perform KS test to detect drift.
    Returns:
        p_value: float
        drift_detected: bool
    """
    statistic, p_value = ks_2samp(reference_data, current_data)
    drift_detected = p_value < threshold
    return {
        "p_value": float(p_value),
        "drift_detected": bool(drift_detected)
    }


def compare_datasets(reference_df: pd.DataFrame,
                     current_df: pd.DataFrame):
    """
    Compare all numeric columns present in both datasets.
    """
    results = {}

    common_columns = [
        col for col in reference_df.columns
        if col in current_df.columns
        and pd.api.types.is_numeric_dtype(reference_df[col])
    ]

    for col in common_columns:
        results[col] = detect_drift(
            reference_df[col].dropna(),
            current_df[col].dropna()
        )

    return results
    