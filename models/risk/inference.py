import pandas as pd

from models.risk.predict import (
    risk_predict
)

class RiskModel:
    def __init__(self):
        pass

    def predict(
        self,
        df: pd.DataFrame
    ):
        try:
            df = df.copy()

            results = []

            for _, row in df.iterrows():
                features = {
                    "revenue": float(
                        row.get("revenue", 0)
                    ),
                    "growth_rate": float(
                        row.get("growth_rate", 0)
                    ),
                    "burn_rate": float(
                        row.get("burn_rate", 0)
                    ),
                    "market_score": float(
                        row.get("market_score", 0.5)
                    )
                }

                result = risk_predict(
                    features
                )

                results.append(result)

            return results

        except Exception as e:
            return [
                {
                    "error": str(e)
                }
            ]