
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="WeatherProjector | Weather Intelligence",
    page_icon=":material/wb_sunny:",
    layout="wide",
    initial_sidebar_state="expanded"
)


def weather_icon(kind, color="#168AAD", size=38):
    icons = {
        "sun": """
            <circle cx="12" cy="12" r="4"/>
            <path d="M12 2v2 M12 20v2 M2 12h2 M20 12h2
            M4.93 4.93l1.42 1.42 M17.65 17.65l1.42 1.42
            M4.93 19.07l1.42-1.42 M17.65 6.35l1.42-1.42"/>
        """,
        "cloud": """
            <path d="M20 16.2A4.8 4.8 0 0 0 18 7h-1.2
            A7 7 0 1 0 4 16.2Z"/>
        """,
        "rain": """
            <path d="M20 16.2A4.8 4.8 0 0 0 18 7h-1.2
            A7 7 0 1 0 4 16.2Z"/>
            <path d="M8 19l-1 3 M13 19l-1 3 M18 19l-1 3"/>
        """,
        "temperature": """
            <path d="M14 14.76V5a2 2 0 0 0-4 0v9.76
            a4 4 0 1 0 4 0Z"/>
            <path d="M12 11v7"/>
        """,
        "humidity": """
            <path d="M12 2.5S5 10 5 15a7 7 0 0 0 14 0
            c0-5-7-12.5-7-12.5Z"/>
        """,
        "wind": """
            <path d="M3 8h12a3 3 0 1 0-3-3"/>
            <path d="M2 12h17a3 3 0 1 1-3 3"/>
            <path d="M4 16h6"/>
        """
    }

    return f"""
    <svg xmlns="http://www.w3.org/2000/svg"
         width="{size}" height="{size}" viewBox="0 0 24 24"
         fill="none" stroke="{color}" stroke-width="1.8"
         stroke-linecap="round" stroke-linejoin="round">
         {icons[kind]}
    </svg>
    """


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Poppins:wght@400;500;600;700;800&display=swap');

:root {
    --navy: #12334D;
    --blue: #087EAD;
    --sky: #39A9DB;
    --orange: #FF8243;
    --gold: #FFB45B;
    --teal: #20B8A6;
    --muted: #536D82;
    --border: #D6E9F4;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #EAF6FC 0%, #F5FAFD 55%, #FFF0E5 100%);
    color: var(--navy);
}

.block-container {
    max-width: 1600px;
    padding: 2rem 2.5rem 4rem;
}

[data-testid="stHeader"] {
    background: rgba(255,255,255,0.95);
}

/* Main headings */
h1, h2, h3, h4,
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {
    font-family: 'Poppins', sans-serif !important;
    font-style: normal !important;
    color: var(--navy) !important;
    font-weight: 700 !important;
    letter-spacing: -0.55px !important;
}

h1 { font-size: 2.6rem !important; }
h2 { font-size: 2rem !important; }
h3 { font-size: 1.45rem !important; }

p, label, li {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px;
}

/* Hero */
.hero {
    background: linear-gradient(115deg, #064B70 0%, #087EAD 38%, #39A9DB 72%, #FF8243 115%);
    padding: 45px;
    border-radius: 24px;
    margin-bottom: 32px;
    box-shadow: 0 15px 35px rgba(8, 92, 135, 0.22);
    position: relative;
    overflow: hidden;
}

.hero h1 {
    color: #FFFFFF !important;
    font-family: 'Poppins', sans-serif !important;
    font-style: normal !important;
    font-size: 44px !important;
    font-weight: 800 !important;
    letter-spacing: -1px !important;
    margin: 8px 0 10px;
}

.hero p {
    color: #EFFAFF !important;
    font-size: 17px !important;
    line-height: 1.7;
    max-width: 850px;
}

.hero-tag {
    display: inline-block;
    background: rgba(255,255,255,0.18);
    border: 1px solid rgba(255,255,255,0.4);
    border-radius: 30px;
    padding: 8px 16px;
    color: white;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 1px;
}

.hero-icon {
    position: absolute;
    right: 65px;
    top: 40px;
    opacity: 0.9;
}

/* KPI cards */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 20px;
    margin: 20px 0;
}

