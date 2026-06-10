import torch
import numpy as np
import joblib

from models.forecasting.model import LSTMModel

MODEL_PATH = "models/forecasting/forecast_model.pt"
SCALER_PATH = "models/forecasting/scaler.pkl"

SEQ_LENGTH = 12
FUTURE_STEPS = 3

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

model = LSTMModel().to(device)

try:
    model.load_state_dict(
        torch.load(
            MODEL_PATH,
            map_location=device
        )
    )

    model.eval()

except Exception:
    model = None

try:
    scaler = joblib.load(SCALER_PATH)

except Exception:
    scaler = None

def detect_trend(sequence):
    diffs = np.diff(sequence)

    slope = np.polyfit(
        range(len(sequence)),
        sequence,
        1
    )[0]

    volatility = (
        np.std(diffs)
        if len(diffs) > 1
        else 0
    )

    mean_val = np.mean(np.abs(sequence)) + 1e-6

    normalized_volatility = volatility / mean_val

    if normalized_volatility > 0.25:
        return "Unstable"

    if slope > mean_val * 0.01:
        return "Increasing"

    if slope < -mean_val * 0.01:
        return "Decreasing"

    return "Stable"

def calculate_confidence(sequence, trend):
    diffs = np.diff(sequence)

    volatility = (
        np.std(diffs)
        if len(diffs) > 1
        else 0
    )

    mean_val = np.mean(np.abs(sequence)) + 1e-6

    normalized_volatility = volatility / mean_val

    confidence = 1 - normalized_volatility

    if trend == "Unstable":
        confidence *= 0.5

    confidence = max(
        0.2,
        min(0.95, confidence)
    )

    return round(float(confidence), 2)

def prepare_sequence(sequence):
    sequence = np.array(
        list(map(float, sequence)),
        dtype=np.float32
    )

    if len(sequence) < SEQ_LENGTH:
        pad = np.full(
            SEQ_LENGTH - len(sequence),
            sequence[0]
        )

        sequence = np.concatenate(
            [pad, sequence]
        )

    else:
        sequence = sequence[-SEQ_LENGTH:]

    return sequence

def fallback_prediction(sequence):
    diffs = np.diff(sequence)

    avg_growth = (
        np.mean(diffs)
        if len(diffs) > 0
        else 0
    )

    next_value = sequence[-1] + avg_growth

    future_forecast = []

    current = next_value

    for _ in range(FUTURE_STEPS):
        future_forecast.append(
            round(float(current), 2)
        )

        current += avg_growth

    trend = detect_trend(sequence)

    confidence = calculate_confidence(
        sequence,
        trend
    )

    return {
        "predicted_value": round(
            float(next_value),
            2
        ),
        "future_forecast": future_forecast,
        "trend": trend,
        "confidence": confidence
    }

def forecast(input_data):
    try:
        if isinstance(input_data, dict):
            sequence = (
                input_data.get("revenue_history")
                or input_data.get("sequence")
            )

        elif isinstance(input_data, list):
            sequence = input_data

        else:
            return {
                "error": "Invalid input format"
            }

        if not sequence or len(sequence) < 2:
            return {
                "error": "Insufficient data"
            }

        sequence = prepare_sequence(sequence)

        if model is None or scaler is None:
            return fallback_prediction(sequence)

        scaled_sequence = scaler.transform(
            sequence.reshape(-1, 1)
        ).flatten()

        current_seq = scaled_sequence.copy()

        future_preds = []

        for _ in range(FUTURE_STEPS):
            seq_tensor = torch.FloatTensor(
                current_seq
            ).reshape(
                1,
                SEQ_LENGTH,
                1
            ).to(device)

            with torch.no_grad():
                pred_scaled = model(
                    seq_tensor
                ).item()

            pred_scaled = np.clip(
                pred_scaled,
                0,
                1
            )

            pred = scaler.inverse_transform(
                [[pred_scaled]]
            )[0][0]

            pred = max(0, pred)

            future_preds.append(
                round(float(pred), 2)
            )

            current_seq = np.append(
                current_seq[1:],
                pred_scaled
            )

        next_prediction = future_preds[0]

        trend = detect_trend(sequence)

        confidence = calculate_confidence(
            sequence,
            trend
        )

        return {
            "predicted_value": round(
                float(next_prediction),
                2
            ),
            "future_forecast": future_preds,
            "trend": trend,
            "confidence": confidence
        }

    except Exception as e:
        return {
            "error": str(e)
        }