"""Customer churn analysis pipeline.

This script cleans Telco churn data, calculates churn metrics by segment,
and trains a simple baseline model for churn risk prioritization.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


DATA_PATH = Path("WA_Fn-UseC_-Telco-Customer-Churn.csv")
RANDOM_STATE = 42
TARGET_COLUMN = "Churn"


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load customer churn data."""
    return pd.read_csv(path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean churn dataset and prepare target variable."""
    clean_df = df.copy()
    clean_df.columns = clean_df.columns.str.strip()

    clean_df["TotalCharges"] = pd.to_numeric(clean_df["TotalCharges"], errors="coerce")
    clean_df = clean_df.dropna(subset=["TotalCharges"])
    clean_df["churn_flag"] = clean_df[TARGET_COLUMN].map({"Yes": 1, "No": 0})

    return clean_df


def calculate_churn_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate overall churn summary."""
    total_customers = df["customerID"].nunique()
    churned_customers = int(df["churn_flag"].sum())
    churn_rate = churned_customers / total_customers

    return pd.DataFrame(
        [
            {
                "total_customers": total_customers,
                "churned_customers": churned_customers,
                "churn_rate": churn_rate,
                "avg_monthly_charges": df["MonthlyCharges"].mean(),
                "monthly_revenue_exposure": df.loc[
                    df["churn_flag"] == 1, "MonthlyCharges"
                ].sum(),
            }
        ]
    )


def calculate_segment_churn(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Calculate churn rate by a selected segment column."""
    segment_summary = (
        df.groupby(column)
        .agg(
            customers=("customerID", "nunique"),
            churned_customers=("churn_flag", "sum"),
            avg_monthly_charges=("MonthlyCharges", "mean"),
        )
        .reset_index()
    )

    segment_summary["churn_rate"] = (
        segment_summary["churned_customers"] / segment_summary["customers"]
    )

    return segment_summary.sort_values("churn_rate", ascending=False)


def build_model_pipeline(df: pd.DataFrame) -> tuple[Pipeline, list[str], list[str]]:
    """Create preprocessing and logistic regression pipeline."""
    excluded_columns = {"customerID", TARGET_COLUMN, "churn_flag"}
    feature_columns = [col for col in df.columns if col not in excluded_columns]

    numeric_features = df[feature_columns].select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_features = [col for col in feature_columns if col not in numeric_features]

    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", StandardScaler(), numeric_features),
            ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)),
        ]
    )

    return model, numeric_features, categorical_features


def train_baseline_model(df: pd.DataFrame) -> dict[str, object]:
    """Train and evaluate a baseline churn model."""
    model, numeric_features, categorical_features = build_model_pipeline(df)

    excluded_columns = {"customerID", TARGET_COLUMN, "churn_flag"}
    feature_columns = [col for col in df.columns if col not in excluded_columns]

    x = df[feature_columns]
    y = df["churn_flag"]

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.25,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    y_proba = model.predict_proba(x_test)[:, 1]

    return {
        "model": model,
        "roc_auc": roc_auc_score(y_test, y_proba),
        "confusion_matrix": confusion_matrix(y_test, y_pred),
        "classification_report": classification_report(y_test, y_pred),
        "numeric_features": numeric_features,
        "categorical_features": categorical_features,
    }


def print_summary(
    overall_summary: pd.DataFrame,
    contract_summary: pd.DataFrame,
    payment_summary: pd.DataFrame,
    model_results: dict[str, object],
) -> None:
    """Print concise churn analysis summary."""
    print("Customer Churn Analysis Summary")
    print("=" * 80)
    print(overall_summary.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\nChurn by Contract")
    print(contract_summary.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\nChurn by Payment Method")
    print(payment_summary.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\nBaseline Model")
    print(f"ROC-AUC: {model_results['roc_auc']:.4f}")
    print("Confusion matrix:")
    print(model_results["confusion_matrix"])
    print("\nClassification report:")
    print(model_results["classification_report"])


def main() -> None:
    """Run the churn analysis pipeline."""
    raw_df = load_data()
    clean_df = clean_data(raw_df)

    overall_summary = calculate_churn_summary(clean_df)
    contract_summary = calculate_segment_churn(clean_df, "Contract")
    payment_summary = calculate_segment_churn(clean_df, "PaymentMethod")
    model_results = train_baseline_model(clean_df)

    print_summary(overall_summary, contract_summary, payment_summary, model_results)


if __name__ == "__main__":
    main()
