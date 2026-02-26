FINAL ARCHITECTURE (Text Version)

[ User / UI ]
        |
        v
[ FastAPI Backend ]
        |
        v
[ Planner Agent ]
        |
        |----> [ Forecast Agent ] ----> [ LSTM Model ]
        |
        |----> [ Risk Agent ] ----> [ XGBoost Model ]
        |
        |----> [ Sentiment Agent ] ----> [ Transformer Model ]
        |
        v
[ Report Generator Agent ]
        |
        v
[ Evaluator Agent ]
        |
        v
[ Final JSON Response ]
        |
        v
[ Logging + MLflow + Monitoring ]


SYSTEM LAYERS 

🔹 Layer 1 – Presentation

UI (later minimal)

🔹 Layer 2 – API

FastAPI
Input validation
Request routing

🔹 Layer 3 – Agent Orchestration

Planner
Tool calls
Structured JSON passing

🔹 Layer 4 – ML/DL Models

LSTM
XGBoost
Transformer

🔹 Layer 5 – MLOps

MLflow
DVC
Drift detection
Docker
CI/CD
