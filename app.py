import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="TRT Intermodal | Truck-to-Rail Conversion",
    layout="wide",
    page_icon="🚛"
)

# ---------------------------------------------------
# TRT BRANDING
# ---------------------------------------------------

TRT_LOGO_URL = "https://www.trtintermodal.com/wp-content/uploads/2021/08/trt-logo.png"

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

.trt-header {
    background: linear-gradient(90deg, #111827 0%, #1f2937 65%, #b91c1c 100%);
    padding: 24px 30px;
    border-radius: 18px;
    margin-bottom: 25px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.18);
}

.trt-title {
    color: white;
    font-size: 36px;
    font-weight: 800;
    line-height: 1.1;
}

.trt-subtitle {
    color: #e5e7eb;
    font-size: 16px;
    margin-top: 6px;
}

.metric-card {
    background: white;
    padding: 16px;
    border-radius: 16px;
    border-left: 6px solid #b91c1c;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
}

.stButton > button {
    background-color: #b91c1c;
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: 700;
}

.stButton > button:hover {
    background-color: #991b1b;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

section[data-testid="stSidebar"] * {
    color: white;
}

</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="trt-header">
    <div style="display:flex; align-items:center; gap:24px;">
        <img src="{TRT_LOGO_URL}" 
             style="height:72px; background:white; padding:10px; border-radius:14px;">

        <div>
            <div class="trt-title">
                Truck-to-Rail Conversion Dashboard
            </div>

            <div class="trt-subtitle">
                TRT Intermodal | Identify lanes where truck rates support rail conversion
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.markdown("## TRT Intermodal")
st.sidebar.markdown("### Conversion Intelligence")
st.sidebar.caption(
    "Monitor truck market conditions and identify intermodal conversion opportunities."
)

# ---------------------------------------------------
# SAMPLE DATA
# ---------------------------------------------------

lanes = [
    "Chicago → Dallas",
    "Chicago → Atlanta",
    "Los Angeles → Chicago",
    "Memphis → Harrisburg",
    "Houston → Chicago",
    "Kansas City → Atlanta",
    "Dallas → Stockton",
    "Chicago → New Jersey"
]

truck_rate = np.random.randint(1800, 4200, len(lanes))
rail_rate = np.random.randint(1200, 2800, len(lanes))

df = pd.DataFrame({
    "Lane": lanes,
    "Truck Rate": truck_rate,
    "Rail Rate": rail_rate
})

df["Savings"] = df["Truck Rate"] - df["Rail Rate"]
df["Conversion Opportunity"] = np.where(
    df["Savings"] > 700,
    "High",
    np.where(df["Savings"] > 300, "Medium", "Low")
)

# ---------------------------------------------------
# TOP METRICS
# ---------------------------------------------------

high_count = len(df[df["Conversion Opportunity"] == "High"])
avg_savings = int(df["Savings"].mean())
max_savings = int(df["Savings"].max())

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("High Conversion Lanes", high_count)

with col2:
    st.metric("Average Savings", f"${avg_savings}")

with col3:
    st.metric("Best Lane Savings", f"${max_savings}")

st.divider()

# ---------------------------------------------------
# DATA TABLE
# ---------------------------------------------------

st.subheader("Lane Conversion Analysis")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# ---------------------------------------------------
# CHART
# ---------------------------------------------------

st.subheader("Truck vs Rail Rate Comparison")

fig = px.bar(
    df,
    x="Lane",
    y=["Truck Rate", "Rail Rate"],
    barmode="group",
    title="Truck vs Rail Pricing"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# SAVINGS CHART
# ---------------------------------------------------

st.subheader("Rail Conversion Savings")

fig2 = px.bar(
    df,
    x="Lane",
    y="Savings",
    color="Conversion Opportunity",
    title="Estimated Savings by Lane"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")
st.caption("TRT Intermodal © 2026 | Strategic Truck-to-Rail Conversion Intelligence")
