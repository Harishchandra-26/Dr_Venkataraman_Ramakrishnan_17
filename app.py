import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

from data_simulation import generate_sample_data
from predictors import predict_outbreak_simple, generate_recommendations

st.set_page_config(
    page_title="JalRakshak",
    page_icon="💧",
    layout="wide"
)

st.title("💧 JalRakshak – Waterborne Disease Prediction")

# Load / generate data
try:
    df = pd.read_csv("synthetic_waterborne_data.csv")
except:
    df = generate_sample_data()
    df.to_csv("synthetic_waterborne_data.csv", index=False)

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Predict Risk"]
)

# ================= DASHBOARD =================
if page == "Dashboard":
    st.subheader("📊 Risk Overview")

    latest = df.groupby("city").last().reset_index()
    fig = px.bar(
        latest,
        x="city",
        y="risk_score",
        color="risk_category",
        title="City-wise Risk Score"
    )
    st.plotly_chart(fig, use_container_width=True)

# ================= PREDICTION =================
if page == "Predict Risk":
    st.subheader("🔍 Predict Outbreak Risk")

    rainfall = st.slider("Rainfall (mm)", 0.0, 200.0, 80.0)
    drainage = st.slider("Drainage (1 good – 5 poor)", 1, 5, 4)
    contamination = st.slider("Water Contamination (%)", 0.0, 100.0, 60.0)
    sanitation = st.slider("Sanitation Coverage (%)", 0.0, 100.0, 40.0)
    humidity = st.slider("Humidity (%)", 20.0, 100.0, 85.0)
    density = st.number_input("Population Density", 5000, 50000, 30000)

    if st.button("Predict"):
        input_data = {
            'rainfall_mm': rainfall,
            'drainage_score': drainage,
            'water_contamination': contamination,
            'sanitation_coverage': sanitation,
            'humidity_percent': humidity,
            'population_density': density
        }

        pred = predict_outbreak_simple(input_data)

        st.markdown(f"### {pred['emoji']} Risk: **{pred['category']}**")
        st.write(f"Risk Score: `{pred['risk_score']:.2f}`")
        st.write(f"Outbreak Probability: `{pred['probability']:.1%}`")
        st.write(f"Predicted Disease: **{pred['disease']}**")

        st.subheader("Recommendations")
        for r in generate_recommendations(pred, input_data):
            st.write(r)
