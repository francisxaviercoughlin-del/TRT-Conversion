import os
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st


# ===================================================
# PAGE CONFIG
# ===================================================

st.set_page_config(
    page_title="TRT Intermodal | Live Truck-to-Rail Conversion",
    layout="wide",
    page_icon="🚛",
)


# ===================================================
# HELPERS
# ===================================================

def get_secret(name: str, default: str = "") -> str:
    try:
        if name in st.secrets:
            return st.secrets[name]
    except Exception:
        pass

    return os.getenv(name, default)


def classify_opportunity(savings: float, high_threshold: float, medium_threshold: float) -> str:
    if savings >= high_threshold:
        return "High"
    if savings >= medium_threshold:
        return "Medium"
    return "Low"


def normalize_lane(origin: str, destination: str) -> str:
    return f"{origin.strip()} → {destination.strip()}"


# ===================================================
# BRANDING + CSS
# ===================================================

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

        .status-card {
            background: white;
            padding: 18px;
            border-radius: 16px;
            border-left: 6px solid #b91c1c;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            margin-bottom: 10px;
        }

        section[data-testid="stSidebar"] {
            background-color: #111827;
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] label {
            color: white !important;
        }

        section[data-testid="stSidebar"] input {
            color: black !important;
            background-color: white !important;
        }

        section[data-testid="stSidebar"] textarea {
            color: black !important;
            background-color: white !important;
        }

        section[data-testid="stSidebar"] .stNumberInput input {
            color: black !important;
            background-color: white !important;
        }

        section[data-testid="stSidebar"] div[data-baseweb="select"] {
            background-color: white !important;
        }

        section[data-testid="stSidebar"] div[data-baseweb="select"] * {
            color: black !important;
        }

        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: white !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="trt-header">
        <div style="display:flex; align-items:center; gap:24px;">
            <div class="trt-logo-box">TRT</div>
            <div>
                <div class="trt-title">Live Truck-to-Rail Conversion Dashboard</div>
                <div class="trt-subtitle">
                    TRT Intermodal | Flag lanes where truck pricing creates rail conversion opportunities
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ===================================================
# SIDEBAR
# ===================================================

st.sidebar.markdown("## TRT Intermodal")
st.sidebar.markdown("### Live Data Settings")
st.sidebar.caption("Monitor truck market conditions and identify intermodal conversion opportunities.")

data_mode = st.sidebar.selectbox(
    "Data source",
    [
        "Demo live-ready data",
        "Upload CSV",
        "API: DAT / truck + manual rail",
        "API: SONAR / truck + rail",
    ],
)

high_threshold = st.sidebar.number_input(
    "High opportunity savings threshold",
    min_value=0,
    max_value=10000,
    value=700,
    step=50,
)

medium_threshold = st.sidebar.number_input(
    "Medium opportunity savings threshold",
    min_value=0,
    max_value=10000,
    value=300,
    step=50,
)

fuel_adjustment = st.sidebar.number_input(
    "Truck fuel / accessorial adjustment",
    min_value=-1000,
    max_value=3000,
    value=0,
    step=25,
)

rail_margin_buffer = st.sidebar.number_input(
    "Rail conversion buffer",
    min_value=0,
    max_value=3000,
    value=150,
    step=25,
    help="Use this to account for drayage, lift fees, service variability, or target margin.",
)

st.sidebar.markdown("---")
st.sidebar.markdown("### What These Mean")
st.sidebar.caption(
    "Savings = adjusted truck rate minus adjusted rail rate. "
    "High and Medium thresholds control how lanes are ranked."
)


# ===================================================
# DATA LOADERS
# ===================================================

def demo_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Origin": [
                "Chicago, IL",
                "Chicago, IL",
                "Los Angeles, CA",
                "Memphis, TN",
                "Houston, TX",
                "Kansas City, MO",
                "Dallas, TX",
                "Chicago, IL",
                "St. Louis, MO",
                "Cleveland, OH",
            ],
            "Destination": [
                "Dallas, TX",
                "Atlanta, GA",
                "Chicago, IL",
                "Harrisburg, PA",
                "Chicago, IL",
                "Atlanta, GA",
                "Stockton, CA",
                "Newark, NJ",
                "Los Angeles, CA",
                "Dallas, TX",
            ],
            "Truck Rate": [3450, 2950, 4200, 3100, 2850, 2600, 3900, 3350, 4300, 3050],
            "Rail Rate": [2350, 2300, 2850, 2400, 2500, 2200, 2750, 2450, 3100, 2450],
            "Truck Miles": [925, 715, 2015, 930, 1085, 805, 1720, 790, 1830, 1180],
            "Rail Transit Days": [4, 4, 5, 4, 5, 4, 5, 4, 5, 5],
            "Truck Transit Days": [2, 2, 4, 2, 3, 2, 4, 2, 4, 3],
            "Data Source": ["Demo"] * 10,
        }
    )


