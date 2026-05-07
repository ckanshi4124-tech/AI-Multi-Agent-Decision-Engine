# agents/report_agent.py

import logging

logger=logging.getLogger(__name__)

def generate_report(
    user_query:str,
    forecast_result:dict,
    risk_result:dict,
    sentiment_result:dict,
    evaluation:dict=None
):

    try:

        predicted_growth=float(
            forecast_result.get(
                "predicted_growth_rate",
                0.0
            )
        )

        forecast_confidence=float(
            forecast_result.get(
                "confidence_score",
                0.5
            )
        )

        trend=forecast_result.get(
            "trend",
            "stable"
        )

        forecast_output={
            "predicted_growth_rate":round(
                predicted_growth,
                2
            ),
            "confidence":round(
                forecast_confidence,
                2
            ),
            "trend":trend
        }

        risk_level=risk_result.get(
            "risk_level",
            "Medium"
        )

        risk_probability=float(
            risk_result.get(
                "risk_probability",
                0.5
            )
        )

        risk_confidence=float(
            risk_result.get(
                "confidence",
                0.5
            )
        )

        risk_output={
            "risk_level":risk_level,
            "risk_probability":round(
                risk_probability,
                2
            ),
            "confidence":round(
                risk_confidence,
                2
            )
        }

        sentiment_label=sentiment_result.get(
            "sentiment_label",
            "Neutral"
        )

        sentiment_score=float(
            sentiment_result.get(
                "sentiment_score",
                0.5
            )
        )

        sentiment_output={
            "label":sentiment_label,
            "confidence":round(
                sentiment_score,
                2
            )
        }

        if (
            predicted_growth>=0.15
            and risk_probability<0.4
            and sentiment_label.lower()=="positive"
        ):

            decision="INVEST"

            explanation=(
                "Strong growth with healthy "
                "market sentiment and low risk."
            )

        elif risk_probability>=0.7:

            decision="AVOID"

            explanation=(
                "High financial or operational "
                "risk detected."
            )

        elif sentiment_label.lower()=="negative":

            decision="WATCH"

            explanation=(
                "Negative market sentiment "
                "requires careful monitoring."
            )

        else:

            decision="WATCH"

            explanation=(
                "Business indicators appear "
                "moderately stable."
            )

        recommendation_output={
            "decision":decision,
            "explanation":explanation
        }

        overall_confidence=(
            forecast_confidence+
            (1-risk_probability)+
            sentiment_score
        )/3

        overall_confidence=round(
            max(0.0,min(1.0,overall_confidence)),
            2
        )

        final_output={
            "forecast":forecast_output,
            "risk_assessment":risk_output,
            "market_sentiment":sentiment_output,
            "strategic_recommendation":recommendation_output,
            "overall_confidence":overall_confidence
        }

        if evaluation:
            final_output["evaluation"]=evaluation

        return final_output

    except Exception as e:

        logger.error(
            f"Report Agent Error: {e}"
        )

        return {
            "forecast":{
                "predicted_growth_rate":0.0,
                "confidence":0.0,
                "trend":"unknown"
            },
            "risk_assessment":{
                "risk_level":"Unknown",
                "risk_probability":0.0,
                "confidence":0.0
            },
            "market_sentiment":{
                "label":"Neutral",
                "confidence":0.0
            },
            "strategic_recommendation":{
                "decision":"WATCH",
                "explanation":"System failed."
            },
            "overall_confidence":0.0
        }
        