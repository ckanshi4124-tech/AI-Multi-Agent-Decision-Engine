# ============================================
# PLANNER PROMPT (OPTIONAL FUTURE USE)
# ============================================

PLANNER_PROMPT = """
You are an AI planning agent.

Decide which tools are needed:
- forecast → predict revenue trends
- risk → evaluate financial risk
- sentiment → analyze market sentiment

Return JSON:
{
  "steps": [
    {"tool": "forecast"},
    {"tool": "risk"},
    {"tool": "sentiment"}
  ]
}

User request:
{user_input}
"""


# ============================================
# REPORT TEMPLATE (FOR FUTURE LLM UPGRADE)
# ============================================

REPORT_TEMPLATE = """
Startup Analysis Report

Trend: {trend}
Risk Level: {risk}
Risk Probability: {risk_prob}
Sentiment: {sentiment}

Decision: {decision}

Provide a short justification.
"""