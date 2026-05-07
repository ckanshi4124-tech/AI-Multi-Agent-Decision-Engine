import pandas as pd
from models.risk.inference import RiskModel


def test_prediction():
    model = RiskModel()

    sample = pd.DataFrame([{
        "revenue": 20000,
        "growth_rate": 0.5,
        "burn_rate": 10000,
        "market_score": 0.8
    }])

    result = model.predict(sample)
    print("Prediction output:", result)


if __name__ == "__main__":
    test_prediction()