.custom-metric {
    background: linear-gradient(145deg, #FFFFFF, #F0F8FD);
    border: 1px solid var(--border);
    border-radius: 19px;
    padding: 24px;
    min-height: 165px;
    box-shadow: 0 8px 22px rgba(20, 75, 110, 0.09);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.custom-metric:hover {
    transform: translateY(-4px);
    box-shadow: 0 14px 28px rgba(20, 75, 110, 0.14);
}

.metric-icon {
    margin-bottom: 13px;
}

.metric-label {
    font-family: 'DM Sans', sans-serif !important;
    color: var(--muted);
    font-size: 14px;
    font-weight: 600;
    font-style: normal;
    letter-spacing: 0.1px;
}

.metric-value {
    font-family: 'DM Sans', sans-serif !important;
    color: #087EAD !important;
    font-size: 34px !important;
    font-style: normal !important;
    font-weight: 700 !important;
    letter-spacing: -1px !important;
    line-height: 1.25;
    margin-top: 7px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #DDF1FC, #EDF7FC 65%, #FFF0E5);
    border-right: 1px solid #D2E6F2;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #075985 !important;
    font-family: 'Poppins', sans-serif !important;
    font-style: normal !important;
    font-weight: 700 !important;
}

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p {
    color: #244B67 !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}

/* Date and multiselect fields */
section[data-testid="stSidebar"] [data-testid="stDateInput"] input {
    background: rgba(255,255,255,0.82) !important;
    border: 1px solid #C9DFEC !important;
    border-radius: 12px !important;
    padding: 10px 13px !important;
    color: #244B67 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease;
}

section[data-testid="stSidebar"] [data-testid="stDateInput"] input:focus {
    border-color: #39A9DB !important;
    box-shadow: 0 0 0 3px rgba(57,169,219,0.15) !important;
}

section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    border-radius: 12px !important;
    border-color: #C9DFEC !important;
    background: rgba(255,255,255,0.82) !important;
}

.stMultiSelect [data-baseweb="tag"] {
    background: linear-gradient(120deg, #FF925C, #FF8243) !important;
    border: 1px solid rgba(255,255,255,0.4) !important;
    border-radius: 8px !important;
    padding: 3px 6px !important;
    box-shadow: 0 2px 5px rgba(255,130,67,0.10);
}

.stMultiSelect [data-baseweb="tag"] span {
    color: white !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    font-style: normal !important;
}

[role="option"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    color: #244B67 !important;
    padding: 10px 13px !important;
}

[role="option"]:hover {
    background: #E6F4FC !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    display: flex;
    gap: 8px;
    background: rgba(255,255,255,0.72);
    padding: 8px;
    border: 1px solid #DCEBF4;
    border-radius: 15px;
    box-shadow: 0 5px 16px rgba(20,70,110,0.05);
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 10px;
    padding: 11px 19px;
    color: #42657D !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    font-style: normal !important;
    border: 1px solid transparent;
    transition: all 0.2s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    background: #EAF5FC;
    color: #087EAD !important;
    border-color: #D6E9F4;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(120deg, #087EAD, #39A9DB) !important;
    color: #FFFFFF !important;
    border: 1px solid #39A9DB;
    box-shadow: 0 4px 12px rgba(8,126,173,0.18);
}

.stTabs [data-baseweb="tab-highlight"] {
    display: none;
}

/* Charts and tables */
[data-testid="stPlotlyChart"] {
    background: white;
    border: 1px solid #DCEBF4;
    border-radius: 17px;
    padding: 12px;
    box-shadow: 0 7px 22px rgba(20,70,110,0.07);
    margin-top: 12px;
    margin-bottom: 22px;
}

[data-testid="stDataFrame"] {
    border: 1px solid #D8E8F2;
    border-radius: 13px;
    overflow: hidden;
}

[data-testid="stExpander"] {
    background: white;
    border: 1px solid #D8E8F2;
    border-radius: 14px;
}

/* Download button */
div[data-testid="stDownloadButton"] button {
    background: linear-gradient(100deg, #087EAD, #FF8243);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 13px 24px;
    font-size: 15px;
    font-weight: 700;
}

div[data-testid="stDownloadButton"] button:hover {
    color: white;
    background: linear-gradient(100deg, #075985, #E86B32);
}

/* Dividers and captions */
hr {
    border-color: #D4E5F0;
    margin-top: 30px;
    margin-bottom: 30px;
}

[data-testid="stCaptionContainer"] p {
    font-size: 13px !important;
    color: #7892A7 !important;
}

/* Footer */
.footer {
    background: linear-gradient(110deg, #064B70, #087EAD, #168AAD);
    padding: 28px;
    text-align: center;
    border-radius: 18px;
}

.footer h3 {
    color: white !important;
    font-family: 'Poppins', sans-serif !important;
    font-style: normal !important;
}

.footer p {
    color: #E5F7FF !important;
    font-size: 14px !important;
}

/* Responsive layout */
@media (max-width: 1000px) {
    .metric-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .block-container {
        padding: 1.2rem;
    }
}

@media (max-width: 600px) {
    .metric-grid {
        grid-template-columns: 1fr;
    }

    .hero {
        padding: 25px;
    }

    .hero h1 {
        font-size: 32px !important;
    }

    .hero-icon {
        display: none;
    }
}
</style>
""", unsafe_allow_html=True)


def style_chart(fig, height=560):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(
            family="DM Sans",
            color="#243F56",
            size=15
        ),
        title=dict(
            font=dict(
                family="Poppins",
                size=23,
                color="#075985"
            ),
            x=0.02
        ),
        height=height,
        autosize=True,
        margin=dict(l=65, r=45, t=95, b=70),
        hoverlabel=dict(
            bgcolor="#075985",
            font=dict(color="#FFFFFF", size=14)
        ),
        legend=dict(
            font=dict(size=14),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#E7EFF5",
        linecolor="#C8DCE9",
        tickfont=dict(size=13, color="#40566B"),
        title_font=dict(size=15, color="#142D45")
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#E7EFF5",
        linecolor="#C8DCE9",
        tickfont=dict(size=13, color="#40566B"),
        title_font=dict(size=15, color="#142D45")
    )

    return fig


DATA_PATH = (
    Path(__file__).parent
    / "datasets"
    / "Weather Prediction Dataset.csv"
)


@st.cache_data
def load_data(path):
    data = pd.read_csv(path)

    required_columns = [
        "DATE", "temp", "tempmax", "tempmin",
        "humidity", "precip", "windspeed", "conditions"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in data.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    data["DATE"] = pd.to_datetime(data["DATE"], errors="coerce")
    data = data.dropna(subset=["DATE"])
    data = data.sort_values("DATE")

    return data


if not DATA_PATH.exists():
    st.error(f"Dataset not found: {DATA_PATH}")
    st.stop()

try:
    df = load_data(str(DATA_PATH))
except Exception as error:
    st.error(f"Unable to load dataset: {error}")
    st.stop()


st.markdown(f"""
<div class="hero">
    <div class="hero-tag">WEATHER INTELLIGENCE · DATA ANALYTICS</div>
    <div class="hero-icon">{weather_icon("sun", "#FFD166", 105)}</div>
    <h1>WeatherProjector</h1>
    <p>Discover the patterns behind every season.</p>
    <p>Explore historical temperatures, rainfall, humidity and atmospheric behaviour through interactive visual analytics.</p>
</div>
""", unsafe_allow_html=True)


st.sidebar.markdown("""
<div style="padding:12px 0 20px 0;">
    <h2 style="font-size:25px;color:#075985;">Dashboard Controls</h2>
    <p style="font-size:14px;color:#42657D;">Personalise your weather exploration.</p>
</div>
""", unsafe_allow_html=True)

min_date = df["DATE"].min().date()
max_date = df["DATE"].max().date()

date_range = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

filtered_df = df.copy()

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range

    filtered_df = filtered_df[
        (filtered_df["DATE"].dt.date >= start_date) &
        (filtered_df["DATE"].dt.date <= end_date)
    ]

if "season" in filtered_df.columns:
    seasons = sorted(filtered_df["season"].dropna().unique())

    selected_seasons = st.sidebar.multiselect(
        "Select season",
        seasons,
        default=seasons
    )

    filtered_df = filtered_df[
        filtered_df["season"].isin(selected_seasons)
    ]

conditions = sorted(filtered_df["conditions"].dropna().unique())

selected_conditions = st.sidebar.multiselect(
    "Weather conditions",
    conditions,
    default=conditions
)

filtered_df = filtered_df[
    filtered_df["conditions"].isin(selected_conditions)
]

if filtered_df.empty:
    st.warning("No records match the selected filters.")
    st.stop()


st.header("Weather Overview")

metrics = [
    (
        "temperature",
        "Average Temperature",
        f"{filtered_df['temp'].mean():.1f}°",
        "#FF8243"
    ),
    (
        "humidity",
        "Average Humidity",
        f"{filtered_df['humidity'].mean():.1f}%",
        "#168AAD"
    ),
    (
        "rain",
        "Total Rainfall",
        f"{filtered_df['precip'].sum():,.2f}",
        "#20B8A6"
    ),
    (
        "cloud",
        "Rainfall Days",
        str(int((filtered_df["precip"] > 0).sum())),
        "#E99A43"
    )
]

metric_html = '<div class="metric-grid">'

for kind, label, value, color in metrics:
    metric_html += f"""
    <div class="custom-metric">
        <div class="metric-icon">
            {weather_icon(kind, color, 38)}
        </div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """

metric_html += "</div>"

st.html(metric_html)

st.caption(
    f"Displaying {len(filtered_df):,} records | "
    f"{filtered_df['DATE'].min().date()} to "
    f"{filtered_df['DATE'].max().date()}"
)


st.divider()
st.header("Monthly Weather Analysis")

monthly = (
    filtered_df.set_index("DATE")
    .resample("MS")
    .agg({
        "temp": "mean",
        "tempmax": "mean",
        "tempmin": "mean",
        "humidity": "mean",
        "precip": "sum",
        "windspeed": "mean"
    })
    .reset_index()
)

tab1, tab2, tab3 = st.tabs([
    "Temperature",
    "Rainfall",
    "Humidity & Wind"
])


with tab1:
    fig_temp = go.Figure()

    fig_temp.add_trace(go.Scatter(
        x=monthly["DATE"],
        y=monthly["tempmax"],
        name="Maximum Temperature",
        mode="lines+markers",
        line=dict(color="#FF8243", width=4),
        marker=dict(size=7)
    ))

    fig_temp.add_trace(go.Scatter(
        x=monthly["DATE"],
        y=monthly["temp"],
        name="Average Temperature",
        mode="lines+markers",
        line=dict(color="#087EAD", width=4),
        marker=dict(size=7)
    ))

    fig_temp.add_trace(go.Scatter(
        x=monthly["DATE"],
        y=monthly["tempmin"],
        name="Minimum Temperature",
        mode="lines+markers",
        line=dict(color="#39A9DB", width=3),
        marker=dict(size=6)
    ))

    fig_temp.update_layout(
        title="Monthly Temperature Trends",
        xaxis_title="Month",
        yaxis_title="Temperature (dataset units)",
        hovermode="x unified"
    )

    fig_temp = style_chart(fig_temp, 600)

    st.plotly_chart(
        fig_temp,
        use_container_width=True,
        config={"displayModeBar": True, "responsive": True}
    )


with tab2:
    fig_rain = px.bar(
        monthly,
        x="DATE",
        y="precip",
        title="Monthly Total Rainfall",
        labels={
            "DATE": "Month",
            "precip": "Rainfall (dataset units)"
        },
        color="precip",
        color_continuous_scale=[
            "#D8F3FC",
            "#39A9DB",
            "#087EAD",
            "#075985"
        ]
    )

    fig_rain = style_chart(fig_rain, 570)

    st.plotly_chart(
        fig_rain,
        use_container_width=True,
        config={"displayModeBar": True, "responsive": True}
    )

    fig_rain_daily = px.area(
        filtered_df,
        x="DATE",
        y="precip",
        title="Daily Rainfall Distribution",
        labels={
            "DATE": "Date",
            "precip": "Rainfall (dataset units)"
        }
    )

    fig_rain_daily.update_traces(
        line_color="#168AAD",
        fillcolor="rgba(57,169,219,0.25)"
    )

    fig_rain_daily = style_chart(fig_rain_daily, 550)

    st.plotly_chart(
        fig_rain_daily,
        use_container_width=True,
        config={"displayModeBar": True, "responsive": True}
    )


with tab3:
    col_a, col_b = st.columns(2, gap="large")

    with col_a:
        fig_humidity = px.line(
            monthly,
            x="DATE",
            y="humidity",
            title="Monthly Average Humidity",
            markers=True
        )

        fig_humidity.update_traces(
            line_color="#20B8A6",
            line_width=4,
            marker_size=9
        )

        fig_humidity = style_chart(fig_humidity, 550)

        st.plotly_chart(
            fig_humidity,
            use_container_width=True,
            config={"responsive": True}
        )

    with col_b:
        fig_wind = px.bar(
            monthly,
            x="DATE",
            y="windspeed",
            title="Monthly Average Wind Speed",
            color="windspeed",
            color_continuous_scale=[
                "#FFE0C2",
                "#FFB45B",
                "#FF8243",
                "#E45A35"
            ]
        )

        fig_wind = style_chart(fig_wind, 550)

        st.plotly_chart(
            fig_wind,
            use_container_width=True,
            config={"responsive": True}
        )


st.divider()
st.header("Weather Correlation Analysis")

correlation_columns = [
    "tempmax",
    "tempmin",
    "temp",
    "humidity",
    "precip",
    "windspeed",
    "sealevelpressure"
]

available_columns = [
    col for col in correlation_columns
    if col in filtered_df.columns
]

correlation = filtered_df[available_columns].corr()

fig_corr = px.imshow(
    correlation,
    text_auto=".2f",
    color_continuous_scale=[
        "#087EAD",
        "#39A9DB",
        "#F7FBFF",
        "#FFB45B",
        "#FF7043",
        "#C63D2F"
    ],
    zmin=-1,
    zmax=1,
    aspect="auto",
    title="Relationship Between Weather Variables"
)

fig_corr.update_traces(
    textfont=dict(size=16, color="#142D45")
)

fig_corr = style_chart(fig_corr, 720)

st.plotly_chart(
    fig_corr,
    use_container_width=True,
    config={"displayModeBar": True, "responsive": True}
)


st.divider()
st.header("Extreme Weather Records")

extreme_tab1, extreme_tab2, extreme_tab3 = st.tabs([
    "Hottest Days",
    "Coldest Days",
    "Rainiest Days"
])

with extreme_tab1:
    st.dataframe(
        filtered_df.nlargest(5, "tempmax")[
            ["DATE", "tempmax", "tempmin", "humidity"]
        ],
        use_container_width=True,
        hide_index=True,
        height=300
    )

with extreme_tab2:
    st.dataframe(
        filtered_df.nsmallest(5, "tempmin")[
            ["DATE", "tempmax", "tempmin", "humidity"]
        ],
        use_container_width=True,
        hide_index=True,
        height=300
    )

with extreme_tab3:
    st.dataframe(
        filtered_df.nlargest(5, "precip")[
            ["DATE", "precip", "humidity", "conditions"]
        ],
        use_container_width=True,
        hide_index=True,
        height=300
    )


st.divider()
st.header("Dataset Explorer")

with st.expander("Explore all weather records"):
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        height=550
    )

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Dataset",
    data=csv_data,
    file_name="WeatherProjector_Filtered_Data.csv",
    mime="text/csv"
)


st.divider()

st.markdown("""
<div class="footer">
    <h3>WeatherProjector</h3>
    <p>Turning historical weather data into meaningful insights.</p>
    <p>Built with Python | Pandas | Plotly | Streamlit</p>
</div>
""", unsafe_allow_html=True)
