import joblib
import numpy as np

MODEL_PATH = "models/risk/risk_model.pkl"
SCALER_PATH = "models/risk/scaler.pkl"

try:
    model = joblib.load(MODEL_PATH)

    scaler = joblib.load(SCALER_PATH)

except Exception:
    model = None
    scaler = None

def validate_inputs(
    revenue,
    growth,
    burn,
    market
):
    if revenue <= 0:
        raise ValueError(
            "Revenue must be greater than 0"
        )

    if burn < 0:
        raise ValueError(
            "Burn rate cannot be negative"
        )

    if not -1 <= growth <= 5:
        raise ValueError(
            "Growth rate out of range"
        )

    if not 0 <= market <= 1:
        raise ValueError(
            "Market score must be between 0 and 1"
        )

def fallback_risk(
    revenue,
    growth,
    burn,
    market
):
    burn_ratio = burn / revenue

    score = 0

    reasons = []

    if growth < 0:
        score += 1
        reasons.append("Negative growth")

    if burn_ratio > 1:
        score += 1
        reasons.append("High burn rate")

    if market < 0.4:
        score += 1
        reasons.append("Weak market")

    if score >= 2:
        level = "High"
        prob = 0.8

    elif score == 1:
        level = "Medium"
        prob = 0.5

    else:
        level = "Low"
        prob = 0.2

    return {
        "risk_level": level,
        "risk_probability": round(
            prob,
            3
        ),
        "confidence": 0.6,
        "factors": {
            "burn_ratio": round(
                burn_ratio,
                2
            ),
            "growth_rate": growth,
            "market_score": market
        },
        "reason": (
            ", ".join(reasons)
            if reasons
            else "Stable metrics"
        )
    }

def risk_predict(features):
    try:
        revenue = float(
            features.get("revenue", 0)
        )

        growth = float(
            features.get("growth_rate", 0)
        )

        burn = float(
            features.get("burn_rate", 0)
        )

        market = float(
            features.get("market_score", 0.5)
        )

        validate_inputs(
            revenue,
            growth,
            burn,
            market
        )

        if model is None or scaler is None:
            return fallback_risk(
                revenue,
                growth,
                burn,
                market
            )

        burn_ratio = burn / revenue

        X = np.array([
            [
                revenue,
                growth,
                burn,
                market
            ]
        ])

        X_scaled = scaler.transform(X)

        model_prob = float(
            model.predict_proba(
                X_scaled
            )[0][1]
        )

        adjustment = 0

        reasons = []

        if growth < 0:
            adjustment += 0.1
            reasons.append(
                "Negative growth"
            )

        if burn_ratio > 1:
            adjustment += 0.12
            reasons.append(
                "High burn vs revenue"
            )

        if market < 0.4:
            adjustment += 0.08
            reasons.append(
                "Weak market"
            )

        if growth > 0.4 and burn_ratio < 0.5:
            adjustment -= 0.1
            reasons.append(
                "Efficient growth"
            )

        final_prob = model_prob + adjustment

        final_prob = max(
            0.01,
            min(0.99, final_prob)
        )

        if final_prob >= 0.7:
            level = "High"

        elif final_prob >= 0.4:
            level = "Medium"

        else:
            level = "Low"

        confidence = round(
            0.5 + abs(model_prob - 0.5),
            2
        )

        confidence = min(
            confidence,
            0.95
        )

        return {
            "risk_level": level,
            "risk_probability": round(
                final_prob,
                3
            ),
            "confidence": confidence,
            "model_probability": round(
                model_prob,
                3
            ),
            "factors": {
                "burn_ratio": round(
                    burn_ratio,
                    2
                ),
                "growth_rate": growth,
                "market_score": market
            },
            "reason": (
                ", ".join(reasons)
                if reasons
                else "Stable metrics"
            )
        }

    except Exception as e:
        return {
            "error": str(e)
        }