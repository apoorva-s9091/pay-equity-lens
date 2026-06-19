"""
salary_predictor.py
Salary Benchmarking & Pay Equity Model for Pay Equity Lens.

Use Case:
    Predicts the 'fair market salary' for each employee based on their 
    qualifications and role. Flags employees who are significantly under 
    or over the predicted benchmark — enabling HR to identify pay inequities.

Models Trained:
    - Linear Regression (baseline)
    - Ridge Regression
    - Random Forest Regressor  ← Best MAE
    - Gradient Boosting Regressor ← Best R²

Output:
    - Trained model saved to model/salary_rf_model.pkl
    - Predictions appended to data/processed/hr_with_predictions.csv
    - Feature importance chart saved to reports/
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import warnings
import json
import pickle
from pathlib import Path
warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE = Path(__file__).parent.parent
DATA_PATH = BASE / "data" / "processed" / "hr_clean.csv"
OUTPUT_PATH = BASE / "data" / "processed" / "hr_with_predictions.csv"
MODEL_PATH = BASE / "model" / "salary_rf_model.pkl"
RESULTS_PATH = BASE / "model" / "model_results.json"

# ── Feature config ─────────────────────────────────────────────────────────────
CATEGORICAL_COLS = ["Department", "Gender", "JobRole", "MaritalStatus",
                    "BusinessTravel", "OverTime", "EducationField", "Attrition"]
FEATURE_COLS = [
    "Age", "Education", "JobLevel", "JobSatisfaction", "TotalWorkingYears",
    "WorkLifeBalance", "YearsAtCompany", "YearsInCurrentRole",
    "TrainingTimesLastYear", "PerformanceRating",
    "Department_enc", "Gender_enc", "JobRole_enc", "MaritalStatus_enc",
    "BusinessTravel_enc", "OverTime_enc",
]
TARGET_COL = "MonthlyIncome"
UNDERPAID_THRESHOLD = -500   # $500 below predicted = underpaid
OVERPAID_THRESHOLD  =  500   # $500 above predicted = overpaid

FEATURE_LABELS = {
    "JobLevel": "Job Level", "TotalWorkingYears": "Total Working Years",
    "YearsAtCompany": "Years at Company", "Age": "Age",
    "YearsInCurrentRole": "Years in Role", "JobRole_enc": "Job Role",
    "Department_enc": "Department", "Education": "Education",
    "Gender_enc": "Gender", "PerformanceRating": "Performance Rating",
    "BusinessTravel_enc": "Business Travel", "JobSatisfaction": "Job Satisfaction",
    "MaritalStatus_enc": "Marital Status", "OverTime_enc": "Overtime",
    "WorkLifeBalance": "Work-Life Balance", "TrainingTimesLastYear": "Training Times",
}


def encode_features(df: pd.DataFrame) -> pd.DataFrame:
    """Label-encode categorical columns."""
    df = df.copy()
    le = LabelEncoder()
    for col in CATEGORICAL_COLS:
        if col in df.columns:
            df[f"{col}_enc"] = le.fit_transform(df[col].astype(str))
    return df


def train_and_evaluate(df: pd.DataFrame) -> dict:
    """Train all models, return results dict."""
    df = encode_features(df)
    X = df[FEATURE_COLS]
    y = df[TARGET_COL]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc  = scaler.transform(X_test)

    models = {
        "Linear Regression":    LinearRegression(),
        "Ridge Regression":     Ridge(alpha=10),
        "Random Forest":        RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42),
        "Gradient Boosting":    GradientBoostingRegressor(n_estimators=200, max_depth=5, random_state=42),
    }

    results = {}
    for name, model in models.items():
        use_scaled = "Regression" in name
        model.fit(X_train_sc if use_scaled else X_train,
                  y_train)
        preds = model.predict(X_test_sc if use_scaled else X_test)

        results[name] = {
            "model":  model,
            "MAE":    float(mean_absolute_error(y_test, preds)),
            "RMSE":   float(np.sqrt(mean_squared_error(y_test, preds))),
            "R2":     float(r2_score(y_test, preds)),
            "preds":  preds,
            "y_test": y_test.values,
        }
        print(f"{name:25s} → MAE=${results[name]['MAE']:,.0f} | "
              f"RMSE=${results[name]['RMSE']:,.0f} | R²={results[name]['R2']:.4f}")

    return results, models, scaler, X, y


def flag_pay_equity(df: pd.DataFrame, rf_model, X: pd.DataFrame) -> pd.DataFrame:
    """Predict fair salary and flag under/over-paid employees."""
    df = df.copy()
    df["PredictedFairSalary"] = rf_model.predict(X).astype(int)
    df["SalaryGap"]  = df[TARGET_COL] - df["PredictedFairSalary"]
    df["Underpaid"]  = df["SalaryGap"] < UNDERPAID_THRESHOLD
    df["Overpaid"]   = df["SalaryGap"] > OVERPAID_THRESHOLD
    df["PayStatus"]  = "Fair"
    df.loc[df["Underpaid"], "PayStatus"] = "Underpaid"
    df.loc[df["Overpaid"],  "PayStatus"] = "Overpaid"
    return df


def save_outputs(results: dict, df_final: pd.DataFrame, rf_model, scaler):
    """Save model, predictions, and results JSON."""
    # Save model
    with open(MODEL_PATH, "wb") as f:
        pickle.dump({"model": rf_model, "scaler": scaler}, f)

    # Save predictions
    df_final.to_csv(OUTPUT_PATH, index=False)

    # Save metrics (no non-serialisable objects)
    metrics = {k: {m: v for m, v in r.items() if m not in ("model", "preds", "y_test")}
               for k, r in results.items()}
    with open(RESULTS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"\nModel saved → {MODEL_PATH}")
    print(f"Predictions saved → {OUTPUT_PATH}")
    print(f"Metrics saved → {RESULTS_PATH}")


def generate_charts(results: dict, rf_model, df_final: pd.DataFrame):
    """Generate and save model evaluation charts."""
    DARK_BG, PANEL_BG = "#0f1117", "#1a1d2e"
    plt.rcParams.update({
        "figure.facecolor": DARK_BG, "axes.facecolor": PANEL_BG,
        "axes.labelcolor": "white", "xtick.color": "white", "ytick.color": "white",
        "text.color": "white", "axes.titlecolor": "white",
        "axes.edgecolor": "#333355", "grid.color": "#333355",
    })

    # Feature Importance
    fi = pd.Series(rf_model.feature_importances_, index=FEATURE_COLS).sort_values()
    fi.index = [FEATURE_LABELS.get(i, i) for i in fi.index]

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor(DARK_BG)

    bar_cols = ["#7B5EA7" if v > fi.mean() else "#54A0E0" for v in fi.values]
    axes[0].barh(fi.index, fi.values, color=bar_cols, edgecolor=DARK_BG)
    axes[0].set_title("Feature Importance\n(Random Forest Salary Predictor)", fontweight="bold")
    axes[0].set_xlabel("Importance Score")
    axes[0].grid(True, alpha=0.3, axis="x")

    rf_res = results["Random Forest"]
    axes[1].scatter(rf_res["y_test"], rf_res["preds"], alpha=0.4, s=15, c="#7B5EA7")
    mn, mx = rf_res["y_test"].min(), rf_res["y_test"].max()
    axes[1].plot([mn, mx], [mn, mx], "r--", lw=2, label="Perfect Prediction")
    axes[1].set_title(f'Actual vs Predicted Salary\nR² = {rf_res["R2"]:.4f}', fontweight="bold")
    axes[1].set_xlabel("Actual Monthly Income ($)")
    axes[1].set_ylabel("Predicted Monthly Income ($)")
    axes[1].legend(facecolor=PANEL_BG, labelcolor="white")
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(BASE / "reports" / "fig5_model_results.png",
                dpi=150, bbox_inches="tight", facecolor=DARK_BG)
    plt.close()
    print("Model chart saved.")


if __name__ == "__main__":
    print("=" * 55)
    print("  Pay Equity Lens — Salary Benchmarking Model")
    print("=" * 55)

    df = pd.read_csv(DATA_PATH)
    results, models, scaler, X, y = train_and_evaluate(df)

    rf_model = models["Random Forest"]
    df_enc = encode_features(df)
    X_all = df_enc[FEATURE_COLS]

    df_final = flag_pay_equity(df_enc, rf_model, X_all)

    print(f"\nUnderpaid employees : {df_final['Underpaid'].sum()} "
          f"({df_final['Underpaid'].mean()*100:.1f}%)")
    print(f"Overpaid employees  : {df_final['Overpaid'].sum()} "
          f"({df_final['Overpaid'].mean()*100:.1f}%)")
    print(f"\nUnderpaid by Gender:")
    print((df_final.groupby('Gender')['Underpaid'].mean()*100).to_string())
    print(f"\nUnderpaid by Department:")
    print((df_final.groupby('Department')['Underpaid'].mean()*100).to_string())

    save_outputs(results, df_final, rf_model, scaler)
    generate_charts(results, rf_model, df_final)
    print("\nDone.")
