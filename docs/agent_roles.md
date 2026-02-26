We are building 6 agents.

1. Planner Agent (Coordinator)

Role:
Reads user input
Breaks task into subtasks
Defines execution order
Calls other agents

It DOES NOT:
Do forecasting
Do prediction
Generate final report

It only orchestrates.

2. Forecast Agent (Deep Learning Agent)

Role:
Takes revenue_history
Runs LSTM model
Produces forecast metrics

Output:
Structured forecast JSON only.

No reasoning text.

3. Risk Agent (Machine Learning Agent)

Role:
Uses burn_rate
Uses customer_growth_rate
Uses forecast output
Runs XGBoost model

Outputs:
risk_level
probability

No free-text reasoning.

4. Sentiment Agent (NLP Agent)

Role:
Reads market_notes
Runs transformer sentiment model
Outputs structured sentiment JSON

No long paragraphs.

5. Report Generator Agent (LLM Reasoning Agent)

Role:
Receives outputs from:
-Forecast Agent
-Risk Agent
-Sentiment Agent
Combines them
Generates structured strategic recommendation

This is the “consultant”.

6. Evaluator Agent (Validation Agent)

Role:
Checks consistency between:
-Growth vs Risk
-Sentiment vs Recommendation
Assigns overall_confidence score
Detects contradictions

It acts as quality control.