def uploaded_csv_data() -> pd.DataFrame:
    st.info(
        "Upload a CSV with columns: Origin, Destination, Truck Rate, Rail Rate. "
        "Optional columns: Truck Miles, Truck Transit Days, Rail Transit Days."
    )

    uploaded_file = st.file_uploader("Upload lane pricing CSV", type=["csv"])

    if uploaded_file is None:
        return demo_data()

    df = pd.read_csv(uploaded_file)

    required_columns = ["Origin", "Destination", "Truck Rate", "Rail Rate"]
    missing = [c for c in required_columns if c not in df.columns]

    if missing:
        st.error(f"Missing required columns: {', '.join(missing)}")
        return demo_data()

    df["Data Source"] = "Uploaded CSV"
    return df


def dat_truck_manual_rail_data() -> pd.DataFrame:
    dat_api_key = get_secret("DAT_API_KEY")

    st.warning(
        "DAT API mode is ready for a future DAT integration. "
        "For now, edit the table below or upload CSV data."
    )

    with st.expander("Enter DAT-ready lane data", expanded=True):
        default_df = demo_data()[["Origin", "Destination", "Truck Rate", "Rail Rate", "Truck Miles"]]
        edited = st.data_editor(default_df, num_rows="dynamic", use_container_width=True)

    edited["Data Source"] = "DAT-ready/manual rail"

    if dat_api_key:
        st.success("DAT_API_KEY detected in Streamlit secrets.")
    else:
        st.info("No DAT_API_KEY found yet. Add it in Streamlit Cloud → App → Settings → Secrets.")

    return edited


def sonar_truck_rail_data() -> pd.DataFrame:
    sonar_api_key = get_secret("SONAR_API_KEY")

    st.warning(
        "SONAR API mode is ready for a future SONAR integration. "
        "For now, edit the table below or upload CSV data."
    )

    with st.expander("Enter SONAR-ready lane data", expanded=True):
        default_df = demo_data()[["Origin", "Destination", "Truck Rate", "Rail Rate", "Truck Miles"]]
        edited = st.data_editor(default_df, num_rows="dynamic", use_container_width=True)

    edited["Data Source"] = "SONAR-ready/manual fallback"

    if sonar_api_key:
        st.success("SONAR_API_KEY detected in Streamlit secrets.")
    else:
        st.info("No SONAR_API_KEY found yet. Add it in Streamlit Cloud → App → Settings → Secrets.")

    return edited


if data_mode == "Upload CSV":
    df = uploaded_csv_data()
elif data_mode == "API: DAT / truck + manual rail":
    df = dat_truck_manual_rail_data()
elif data_mode == "API: SONAR / truck + rail":
    df = sonar_truck_rail_data()
else:
    df = demo_data()


# ===================================================
# CALCULATIONS
# ===================================================

df = df.copy()

for column in ["Truck Miles", "Truck Transit Days", "Rail Transit Days"]:
    if column not in df.columns:
        df[column] = None

df["Lane"] = df.apply(lambda row: normalize_lane(str(row["Origin"]), str(row["Destination"])), axis=1)

df["Truck Rate"] = pd.to_numeric(df["Truck Rate"], errors="coerce").fillna(0)
df["Rail Rate"] = pd.to_numeric(df["Rail Rate"], errors="coerce").fillna(0)
df["Truck Miles"] = pd.to_numeric(df["Truck Miles"], errors="coerce")

df["Adjusted Truck Rate"] = df["Truck Rate"] + fuel_adjustment
df["Adjusted Rail Rate"] = df["Rail Rate"] + rail_margin_buffer

df["Savings"] = df["Adjusted Truck Rate"] - df["Adjusted Rail Rate"]
df["Savings %"] = df["Savings"] / df["Adjusted Truck Rate"].replace(0, pd.NA)

df["Conversion Opportunity"] = df["Savings"].apply(
    lambda x: classify_opportunity(x, high_threshold, medium_threshold)
)

df["Truck RPM"] = df["Adjusted Truck Rate"] / df["Truck Miles"]
df["Rail RPM"] = df["Adjusted Rail Rate"] / df["Truck Miles"]

df["Last Updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")


# ===================================================
# METRICS
# ===================================================

high_count = int((df["Conversion Opportunity"] == "High").sum())
avg_savings = int(df["Savings"].mean())
max_savings = int(df["Savings"].max())
total_savings = int(df[df["Conversion Opportunity"] == "High"]["Savings"].sum())

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("High Conversion Lanes", high_count)

