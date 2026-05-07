import logging

logger = logging.getLogger(__name__)


def generate_plan(user_input: str):
    """
    Intelligent planning agent:
    - Detects user intent
    - Assigns strategy
    - Prioritizes tools
    - Returns explainable plan
    """

    try:
        text = str(user_input).lower()

        steps = []
        reason = []
        strategy = "general"

        # =========================
        # INTENT DETECTION
        # =========================

        growth_keywords = ["growth", "scale", "expand", "revenue", "increase"]
        risk_keywords = ["risk", "loss", "burn", "decline", "churn"]
        sentiment_keywords = ["market", "customer", "feedback", "reviews"]

        growth_score = sum(1 for w in growth_keywords if w in text)
        risk_score = sum(1 for w in risk_keywords if w in text)
        sentiment_score = sum(1 for w in sentiment_keywords if w in text)

        # =========================
        # STRATEGY SELECTION
        # =========================

        if risk_score > growth_score:
            strategy = "risk_mitigation"
            reason.append("User input indicates risk or instability")

        elif growth_score > risk_score:
            strategy = "growth"
            reason.append("User input focuses on growth and expansion")

        elif sentiment_score > 0:
            strategy = "market_analysis"
            reason.append("User input relates to customer/market sentiment")

        else:
            strategy = "general_analysis"
            reason.append("Balanced or unclear input → general plan")

        # =========================
        # TOOL PRIORITY LOGIC
        # =========================

        # Always include forecast (core signal)
        steps.append({"tool": "forecast", "priority": 1})

        # Strategy-based ordering
        if strategy == "growth":
            steps.append({"tool": "forecast", "priority": 1})
            steps.append({"tool": "sentiment", "priority": 2})
            steps.append({"tool": "risk", "priority": 3})

        elif strategy == "risk_mitigation":
            steps.append({"tool": "risk", "priority": 1})
            steps.append({"tool": "forecast", "priority": 2})
            steps.append({"tool": "sentiment", "priority": 3})

        elif strategy == "market_analysis":
            steps.append({"tool": "sentiment", "priority": 1})
            steps.append({"tool": "forecast", "priority": 2})
            steps.append({"tool": "risk", "priority": 3})

        else:
            steps.append({"tool": "forecast", "priority": 1})
            steps.append({"tool": "sentiment", "priority": 2})
            steps.append({"tool": "risk", "priority": 3})

        # =========================
        # REMOVE DUPLICATES
        # =========================

        seen = set()
        unique_steps = []
        for step in sorted(steps, key=lambda x: x["priority"]):
            tool = step["tool"]
            if tool not in seen:
                unique_steps.append(step)
                seen.add(tool)

        # =========================
        # FINAL OUTPUT
        # =========================

        return {
            "strategy": strategy,
            "steps": unique_steps,
            "reason": ", ".join(reason)
        }

    except Exception as e:
        logger.error(f"Planner error: {e}")
        return {
            "strategy": "fallback",
            "steps": [
                {"tool": "forecast", "priority": 1},
                {"tool": "risk", "priority": 2}
            ],
            "reason": "Fallback due to error"
        }