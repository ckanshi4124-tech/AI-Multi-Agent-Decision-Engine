# agents/orchestrator.py

from agents.tools import run_tool
from agents.report_agent import generate_report
from agents.evaluator_agent import evaluate_report
import numpy as np

def run_agent(data:dict):

    revenue_history=data.get("revenue_history",[])
    market_notes=data.get("market_notes","")
    burn_rate=float(data.get("burn_rate",0))

    if not isinstance(revenue_history,list):
        revenue_history=[]

    forecast_raw=run_tool("forecast",revenue_history)

    if not isinstance(forecast_raw,dict) or "error" in forecast_raw:

        forecast_result={
            "predicted_growth_rate":0.0,
            "confidence_score":0.3,
            "trend":"stable"
        }

    else:

        predicted_value=float(
            forecast_raw.get("predicted_value",0)
        )

        last_revenue=(
            revenue_history[-1]
            if revenue_history else 1
        )

        growth_rate=(
            predicted_value-last_revenue
        )/max(last_revenue,1)

        confidence=float(
            forecast_raw.get("confidence",0.5)
        )

        if growth_rate>0.15:
            trend="increasing"
        elif growth_rate<-0.1:
            trend="decreasing"
        else:
            trend="stable"

        forecast_result={
            "predicted_growth_rate":round(growth_rate,2),
            "confidence_score":round(confidence,2),
            "trend":trend
        }

    sentiment_raw=run_tool(
        "sentiment",
        market_notes
    )

    if not isinstance(sentiment_raw,dict) or "error" in sentiment_raw:

        sentiment_result={
            "sentiment_label":"Neutral",
            "sentiment_score":0.5
        }

    else:

        sentiment_result={
            "sentiment_label":sentiment_raw.get(
                "label",
                "Neutral"
            ),
            "sentiment_score":round(
                float(
                    sentiment_raw.get(
                        "confidence",
                        0.5
                    )
                ),
                2
            )
        }

    if len(revenue_history)>=2:

        revenue=float(revenue_history[-1])

        diffs=np.diff(revenue_history)

        avg_growth=float(np.mean(diffs))

        growth_rate=max(
            min(avg_growth/max(revenue,1),1),
            -1
        )

    else:

        revenue=0
        growth_rate=0

    sentiment_label=sentiment_result[
        "sentiment_label"
    ].lower()

    sentiment_score=float(
        sentiment_result[
            "sentiment_score"
        ]
    )

    if sentiment_label=="positive":
        market_score=min(sentiment_score+0.2,1.0)

    elif sentiment_label=="negative":
        market_score=max(sentiment_score*0.4,0.1)

    else:
        market_score=0.5

    risk_raw=run_tool(
        "risk",
        {
            "revenue":revenue,
            "growth_rate":growth_rate,
            "burn_rate":burn_rate,
            "market_score":market_score
        }
    )

    if not isinstance(risk_raw,dict) or "error" in risk_raw:

        risk_result={
            "risk_level":"Medium",
            "risk_probability":0.5,
            "confidence":0.5
        }

    else:

        risk_result={
            "risk_level":risk_raw.get(
                "risk_level",
                "Medium"
            ),
            "risk_probability":round(
                float(
                    risk_raw.get(
                        "risk_probability",
                        0.5
                    )
                ),
                2
            ),
            "confidence":round(
                float(
                    risk_raw.get(
                        "confidence",
                        0.5
                    )
                ),
                2
            )
        }

    final_report=generate_report(
        user_query=str(data),
        forecast_result=forecast_result,
        risk_result=risk_result,
        sentiment_result=sentiment_result
    )

    try:

        evaluation=evaluate_report(
            final_report
        )

        if (
            isinstance(evaluation,dict)
            and "error" not in evaluation
        ):

            final_report["evaluation"]=evaluation

            final_report[
                "overall_confidence"
            ]=round(
                float(
                    evaluation.get(
                        "confidence_check",
                        final_report.get(
                            "overall_confidence",
                            0.5
                        )
                    )
                ),
                2
            )

    except Exception as e:
        print(f"Evaluation error: {e}")

    return final_report