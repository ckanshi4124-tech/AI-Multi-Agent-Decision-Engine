import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Multi-Agent Decision Engine",
    page_icon="🤖",
    layout="wide"
)

# Hide Streamlit developer toolbar
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
header[data-testid="stHeader"] {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

API_URL = "https://ai-multi-agent-decision-engine.onrender.com/report"

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
.main-title {
    font-size: 3rem;
    font-weight: 800;
    color: #0F172A;
}
.subtitle {
    font-size: 1.5rem;
    color: #475569;
    margin-bottom: 1rem;
}
.metric-card {
    background-color: #F8FAFC;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #E2E8F0;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.recommendation-box {
    background: linear-gradient(135deg, #EEF2FF, #F8FAFC);
    padding: 20px;
    border-radius: 16px;
    border-left: 6px solid #6366F1;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR INPUTS
# =========================
st.sidebar.title("📥 Startup Inputs")

startup_name = st.sidebar.text_input("Startup Name", "EcoTech Solutions")
industry = st.sidebar.text_input("Industry", "Clean Energy")
revenue_history_text = st.sidebar.text_input(
    "Revenue History (comma-separated)",
    "100000,120000,150000,190000,240000,300000"
)
burn_rate = st.sidebar.number_input("Burn Rate", value=45000.0)
customer_growth_rate = st.sidebar.number_input(
    "Customer Growth Rate (%)",
    value=28.5
)
market_notes = st.sidebar.text_area(
    "Market Notes",
    "The clean energy market is expanding rapidly with strong investor interest and favorable government policies."
)

report_mode = st.sidebar.radio(
    "📊 Report Mode",
    ["Executive Summary", "Detailed Analysis"]
)

# =========================
# HEADER
# =========================
st.markdown('<div class="main-title">🤖 AI Multi-Agent Decision Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Startup Investment Analysis Platform</div>', unsafe_allow_html=True)

st.info("Enter startup details and click Generate Full Report.")

# =========================
# BUTTON
# =========================
if st.sidebar.button("🚀 Generate Full Report", use_container_width=True):

    try:
        revenue_history = [
            float(x.strip())
            for x in revenue_history_text.split(",")
            if x.strip()
        ]

        payload = {
            "startup_name": startup_name,
            "industry": industry,
            "revenue_history": revenue_history,
            "burn_rate": burn_rate,
            "customer_growth_rate": customer_growth_rate,
            "market_notes": market_notes
        }

        with st.spinner("Running all AI agents..."):
            response = requests.post(API_URL, json=payload, timeout=120)

        if response.status_code != 200:
            st.error(f"API Error: {response.text}")
            st.stop()

        result = response.json()

        # =========================
        # EXECUTIVE SUMMARY
        # =========================
        st.success("Analysis Completed Successfully!")

        decision = result["strategic_recommendation"]["decision"]
        risk_level = result["risk_assessment"]["risk_level"]
        sentiment = result["market_sentiment"]["label"]
        confidence = result["overall_confidence"]

        st.markdown("## 📊 Executive Summary")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Decision", decision)
        col2.metric("Risk Level", risk_level)
        col3.metric("Sentiment", sentiment)
        col4.metric("Overall Confidence", f"{confidence:.2f}")

        # =========================
        # RECOMMENDATION
        # =========================
        explanation = result["strategic_recommendation"]["explanation"]

        st.markdown(
            f"""
            <div class="recommendation-box">
                <h3>🧠 Strategic Recommendation</h3>
                <p style="font-size:18px;">{explanation}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # =========================
        # REVENUE CHART
        # =========================
        st.markdown("## 📈 Revenue History")

        df = pd.DataFrame({
            "Period": list(range(1, len(revenue_history) + 1)),
            "Revenue": revenue_history
        })

        fig = px.line(
            df,
            x="Period",
            y="Revenue",
            markers=True,
            title="Historical Revenue Trend"
        )

        st.plotly_chart(fig, use_container_width=True)

        # =========================
        # DETAILED MODE
        # =========================
        if report_mode == "Detailed Analysis":
            st.markdown("## 🔍 Detailed Analysis")

            # Forecast Analysis
            with st.expander("📈 Forecast Analysis", expanded=True):
                forecast = result.get("forecast", {})
                st.metric("Predicted Growth Rate", f"{forecast.get('predicted_growth_rate', 0):.2f}%")
                st.metric("Confidence", f"{forecast.get('confidence', 0):.2f}")
                st.write(f"**Trend:** {forecast.get('trend', 'N/A').title()}")

            # Risk Assessment
            with st.expander("⚠️ Risk Assessment"):
                risk = result.get("risk_assessment", {})
                st.metric("Risk Level", risk.get("risk_level", "N/A"))
                st.metric("Risk Probability", f"{risk.get('risk_probability', 0):.2%}")
                st.metric("Confidence", f"{risk.get('confidence', 0):.2f}")

            # Market Sentiment
            with st.expander("📰 Market Sentiment"):
                sentiment = result.get("market_sentiment", {})
                st.metric("Sentiment", sentiment.get("label", "N/A"))
                st.metric("Confidence", f"{sentiment.get('confidence', 0):.2f}")

            # Strategic Recommendation
            with st.expander("🧠 Strategic Recommendation"):
                recommendation = result.get("strategic_recommendation", {})
                st.success(recommendation.get("decision", "N/A"))
                st.write(recommendation.get("explanation", "No explanation available."))

            # Evaluation Diagnostics
            with st.expander("🧪 Evaluation Diagnostics"):
                evaluation = result.get("evaluation", {})
                st.metric("Expected Decision", evaluation.get("expected_decision", "N/A"))
                st.metric("Actual Decision", evaluation.get("actual_decision", "N/A"))
                st.metric("Evaluation Grade", evaluation.get("evaluation_grade", "N/A"))
                st.metric("Quality Score", f"{evaluation.get('quality_score', 0):.2f}")
                st.metric("Signal Agreement", f"{evaluation.get('signal_agreement', 0):.2f}")

                issues = evaluation.get("issues_found", [])
                if issues:
                    st.warning("Issues Found:")
                    for issue in issues:
                        st.write(f"• {issue}")
                else:
                    st.success("No issues detected.")

            
    except Exception as e:
        st.error(f"Unexpected Error: {e}")
        