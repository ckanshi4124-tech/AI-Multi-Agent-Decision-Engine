from models.forecasting.predict import forecast
from models.risk.predict import risk_predict
from models.sentiment.sentiment import sentiment_analyze


def run_tool(tool_name: str, input_data):
    try:

        # =====================================================
        # 📈 FORECAST TOOL
        # =====================================================
        if tool_name == "forecast":
            result = forecast(input_data)

            if not isinstance(result, dict) or "error" in result:
                return {
                    "predicted_value": 0,
                    "trend": "Stable",
                    "confidence": 0.5,
                    "reason": "Fallback due to error"
                }

            return {
                "predicted_value": float(result.get("predicted_value", 0)),
                "trend": result.get("trend", "Stable"),
                "confidence": float(result.get("confidence", 0.5)),
                "details": result.get("details", {})
            }

        # =====================================================
        # ⚠️ RISK TOOL (UPGRADED 🔥)
        # =====================================================
        elif tool_name == "risk":
            result = risk_predict(input_data)

            if not isinstance(result, dict) or "error" in result:
                return {
                    "risk_level": "Medium",
                    "risk_probability": 0.5,
                    "confidence": 0.5,
                    "reason": "Fallback due to error",
                    "factors": {}
                }

            return {
                "risk_level": result.get("risk_level", "Medium"),
                "risk_probability": float(result.get("risk_probability", 0.5)),
                "confidence": float(result.get("confidence", 0.5)),
                "reason": result.get("reason", ""),
                "factors": result.get("factors", {})
            }

        # =====================================================
        # 🧠 SENTIMENT TOOL
        # =====================================================
        elif tool_name == "sentiment":
            result = sentiment_analyze(input_data)

            if not isinstance(result, dict) or "error" in result:
                return {
                    "label": "Neutral",
                    "confidence": 0.5,
                    "reason": "Fallback due to error"
                }

            return {
                "label": result.get("label", "Neutral"),
                "confidence": float(result.get("confidence", 0.5)),
                "reason": result.get("reason", "")
            }

        # =====================================================
        # ❌ UNKNOWN TOOL
        # =====================================================
        else:
            return {"error": f"Unknown tool: {tool_name}"}

    except Exception as e:
        return {"error": str(e)}
        