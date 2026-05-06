import streamlit as st
import pandas as pd
import plotly.express as px

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

st.markdown(
    """
    <style>
        .stApp {
            background-color: #f5f7fa;
        }

        .trt-header {
            background: linear-gradient(90deg, #111827 0%, #1f2937 65%, #b91c1c 100%);
            padding: 26px 30px;
            border-radius: 18px;
            margin-bottom: 24px;
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
            margin-top: 8px;
        }

        .trt-logo-box {
            background: white;
            color: #b91c1c;
            border-radius: 14px;
            padding: 14px 18px;
            font-weight: 900;
            font-size: 28px;
            letter-spacing: 1px;
            min-width: 105px;
            text-align: center;
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
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="trt-header">
        <div style="display:flex; align-items:center; gap:24px;">
            <div class="trt-logo-box">TRT</div>
            <div>
                <div class="trt-title">Truck-to-Rail Conversion Dashboard</div>
                <div class="trt-subtitle">
                    TRT Intermodal | Identify lanes where truck rates support rail conversion
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.markdown("## TRT Intermodal")
st.sidebar.markdown("### Conversion Intelligence")
st.sidebar.caption("Monitor truck market conditions and identify intermodal conversion opportunities.")

savings_threshold_high = st.sidebar.number_input(
    "High opportunity savings threshold",
    min_value=0,
    max_value=5000,
    value=700,
    step=50
)

savings_threshold_medium = st.sidebar.number_input(
    "Medium opportunity savings threshold",
    min_value=0,
    max_value=5000,
    value=300,
    step=50
)

# ---------------------------------------------------
# DATA
# ---------------------------------------------------

df = pd.DataFrame({
    "Lane": [
        "Chicago → Dallas",
        "Chicago → Atlanta",
        "Los Angeles → Chicago",
        "Memphis → Harrisburg",
        "Houston → Chicago",
        "Kansas City → Atlanta",
        "Dallas → Stockton",
        "Chicago → New Jersey"
    ],
    "Truck Rate": [3450, 2950, 4200, 3100, 2850, 2600, 3900, 3350],
    "Rail Rate": [2350, 2300, 2850, 2400, 2500, 2200, 2750, 2450]
})

df["Savings"] = df["Truck Rate"] - df["Rail Rate"]

def classify_opportunity(savings):
    if savings >= savings_threshold_high:
        return "High"
    elif savings >= savings_threshold_medium:
        return "Medium"
    else:
        return "Low"

df["Conversion Opportunity"] = df["Savings"].apply(classify_opportunity)

# ---------------------------------------------------
# TOP METRICS
# ---------------------------------------------------

high_count = int((df["Conversion Opportunity"] == "High").sum())
avg_savings = int(df["Savings"].mean())
max_savings = int(df["Savings"].max())

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("High Conversion Lanes", high_count)

with col2:
    st.metric("Average Savings", f"${avg_savings:,}")

with col3:
    st.metric("Best Lane Savings", f"${max_savings:,}")

st.divider()

# ---------------------------------------------------
# TABLE
# ---------------------------------------------------

st.subheader("Lane Conversion Analysis")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# ---------------------------------------------------
# CHARTS
# ---------------------------------------------------

st.subheader("Truck vs Rail Rate Comparison")

rate_chart = px.bar(
    df,
    x="Lane",
    y=["Truck Rate", "Rail Rate"],
    barmode="group",
    title="Truck vs Rail Pricing"
)

st.plotly_chart(rate_chart, use_container_width=True)

st.subheader("Rail Conversion Savings")

savings_chart = px.bar(
    df,
    x="Lane",
    y="Savings",
    color="Conversion Opportunity",
    title="Estimated Savings by Lane",
    category_orders={"Conversion Opportunity": ["High", "Medium", "Low"]}
)

st.plotly_chart(savings_chart, use_container_width=True)

# ---------------------------------------------------
# RECOMMENDATIONS
# ---------------------------------------------------

st.subheader("Recommended Action")

best_lane = df.sort_values("Savings", ascending=False).iloc[0]

st.success(
    f"The strongest current conversion opportunity is {best_lane['Lane']} "
    f"with estimated savings of ${int(best_lane['Savings']):,} per load."
)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")
st.caption("TRT Intermodal © 2026 | Strategic Truck-to-Rail Conversion Intelligence")
