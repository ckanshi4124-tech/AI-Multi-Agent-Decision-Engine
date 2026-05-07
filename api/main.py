from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict
import logging

# Agents
from agents.orchestrator import run_agent
from agents.planner_agent import generate_plan
from agents.evaluator_agent import evaluate_report

# Models
from models.risk.predict import risk_predict
from models.forecasting.predict import forecast
from models.sentiment.sentiment import sentiment_analyze


# =========================
# APP CONFIG
# =========================

app = FastAPI(
    title="AI Multi-Agent Decision Engine",
    version="2.0"
)

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


# =========================
# REQUEST MODELS
# =========================

class RiskRequest(BaseModel):

    features: Dict[str, float]

    @field_validator("features")
    def validate_features(cls, v):

        required = [
            "revenue",
            "growth_rate",
            "burn_rate",
            "market_score"
        ]

        for key in required:

            if key not in v:
                raise ValueError(f"Missing feature: {key}")

        if v["revenue"] < 0:
            raise ValueError("Revenue cannot be negative")

        if v["burn_rate"] < 0:
            raise ValueError("Burn rate cannot be negative")

        if not (0 <= v["market_score"] <= 1):
            raise ValueError("Market score must be between 0 and 1")

        return v


class ForecastRequest(BaseModel):

    sequence: List[float] = Field(
        ...,
        min_length=2
    )


class SentimentRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=3
    )


class PlanRequest(BaseModel):

    query: str


class ReportRequest(BaseModel):

    startup_name: str

    industry: str

    revenue_history: List[float]

    burn_rate: float

    customer_growth_rate: float

    market_notes: str


# =========================
# HEALTH
# =========================

@app.get("/health")
def health():

    return {
        "status": "API is running"
    }


# =========================
# RISK
# =========================

@app.post("/risk")
def predict_risk(request: RiskRequest):

    try:

        result = risk_predict(
            request.features
        )

        return result

    except Exception as e:

        logger.error(f"Risk error: {e}")

        return {
            "error": str(e)
        }


# =========================
# FORECAST
# =========================

@app.post("/forecast")
def predict_forecast(request: ForecastRequest):

    try:

        result = forecast(
            request.sequence
        )

        return result

    except Exception as e:

        logger.error(f"Forecast error: {e}")

        return {
            "error": str(e)
        }


# =========================
# SENTIMENT
# =========================

@app.post("/sentiment")
def predict_sentiment(request: SentimentRequest):

    try:

        result = sentiment_analyze(
            request.text
        )

        return result

    except Exception as e:

        logger.error(f"Sentiment error: {e}")

        return {
            "error": str(e)
        }


# =========================
# PLANNER
# =========================

@app.post("/plan")
def create_plan(request: PlanRequest):

    try:

        result = generate_plan(
            request.query
        )

        return result

    except Exception as e:

        logger.error(f"Planner error: {e}")

        return {
            "error": str(e)
        }


# =========================
# FULL REPORT
# =========================

@app.post("/report")
def run_full_report(request: ReportRequest):

    try:

        data = request.model_dump()

        result = run_agent(data)

        return result

    except Exception as e:

        logger.error(f"Report error: {e}")

        return {
            "error": str(e)
        }


# =========================
# EVALUATE
# =========================

@app.post("/evaluate")
def evaluate_only(report: dict):

    try:

        result = evaluate_report(report)

        return result

    except Exception as e:

        logger.error(f"Evaluation error: {e}")

        return {
            "error": str(e)
        }