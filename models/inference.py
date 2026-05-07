from models.risk.predict import risk_predict
from models.forecasting.predict import forecast
from models.sentiment.sentiment import SentimentAnalyzer


class DecisionEngine:

    def __init__(self):
        self.sentiment_model = SentimentAnalyzer()

    def evaluate_risk(self, risk_input: dict):
        return risk_predict(risk_input)

    def forecast_revenue(self, revenue_sequence: list):
        return forecast(revenue_sequence)

    def analyze_sentiment(self, text: str):
        return self.sentiment_model.analyze(text)

    def full_decision(self, risk_input: dict, revenue_sequence: list, text: str):
        risk_result = self.evaluate_risk(risk_input)
        revenue_prediction = self.forecast_revenue(revenue_sequence)
        sentiment_result = self.analyze_sentiment(text)

        return {
            "risk": risk_result,
            "revenue_forecast": revenue_prediction,
            "sentiment": sentiment_result
        }