with col2:
    st.metric("Average Savings / Load", f"${avg_savings:,.0f}")

with col3:
    st.metric("Best Lane Savings", f"${max_savings:,.0f}")

with col4:
    st.metric("High-Lane Savings Pool", f"${total_savings:,.0f}")

st.caption(f"Last refreshed: {df['Last Updated'].iloc[0]} | Mode: {data_mode}")

st.divider()


# ===================================================
# FILTERS
# ===================================================

filter_col1, filter_col2 = st.columns([1, 2])

with filter_col1:
    selected_opportunities = st.multiselect(
        "Filter by opportunity level",
        ["High", "Medium", "Low"],
        default=["High", "Medium", "Low"],
    )

with filter_col2:
    lane_search = st.text_input("Search lane", "")

filtered_df = df[df["Conversion Opportunity"].isin(selected_opportunities)]

if lane_search:
    filtered_df = filtered_df[
        filtered_df["Lane"].str.contains(lane_search, case=False, na=False)
    ]


# ===================================================
# TABLE
# ===================================================

st.subheader("Lane Conversion Analysis")

display_columns = [
    "Lane",
    "Adjusted Truck Rate",
    "Adjusted Rail Rate",
    "Savings",
    "Savings %",
    "Truck RPM",
    "Rail RPM",
    "Truck Transit Days",
    "Rail Transit Days",
    "Conversion Opportunity",
    "Data Source",
]

st.dataframe(
    filtered_df[display_columns],
    use_container_width=True,
    hide_index=True,
    column_config={
        "Adjusted Truck Rate": st.column_config.NumberColumn(format="$%d"),
        "Adjusted Rail Rate": st.column_config.NumberColumn(format="$%d"),
        "Savings": st.column_config.NumberColumn(format="$%d"),
        "Savings %": st.column_config.ProgressColumn(format="%.1f", min_value=0, max_value=1),
        "Truck RPM": st.column_config.NumberColumn(format="$%.2f"),
        "Rail RPM": st.column_config.NumberColumn(format="$%.2f"),
    },
)


# ===================================================
# CHARTS
# ===================================================

st.subheader("Truck vs Rail Rate Comparison")

rate_chart = px.bar(
    filtered_df,
    x="Lane",
    y=["Adjusted Truck Rate", "Adjusted Rail Rate"],
    barmode="group",
    title="Truck vs Rail Pricing",
)

st.plotly_chart(rate_chart, use_container_width=True)

st.subheader("Rail Conversion Savings")

savings_chart = px.bar(
    filtered_df.sort_values("Savings", ascending=False),
    x="Lane",
    y="Savings",
    color="Conversion Opportunity",
    title="Estimated Savings by Lane",
    category_orders={"Conversion Opportunity": ["High", "Medium", "Low"]},
)

st.plotly_chart(savings_chart, use_container_width=True)


# ===================================================
# RECOMMENDATION
# ===================================================

st.subheader("Recommended Action")

if filtered_df.empty:
    st.info("No lanes match the current filters.")
else:
    best_lane = filtered_df.sort_values("Savings", ascending=False).iloc[0]

    st.success(
        f"Best current conversion target: {best_lane['Lane']} — "
        f"estimated savings of ${int(best_lane['Savings']):,} per load."
    )

    st.markdown(
        """
        **Suggested commercial action:**  
        Prioritize this lane for shipper conversion outreach. Validate origin/destination drayage,
        rail ramp pairing, service days, equipment availability, and minimum volume commitment.
        """
    )


# ===================================================
# API INTEGRATION NOTES
# ===================================================

with st.expander("How to connect real APIs"):
    st.markdown(
        """
        ### Recommended live data path

        **Truck rates**
        - DAT iQ / DAT API
        - FreightWaves SONAR TRAC or contract/spot rate data
        - Internal TMS rate history

        **Rail / intermodal rates**
        - FreightWaves SONAR intermodal datasets
        - Railroad/private IMC quote tables
        - TRT rate sheets uploaded as CSV

        ### Streamlit secrets example

        Add this in Streamlit Cloud:

        ```toml
        DAT_API_KEY = "your_dat_key_here"
        SONAR_API_KEY = "your_sonar_key_here"
        ```

        ### CSV upload format

        Required:
        - Origin
        - Destination
        - Truck Rate
        - Rail Rate

        Optional:
        - Truck Miles
        - Truck Transit Days
        - Rail Transit Days
        """
    )


# ===================================================
# FOOTER
# ===================================================

st.markdown("---")
st.caption("TRT Intermodal © 2026 | Live Truck-to-Rail Conversion Intelligence")
