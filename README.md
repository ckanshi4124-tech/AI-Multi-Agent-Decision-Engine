# AI-Multi-Agent-Decision-Engine
AI Multi-Agent Decision Engine

An AI-powered startup investment analysis platform that uses a multi-agent architecture to evaluate startup opportunities through forecasting, risk assessment, sentiment analysis, strategic recommendations, and evaluation diagnostics.

Live Demo :-
Frontend (Streamlit): https://ai-multi-agent-decision-engine-f62eugdjr8h2mmmduwz8xc.streamlit.app
Repository: https://github.com/ckanshi4124-tech/AI-Multi-Agent-Decision-Engine

## Project Overview :-

This platform helps investors and analysts assess startup opportunities by combining multiple specialized AI agents. Each agent analyzes one dimension of the business and the orchestrator aggregates the outputs into a unified investment recommendation.

## Key Features:

- Revenue forecasting
- Risk assessment
- Market sentiment analysis
- Strategic recommendations
- Evaluation diagnostics
- Executive Summary mode
- Detailed Analysis mode
- Cloud deployment with Streamlit and Render

## Architecture:
```text
User
  ↓
Streamlit Frontend
  ↓
FastAPI Backend (Render)
  ↓
Orchestrator Agent
  ├── Forecast Agent
  ├── Risk Agent
  ├── Sentiment Agent
  ├── Report Agent
  └── Evaluation Agent
```

## Agent Descriptions:

Forecast Agent-
Predicts future growth trends from historical revenue data.

Risk Agent-
Assesses operational and financial risk.

Sentiment Agent-
Analyzes market notes and industry conditions.

Report Agent-
Combines outputs into a final investment recommendation.

Evaluation Agent-
Measures agreement and consistency across all agent signals.

## Technology Stack:
- Python
- Streamlit
- FastAPI
- Pandas
- PyTorch
- MLflow
- DVC
- Git & GitHub
- Render
- Streamlit Community Cloud

## Repository Structure:
```text
AI-MULTI-AGENT-DECISION-ENGINE/
├── .dvc/
├── .github/
│   └── workflows/
├── agents/
│   ├── orchestrator.py
│   ├── planner_agent.py
│   ├── report_agent.py
│   ├── tools.py
│   └── prompts.py
├── api/
│   └── main.py
├── data/
├── docs/
├── dvc_storage_files/
├── frontend/
│   └── app.py
├── mlruns/
├── models/
│   ├── forecasting/
│   ├── risk/
│   └── sentiment/
├── scripts/
├── tests/
├── utils/
├── Dockerfile
├── render.yaml
├── requirements.txt
└── README.md
```

## Installation:
git clone https://github.com/ckanshi4124-tech/AI-Multi-Agent-Decision-Engine.git
cd AI-Multi-Agent-Decision-Engine
pip install -r requirements.txt

Run Backend:
uvicorn api.main:app --reload

Run Frontend:
streamlit run frontend/app.py

API Endpoint:
POST /report

Input Example:

{
  "startup_name": "EcoTech Solutions",
  "industry": "Clean Energy",
  "revenue_history": [100000, 120000, 150000, 190000, 240000],
  "burn_rate": 45000,
  "customer_growth_rate": 28.5,
  "market_notes": "The clean energy market is expanding rapidly with strong investor interest."
}

## Model Design Decisions:
- Forecasting model built with PyTorch
- Risk scoring based on financial heuristics
- Sentiment analysis using NLP rules and domain signals
- Evaluation diagnostics for signal consistency

## MLOps Practices:
- DVC for data versioning
- MLflow for experiment tracking
- GitHub for version control
- Cloud deployment on Render and Streamlit

## Results
The system generates:
- Investment decision (INVEST / WATCH / PASS)
- Risk level
- Sentiment classification
- Confidence scores
- Strategic recommendations
- Diagnostic insights

## Future Enhancements:
- LLM-powered narrative generation
- Automated PDF reports
- Authentication and user accounts
- Scenario comparison dashboard
- Monitoring and alerting

## Author
 
Chitranshi Kulshrestha