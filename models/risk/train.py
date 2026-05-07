import pandas as pd
import numpy as np
import joblib
import mlflow
import mlflow.sklearn

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from utils.mlflow_config import setup_mlflow


MODEL_PATH = "models/risk/risk_model.pkl"
SCALER_PATH = "models/risk/scaler.pkl"


def generate_dataset(n_samples=1000):
    data = []

    for _ in range(n_samples):

        revenue = np.random.randint(5000, 200000)

        growth_rate = np.random.uniform(
            -0.5,
            1.5
        )

        burn_rate = np.random.randint(
            1000,
            150000
        )

        market_score = np.random.uniform(
            0,
            1
        )

        burn_ratio = burn_rate / revenue

        risk_score = 0

        if growth_rate < 0:
            risk_score += 1

        if burn_ratio > 1:
            risk_score += 1

        if market_score < 0.4:
            risk_score += 1

        if growth_rate > 0.4 and burn_ratio < 0.5:
            risk_score -= 1

        risk = 1 if risk_score >= 2 else 0

        data.append([
            revenue,
            growth_rate,
            burn_rate,
            market_score,
            risk
        ])

    df = pd.DataFrame(
        data,
        columns=[
            "revenue",
            "growth_rate",
            "burn_rate",
            "market_score",
            "risk"
        ]
    )

    return df


def train_model(df):

    setup_mlflow("risk_prediction_experiment")

    with mlflow.start_run():

        X = df[
            [
                "revenue",
                "growth_rate",
                "burn_rate",
                "market_score"
            ]
        ]

        y = df["risk"]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

        scaler = StandardScaler()

        X_train_scaled = scaler.fit_transform(
            X_train
        )

        X_test_scaled = scaler.transform(
            X_test
        )

        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=8,
            random_state=42
        )

        model.fit(
            X_train_scaled,
            y_train
        )

        preds = model.predict(X_test_scaled)

        accuracy = accuracy_score(
            y_test,
            preds
        )

        print(f"Accuracy: {accuracy:.4f}")

        mlflow.log_param("n_estimators", 200)
        mlflow.log_param("max_depth", 8)

        mlflow.log_metric("accuracy", accuracy)

        mlflow.sklearn.log_model(
            model,
            "risk_model"
        )

        joblib.dump(
            model,
            MODEL_PATH
        )

        joblib.dump(
            scaler,
            SCALER_PATH
        )

        mlflow.log_artifact(MODEL_PATH)
        mlflow.log_artifact(SCALER_PATH)

        print("Risk model saved.")
        print("Scaler saved.")


if __name__ == "__main__":

    df = generate_dataset()

    train_model(df)