# agents/evaluator_agent.py
import logging

logger=logging.getLogger(__name__)

def evaluate_report(data):
    try:
        forecast=data.get("forecast",{})
        risk=data.get("risk_assessment",{})
        sentiment=data.get("market_sentiment",{})
        recommendation=data.get("strategic_recommendation",{})

        trend=str(forecast.get("trend","stable")).lower()
        forecast_conf=float(forecast.get("confidence",0.5))

        risk_prob=float(risk.get("risk_probability",0.5))

        sentiment_label=str(
            sentiment.get("label","neutral")
        ).lower()

        sentiment_score=float(
            sentiment.get("confidence",0.5)
        )

        decision=str(
            recommendation.get("decision","WATCH")
        ).upper()

        if risk_prob>=0.7:
            risk_level="high"
        elif risk_prob>=0.4:
            risk_level="medium"
        else:
            risk_level="low"

        trend_score={
            "increasing":1.0,
            "stable":0.6,
            "decreasing":0.2,
            "unstable":0.3
        }.get(trend,0.5)

        sentiment_numeric={
            "positive":1.0,
            "neutral":0.5,
            "negative":0.2
        }.get(sentiment_label,0.5)

        safety_score=1-risk_prob

        agreement=1-abs(
            trend_score-sentiment_numeric
        )

        agreement=round(
            max(0.0,min(1.0,agreement)),
            2
        )

        issues=[]

        if agreement<0.4:
            issues.append(
                "Trend and sentiment conflict"
            )

        if (
            trend=="increasing"
            and sentiment_label=="negative"
        ):
            issues.append(
                "Growth vs negative sentiment"
            )

        if (
            trend=="decreasing"
            and sentiment_label=="positive"
        ):
            issues.append(
                "Decline vs positive sentiment"
            )

        if (
            risk_level=="high"
            and trend=="increasing"
        ):
            issues.append(
                "High risk contradicts growth"
            )

        if risk_level=="high":
            expected_decision="AVOID"

        elif (
            trend=="increasing"
            and sentiment_label=="positive"
            and risk_level=="low"
        ):
            expected_decision="INVEST"

        elif (
            trend=="decreasing"
            and sentiment_label=="negative"
        ):
            expected_decision="AVOID"

        elif agreement<0.5:
            expected_decision="WATCH"

        else:
            expected_decision="WATCH"

        if decision!=expected_decision:
            issues.append(
                f"Expected {expected_decision}, got {decision}"
            )

        confidence_check=(
            0.4*forecast_conf+
            0.3*safety_score+
            0.3*sentiment_score
        )

        confidence_check=round(
            max(0.0,min(1.0,confidence_check)),
            2
        )

        if (
            confidence_check>0.8
            and agreement<0.5
        ):
            issues.append(
                "Overconfident conflicting signals"
            )

        quality_score=(
            0.4*agreement+
            0.3*safety_score+
            0.3*sentiment_score
        )

        quality_score=round(
            max(0.0,min(1.0,quality_score)),
            2
        )

        if len(issues)==0 and quality_score>0.75:
            grade="A+"
        elif quality_score>0.6:
            grade="A"
        elif quality_score>0.45:
            grade="B"
        else:
            grade="C"

        status=(
            "Consistent"
            if len(issues)==0
            else "Needs Review"
        )

        explanation=(
            f"Trend:{trend}, "
            f"Sentiment:{sentiment_label}, "
            f"Risk:{risk_level}, "
            f"Agreement:{agreement}"
        )

        return {
            "expected_decision":expected_decision,
            "actual_decision":decision,
            "evaluation_grade":grade,
            "quality_score":quality_score,
            "confidence_check":confidence_check,
            "signal_agreement":agreement,
            "issues_found":issues,
            "status":status,
            "explanation":explanation
        }

    except Exception as e:
        logger.error(f"Evaluation error: {e}")
        return {"error":str(e)}