import os
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st


# ===================================================
# PAGE CONFIG
# ===================================================

st.set_page_config(
    page_title="TRT Intermodal | Truck-to-Rail Conversion",
    layout="wide",
    page_icon="🚛",
)


# ===================================================
# TRT LOGO
# ===================================================

TRT_LOGO_BASE64 = "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6r7R7PC12OQLT/gafKUtNa9vfC2+UmUCd/iafKV6aE4jvjZfqTWnBl+jrwyaE75WmqrRjCZ8jb7S4evqW2tG3/hafeWh6Xp8zb4dvq6+T0034Gv2rTXdiK/ZV/D19X3g6+o74ovvT+zb44svvvjiiy+++OKLL7744osvvvjiiy+++OKLL7744osvvvjiiy++n+B7w3eGL/tT8cUX33+p5/0WfH9i30GTVfjafUfe3/T15f1uV9+G7xN4+laarMfX7jvxfRhX357vG7n6jpqqxNfuW2myAV+771OT3fG1+z40VSP4/nvzh2+Hr933ocnu+Jp9B03WCL7/0fxva+Br9b1rRi2+Rt+nZtQJvibf9qY5tfhafNtOs+oE31d9q6kvNa+mxfe/6//cMI6N5tcLvo6Vgq9jTYuvZ0/B17FB8HWsE3xdefF15cXX0XcQfP18m6fg6+db1oKvn28vgq+b79gKvm6+4ySCr5vv4y74us4Pjye+vte3csLXd312q/D1vb+Y8PX0Ve3x5fmOv69jY4Wvejbiq651+PrW4+vbhK9rjwpf1wZ8fZvwdW3E17c7vq6V+L6y//c2PvS1Jnxf3L8+9aXmd8M31/eP2qHR3Fp8De8PVYNm9o2vwVdkajSrEl+Tr7SlZtXia/KVqtGcnvjafKXWnG74Gn2l14wafD2/r6Fa4+v4fRjVJ76O3zdSHfA1+/aqfD/V0bdV5fu/jr5SKt+v9vQdlO+ve/reNd0TX7Nvq/z9izd/H1wHfO2+I38/y9W3w5e///b/9lV87TITvvjiiy+++OKLL7744osvvvjiiy+++OKLL7744osvvvjiiy+++OKLL7744osvvvjiiy+++OKLL7744osvvvjiiy+++OKLL7744osvviEytaar8TX7iqab8MUXX3zxxRdffF/07fG1+474vtt3wNfVd8TX7jtoshJfu2+v6fC1wzw1XY2v2XfSdHd8zb6VphvwNfvKQ5ON+Np9b5quwtfs+63p7viafWtN1+Gb4WufgBt87b6Dpnvia/atNd344b71mK6Wl6qmdJkWGfn4krVqSpe36vsNP+839prkVTkAAAAASUVORK5CYII="


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
        :root {
            --trt-navy: #002f44;
            --trt-blue: #67a6ba;
            --trt-light: #eef6f8;
            --trt-white: #ffffff;
            --trt-gray: #f4f7f9;
            --trt-text: #102a35;
        }

        .stApp {
            background: linear-gradient(180deg, #eef6f8 0%, #f7fafb 45%, #ffffff 100%);
            color: var(--trt-text);
        }

        .trt-header {
            background: linear-gradient(135deg, #002f44 0%, #06465d 55%, #67a6ba 100%);
            padding: 28px 32px;
            border-radius: 22px;
            margin-bottom: 26px;
            box-shadow: 0 10px 28px rgba(0, 47, 68, 0.25);
            border: 1px solid rgba(255,255,255,0.15);
        }

        .trt-header-inner {
            display: flex;
            align-items: center;
            gap: 26px;
        }

        .trt-logo-wrap {
            background: white;
            border-radius: 18px;
            padding: 12px 16px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.18);
        }

        .trt-logo {
            height: 86px;
            width: auto;
            display: block;
        }

        .trt-title {
            color: white;
            font-size: 38px;
            font-weight: 850;
            line-height: 1.05;
            letter-spacing: -0.5px;
        }

        .trt-subtitle {
            color: #d9edf2;
            font-size: 17px;
            margin-top: 10px;
            max-width: 980px;
        }

        .trt-pill {
            display: inline-block;
            margin-top: 14px;
            padding: 7px 12px;
            border-radius: 999px;
            background: rgba(255,255,255,0.14);
            color: #ffffff;
            font-size: 13px;
            font-weight: 700;
            border: 1px solid rgba(255,255,255,0.22);
        }

        div[data-testid="stMetric"] {
            background: white;
            padding: 18px 18px;
            border-radius: 18px;
            border-left: 6px solid #67a6ba;
            box-shadow: 0 4px 14px rgba(0,47,68,0.08);
        }

        div[data-testid="stMetric"] label {
            color: #002f44 !important;
            font-weight: 700;
        }

        div[data-testid="stMetricValue"] {
            color: #002f44;
        }

        .stButton > button {
            background-color: #002f44;
            color: white;
            border-radius: 12px;
            border: none;
            font-weight: 700;
        }

        .stButton > button:hover {
            background-color: #06465d;
            color: white;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #002f44 0%, #06394e 100%);
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] label {
            color: white !important;
        }

        section[data-testid="stSidebar"] input {
            color: #002f44 !important;
            background-color: white !important;
        }

        section[data-testid="stSidebar"] textarea {
            color: #002f44 !important;
            background-color: white !important;
        }

        section[data-testid="stSidebar"] .stNumberInput input {
            color: #002f44 !important;
            background-color: white !important;
        }

        section[data-testid="stSidebar"] div[data-baseweb="select"] {
            background-color: white !important;
        }

        section[data-testid="stSidebar"] div[data-baseweb="select"] * {
            color: #002f44 !important;
        }

        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: white !important;
        }

        hr {
            border-color: rgba(0,47,68,0.12);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="trt-header">
        <div class="trt-header-inner">
            <div class="trt-logo-wrap">
                <img class="trt-logo" src="data:image/png;base64,{TRT_LOGO_BASE64}">
            </div>
            <div>
                <div class="trt-title">Truck-to-Rail Conversion Dashboard</div>
                <div class="trt-subtitle">
                    TRT Intermodal intelligence for identifying lanes where truck pricing creates rail conversion opportunities.
                </div>
                <div class="trt-pill">Live-ready lane pricing · rail savings · conversion prioritization</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ===================================================
# SIDEBAR
# ===================================================

st.sidebar.image(f"data:image/png;base64,{TRT_LOGO_BASE64}", use_container_width=True)
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
st.sidebar.markdown("### How to Read It")
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
    color_discrete_sequence=["#002f44", "#67a6ba"],
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
    color_discrete_map={
        "High": "#002f44",
        "Medium": "#67a6ba",
        "Low": "#b8d7df",
    },
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
st.caption("TRT Intermodal © 2026 | Truck-to-Rail Conversion Intelligence")
