
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Truck-to-Rail Conversion Intelligence", layout="wide")

st.title("🚛➡️🚂 Truck-to-Rail Conversion Intelligence MVP")
st.markdown("Identify when truck pricing becomes expensive enough for freight to convert to rail/intermodal.")

@st.cache_data
def load_data():
    return pd.read_csv("sample_lanes.csv")

df = load_data()

# --- Sidebar ---
st.sidebar.header("Controls")

fuel_adj = st.sidebar.slider(
    "Fuel Adjustment Factor",
    min_value=-0.20,
    max_value=0.20,
    value=0.00,
    step=0.01
)

conversion_threshold = st.sidebar.slider(
    "Conversion Alert Threshold (%)",
    min_value=5,
    max_value=50,
    value=25
)

# --- Calculations ---
df["Adjusted_Truck_Rate"] = df["Truck_Rate"] * (1 + fuel_adj)

df["All_In_Rail_Cost"] = (
    df["Rail_Rate"] +
    df["Drayage_Cost"] +
    df["Accessorials"]
)

df["Spread_Dollars"] = (
    df["Adjusted_Truck_Rate"] -
    df["All_In_Rail_Cost"]
)

df["Spread_Percent"] = (
    df["Spread_Dollars"] /
    df["Adjusted_Truck_Rate"]
) * 100

def conversion_score(row):
    score = 0

    if row["Spread_Percent"] > 10:
        score += 20

    if row["Spread_Percent"] > 20:
        score += 25

    if row["Spread_Percent"] > 30:
        score += 25

    if row["Distance_Miles"] > 700:
        score += 10

    if row["Rail_Service_Score"] >= 8:
        score += 10

    if row["Truck_Capacity_Tightness"] >= 7:
        score += 10

    return min(score, 100)

df["Conversion_Probability"] = df.apply(conversion_score, axis=1)

def classify(prob):
    if prob >= 70:
        return "HIGH"
    elif prob >= 40:
        return "MEDIUM"
    else:
        return "LOW"

df["Conversion_Risk"] = df["Conversion_Probability"].apply(classify)

# --- KPIs ---
col1, col2, col3, col4 = st.columns(4)

col1.metric("Tracked Lanes", len(df))
col2.metric("Avg Spread %", f"{df['Spread_Percent'].mean():.1f}%")
col3.metric(
    "High Conversion Lanes",
    int((df["Conversion_Risk"] == "HIGH").sum())
)
col4.metric(
    "Largest Spread",
    f"${df['Spread_Dollars'].max():,.0f}"
)

st.divider()

# --- Alert Section ---
alerts = df[df["Spread_Percent"] >= conversion_threshold]

st.subheader("🚨 Conversion Alerts")

if len(alerts) > 0:
    st.dataframe(
        alerts[[
            "Origin",
            "Destination",
            "Adjusted_Truck_Rate",
            "All_In_Rail_Cost",
            "Spread_Percent",
            "Conversion_Probability",
            "Conversion_Risk"
        ]].sort_values("Spread_Percent", ascending=False),
        use_container_width=True
    )
else:
    st.success("No lanes currently exceed the conversion threshold.")

st.divider()

# --- Chart ---
st.subheader("Lane Conversion Risk")

fig = px.scatter(
    df,
    x="Spread_Percent",
    y="Conversion_Probability",
    size="Distance_Miles",
    color="Conversion_Risk",
    hover_name="Lane",
    text="Lane"
)

fig.update_traces(textposition="top center")

st.plotly_chart(fig, use_container_width=True)

# --- Full Lane Table ---
st.subheader("All Lanes")

display_cols = [
    "Lane",
    "Adjusted_Truck_Rate",
    "All_In_Rail_Cost",
    "Spread_Dollars",
    "Spread_Percent",
    "Conversion_Probability",
    "Conversion_Risk"
]

st.dataframe(
    df[display_cols].sort_values("Conversion_Probability", ascending=False),
    use_container_width=True
)

# --- Footer ---
st.caption("Version 1 MVP • Truck-to-Rail Conversion Intelligence Platform")
