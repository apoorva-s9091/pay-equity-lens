"""
data_loader.py
Reusable data loading and preprocessing utilities for Pay Equity Lens.
"""

import pandas as pd
import numpy as np
from pathlib import Path

RAW_PATH = Path(__file__).parent.parent / "data" / "raw" / "hr_raw.csv"
PROCESSED_PATH = Path(__file__).parent.parent / "data" / "processed" / "hr_clean.csv"
PREDICTIONS_PATH = Path(__file__).parent.parent / "data" / "processed" / "hr_with_predictions.csv"

EDUCATION_MAP = {1: "Below College", 2: "College", 3: "Bachelor", 4: "Master", 5: "Doctor"}
JOB_SATISFACTION_MAP = {1: "Low", 2: "Medium", 3: "High", 4: "Very High"}
WORK_LIFE_BALANCE_MAP = {1: "Bad", 2: "Good", 3: "Better", 4: "Best"}
PERFORMANCE_MAP = {1: "Low", 2: "Good", 3: "Excellent", 4: "Outstanding"}
JOB_LEVEL_MAP = {1: "Junior", 2: "Mid", 3: "Senior", 4: "Lead", 5: "Executive"}


def load_raw() -> pd.DataFrame:
    """Load the raw HR dataset."""
    return pd.read_csv(RAW_PATH)


def load_clean() -> pd.DataFrame:
    """Load the cleaned and processed HR dataset."""
    return pd.read_csv(PROCESSED_PATH)


def load_with_predictions() -> pd.DataFrame:
    """Load the dataset with model salary predictions."""
    return pd.read_csv(PREDICTIONS_PATH)


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply label mappings and feature engineering to raw DataFrame.
    Returns enriched DataFrame.
    """
    df = df.copy()

    # Ordinal label mappings
    df["EducationLabel"] = df["Education"].map(EDUCATION_MAP)
    df["JobSatisfactionLabel"] = df["JobSatisfaction"].map(JOB_SATISFACTION_MAP)
    df["WorkLifeBalanceLabel"] = df["WorkLifeBalance"].map(WORK_LIFE_BALANCE_MAP)
    df["PerformanceLabel"] = df["PerformanceRating"].map(PERFORMANCE_MAP)
    df["JobLevelLabel"] = df["JobLevel"].map(JOB_LEVEL_MAP)

    # Sanity checks
    assert df["MonthlyIncome"].min() > 0, "Negative salaries found."
    assert df.isnull().sum().sum() == 0, "Null values found after preprocessing."

    return df


def get_pay_gap_summary(df: pd.DataFrame) -> dict:
    """Return a dictionary of key pay gap metrics."""
    male_avg = df[df["Gender"] == "Male"]["MonthlyIncome"].mean()
    female_avg = df[df["Gender"] == "Female"]["MonthlyIncome"].mean()
    gap_pct = ((male_avg - female_avg) / male_avg) * 100

    return {
        "total_employees": len(df),
        "male_avg_salary": round(male_avg, 2),
        "female_avg_salary": round(female_avg, 2),
        "pay_gap_pct": round(gap_pct, 2),
        "overall_avg_salary": round(df["MonthlyIncome"].mean(), 2),
    }


if __name__ == "__main__":
    df = load_raw()
    df = preprocess(df)
    df.to_csv(PROCESSED_PATH, index=False)
    print(f"Processed dataset saved: {df.shape}")
    print(get_pay_gap_summary(df))
