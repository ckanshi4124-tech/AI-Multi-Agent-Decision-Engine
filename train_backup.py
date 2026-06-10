import torch
import torch.nn as nn
import numpy as np
import joblib
import mlflow
import mlflow.pytorch

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

from models.forecasting.preprocess import (
    load_data,
    preprocess_data,
    create_sequences
)

from models.forecasting.model import LSTMModel

from utils.mlflow_config import setup_mlflow


MODEL_PATH = "models/forecasting/forecast_model.pt"
SCALER_PATH = "models/forecasting/scaler.pkl"


def train_model(X, y):

    setup_mlflow("forecasting_experiment")

    with mlflow.start_run():

        device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        X_train, X_val, y_train, y_val = train_test_split(
            X,
            y,
            test_size=0.2,
            shuffle=False
        )

        X_train = torch.tensor(
            X_train,
            dtype=torch.float32
        ).to(device)

        y_train = torch.tensor(
            y_train,
            dtype=torch.float32
        ).to(device)

        X_val = torch.tensor(
            X_val,
            dtype=torch.float32
        ).to(device)

        y_val = torch.tensor(
            y_val,
            dtype=torch.float32
        ).to(device)

        model = LSTMModel().to(device)

        criterion = nn.MSELoss()

        optimizer = torch.optim.Adam(
            model.parameters(),
            lr=0.001
        )

        epochs = 40

        mlflow.log_param("epochs", epochs)
        mlflow.log_param("learning_rate", 0.001)

        best_loss = float("inf")

        for epoch in range(epochs):

            model.train()

            outputs = model(X_train)

            loss = criterion(outputs, y_train)

            optimizer.zero_grad()

            loss.backward()

            torch.nn.utils.clip_grad_norm_(
                model.parameters(),
                max_norm=1.0
            )

            optimizer.step()

            model.eval()

            with torch.no_grad():

                val_outputs = model(X_val)

                val_loss = criterion(
                    val_outputs,
                    y_val
                )

            if val_loss.item() < best_loss:

                best_loss = val_loss.item()

                torch.save(
                    model.state_dict(),
                    MODEL_PATH
                )

            print(
                f"Epoch {epoch+1}/{epochs} | "
                f"Train Loss: {loss.item():.6f} | "
                f"Val Loss: {val_loss.item():.6f}"
            )

        model.load_state_dict(
            torch.load(
                MODEL_PATH,
                map_location=device
            )
        )

        model.eval()

        with torch.no_grad():

            preds = model(X_val).cpu().numpy()

        actual = y_val.cpu().numpy()

        rmse = np.sqrt(
            mean_squared_error(actual, preds)
        )

        print(f"Validation RMSE: {rmse:.4f}")

        mlflow.log_metric("rmse", rmse)

        mlflow.pytorch.log_model(
            pytorch_model=model,
            artifact_path="forecast_model"
        )

        mlflow.log_artifact(MODEL_PATH)

        return model


if __name__ == "__main__":

    train, stores = load_data()

    df = preprocess_data(train, stores)

    X, y, scaler = create_sequences(df)

    model = train_model(X, y)

    joblib.dump(
        scaler,
        SCALER_PATH
    )

    mlflow.log_artifact(SCALER_PATH)

    print("Forecast model saved.")
    print("Scaler saved.")