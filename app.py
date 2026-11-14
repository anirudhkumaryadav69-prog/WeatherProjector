import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="WeatherProjector | Weather Intelligence",
    page_icon=":material/wb_sunny:",
    layout="wide",
    initial_sidebar_state="auto"
)


def weather_icon(kind, color="#087EAD", size=32):
    icons = {
        "sun": (
            '<circle cx="12" cy="12" r="4"/>'
            '<path d="M12 2v2 M12 20v2 M2 12h2 M20 12h2 '
            'M4.93 4.93l1.42 1.42 M17.65 17.65l1.42 1.42 '
            'M4.93 19.07l1.42-1.42 M17.65 6.35l1.42-1.42"/>'
        ),
        "cloud": (
            '<path d="M20 16.2A4.8 4.8 0 0 0 18 7h-1.2 '
            'A7 7 0 1 0 4 16.2Z"/>'
        ),
        "rain": (
            '<path d="M20 16.2A4.8 4.8 0 0 0 18 7h-1.2 '
            'A7 7 0 1 0 4 16.2Z"/>'
            '<path d="M8 19l-1 3 M13 19l-1 3 M18 19l-1 3"/>'
        ),
        "temperature": (
            '<path d="M14 14.76V5a2 2 0 0 0-4 0v9.76 '
            'a4 4 0 1 0 4 0Z"/>'
            '<path d="M12 11v7"/>'
        ),
        "humidity": (
            '<path d="M12 2.5S5 10 5 15a7 7 0 0 0 14 0 '
            'c0-5-7-12.5-7-12.5Z"/>'
        ),
        "wind": (
            '<path d="M3 8h12a3 3 0 1 0-3-3"/>'
            '<path d="M2 12h17a3 3 0 1 1-3 3"/>'
            '<path d="M4 16h6"/>'
        )
    }

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{size}" height="{size}" viewBox="0 0 24 24" '
        f'fill="none" stroke="{color}" stroke-width="1.9" '
        f'stroke-linecap="round" stroke-linejoin="round" '
        f'style="flex-shrink:0; display:block;">'
        f'{icons[kind]}</svg>'
    )


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&family=Poppins:wght@500;600;700;800&display=swap');

:root {
    --navy: #0F2942;
    --navy-soft: #1E3A5F;
    --blue: #087EAD;
    --blue-dark: #065A82;
    --sky: #38A3D1;
    --sky-light: #EBF5FB;
    --sky-tint: #F4F9FD;
    --orange: #F27438;
    --orange-soft: #FFF3EC;
    --amber: #E59838;
    --teal: #189AB4;
    --muted: #5A7184;
    --border: #DCEBF5;
    --surface: #FFFFFF;
    --shadow-sm: 0 2px 10px rgba(15, 41, 66, 0.04);
    --shadow-md: 0 8px 24px rgba(15, 41, 66, 0.06);
    --shadow-hover: 0 12px 28px rgba(8, 126, 173, 0.11);
    --radius-lg: 20px;
    --radius-md: 14px;
    --radius-sm: 10px;
}

*, *::before, *::after {
    box-sizing: border-box;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--navy);
    overflow-x: hidden;
}

.stApp {
    background-color: var(--sky-tint);
    background-image: radial-gradient(circle at 10% 0%, #E6F3FB 0%, #F4F9FD 45%, #FAFCFF 100%);
    color: var(--navy);
    overflow-x: hidden;
}

.block-container {
    max-width: 1440px;
    padding: 1.75rem 2.25rem 3.5rem;
    overflow-x: hidden;
}

[data-testid="stHeader"] {
    background: rgba(244, 249, 253, 0.88);
    backdrop-filter: blur(8px);
}

/* Touch-friendly sidebar toggle controls */
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"] button,
button[kind="header"] {
    min-width: 44px !important;
    min-height: 44px !important;
    border-radius: 10px !important;
}

/* Typography & Responsive Headings */
h1, h2, h3, h4,
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {
    font-family: 'Poppins', sans-serif !important;
    font-style: normal !important;
    color: var(--navy) !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
    line-height: 1.25 !important;
    overflow-wrap: break-word;
    word-wrap: break-word;
}

h1, .stApp h1 {
    font-size: clamp(1.65rem, 3.5vw, 2.45rem) !important;
}

h2, .stApp h2 {
    font-size: clamp(1.25rem, 2.4vw, 1.65rem) !important;
    margin-top: 0.25rem !important;
    margin-bottom: 0.4rem !important;
}

h3, .stApp h3 {
    font-size: clamp(1.05rem, 1.8vw, 1.3rem) !important;
}

p, label, li {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem;
    line-height: 1.6;
}

/* Section Heading Wrapper */
.section-header {
    display: flex;
    flex-direction: column;
    gap: 4px;
    margin: 0.25rem 0 1rem 0;
}

.section-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--blue);
}

.section-eyebrow::before {
    content: "";
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--orange);
}

.section-subtitle {
    color: var(--muted);
    font-size: 0.9rem;
    margin: 0;
}

/* Hero Banner */
.hero {
    background: linear-gradient(135deg, #0D3554 0%, #087EAD 68%, #2E9CCA 100%);
    padding: 36px 40px;
    border-radius: var(--radius-lg);
    margin-bottom: 24px;
    box-shadow: 0 12px 32px rgba(13, 53, 84, 0.14);
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.15);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
}

.hero::after {
    content: "";
    position: absolute;
    right: -60px;
    bottom: -80px;
    width: 260px;
    height: 260px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255, 180, 91, 0.22) 0%, rgba(255, 180, 91, 0) 70%);
    pointer-events: none;
}

.hero-content {
    position: relative;
    z-index: 1;
    flex: 1 1 auto;
    min-width: 0;
}

.hero-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
}

.hero-tag {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255, 255, 255, 0.14);
    border: 1px solid rgba(255, 255, 255, 0.28);
    border-radius: 999px;
    padding: 6px 14px;
    color: #FFFFFF;
    font-size: 0.74rem;
    font-weight: 700;
    letter-spacing: 0.07em;
    text-transform: uppercase;
}

.hero-tag-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #FFB45B;
    display: inline-block;
}

.hero h1 {
    color: #FFFFFF !important;
    font-family: 'Poppins', sans-serif !important;
    font-size: clamp(1.75rem, 4vw, 2.5rem) !important;
    font-weight: 700 !important;
    letter-spacing: -0.025em !important;
    margin: 12px 0 8px 0 !important;
    line-height: 1.18 !important;
}

.hero p {
    color: rgba(240, 249, 255, 0.92) !important;
    font-size: clamp(0.92rem, 1.6vw, 1.04rem) !important;
    line-height: 1.6 !important;
    max-width: 720px;
    margin: 0 0 6px 0 !important;
}

.hero-icon {
    position: relative;
    z-index: 1;
    flex-shrink: 0;
    opacity: 0.94;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    padding: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Active Filter Status Bar */
.filter-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 12px 18px;
    margin-bottom: 22px;
    box-shadow: var(--shadow-sm);
}

.filter-bar-left {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 10px;
    font-size: 0.86rem;
    color: var(--muted);
    font-weight: 500;
}

.filter-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--sky-light);
    color: var(--blue-dark);
    border: 1px solid #CBE4F5;
    border-radius: 999px;
    padding: 4px 12px;
    font-size: 0.8rem;
    font-weight: 600;
}

.filter-pill-orange {
    background: var(--orange-soft);
    color: #C85018;
    border-color: #FAD5C0;
}

/* KPI Cards Grid */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 18px;
    margin: 14px 0 18px 0;
}

.custom-metric {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 20px 22px;
    box-shadow: var(--shadow-sm);
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-width: 0;
    position: relative;
    overflow: hidden;
}

.custom-metric::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--card-accent, var(--blue));
    opacity: 0.85;
}

.custom-metric:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-hover);
    border-color: #B8D9EE;
}

.metric-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    margin-bottom: 12px;
}

.metric-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: var(--icon-bg, var(--sky-light));
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.metric-label {
    font-family: 'DM Sans', sans-serif !important;
    color: var(--muted);
    font-size: 0.85rem;
    font-weight: 600;
    line-height: 1.35;
    overflow-wrap: break-word;
}

.metric-value {
    font-family: 'Poppins', sans-serif !important;
    color: var(--navy) !important;
    font-size: clamp(1.45rem, 2.4vw, 2rem) !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
    line-height: 1.2;
    margin-top: 2px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.25rem;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: var(--navy) !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 700 !important;
}

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p {
    color: var(--navy-soft) !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
}

/* Touch-friendly Date and Multiselect Inputs */
section[data-testid="stSidebar"] [data-testid="stDateInput"] input {
    background: var(--sky-tint) !important;
    border: 1px solid #C9DFEC !important;
    border-radius: var(--radius-sm) !important;
    padding: 10px 12px !important;
    min-height: 44px !important;
    color: var(--navy) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

section[data-testid="stSidebar"] [data-testid="stDateInput"] input:focus {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 3px rgba(8, 126, 173, 0.14) !important;
    background: #FFFFFF !important;
}

section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    border-radius: var(--radius-sm) !important;
    border-color: #C9DFEC !important;
    background: var(--sky-tint) !important;
    min-height: 44px !important;
    padding: 2px 6px !important;
}

.stMultiSelect [data-baseweb="tag"] {
    background: var(--sky-light) !important;
    border: 1px solid #BDDEF2 !important;
    border-radius: 7px !important;
    padding: 3px 8px !important;
    margin: 2px !important;
}

.stMultiSelect [data-baseweb="tag"] span {
    color: var(--blue-dark) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
}

[role="option"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
    color: var(--navy) !important;
    padding: 10px 14px !important;
    min-height: 42px !important;
}

[role="option"]:hover {
    background: var(--sky-light) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    display: flex;
    flex-wrap: nowrap;
    overflow-x: auto;
    gap: 6px;
    background: var(--surface);
    padding: 6px;
    border: 1px solid var(--border);
    border-radius: 13px;
    box-shadow: var(--shadow-sm);
    scrollbar-width: none;
    -ms-overflow-style: none;
}

.stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
    display: none;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 9px;
    padding: 10px 18px;
    min-height: 42px;
    color: var(--muted) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    border: 1px solid transparent;
    transition: all 0.18s ease;
    white-space: nowrap;
    flex-shrink: 0;
}

.stTabs [data-baseweb="tab"]:hover {
    background: var(--sky-tint);
    color: var(--blue) !important;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: var(--blue) !important;
    color: #FFFFFF !important;
    border: 1px solid var(--blue);
    box-shadow: 0 3px 10px rgba(8, 126, 173, 0.2);
}

.stTabs [data-baseweb="tab"][aria-selected="true"] p {
    color: #FFFFFF !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    display: none;
}

/* Charts, Tables & Expanders */
[data-testid="stPlotlyChart"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 10px 12px 6px;
    box-shadow: var(--shadow-sm);
    margin-top: 8px;
    margin-bottom: 18px;
    width: 100% !important;
    max-width: 100% !important;
    overflow: hidden;
}

[data-testid="stPlotlyChart"] .js-plotly-plot,
[data-testid="stPlotlyChart"] .plot-container,
[data-testid="stPlotlyChart"] .svg-container {
    width: 100% !important;
    max-width: 100% !important;
}

[data-testid="stDataFrame"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
}

[data-testid="stExpander"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-sm);
    overflow: hidden;
}

[data-testid="stExpander"] summary {
    min-height: 46px;
    padding: 12px 16px !important;
    font-weight: 600 !important;
}

/* Download Button */
div[data-testid="stDownloadButton"] button {
    background: var(--blue);
    color: #FFFFFF !important;
    border: 1px solid var(--blue-dark);
    border-radius: var(--radius-sm);
    padding: 12px 22px;
    min-height: 46px;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem;
    font-weight: 600;
    box-shadow: 0 4px 12px rgba(8, 126, 173, 0.18);
    transition: background 0.2s ease, transform 0.15s ease, box-shadow 0.2s ease;
}

div[data-testid="stDownloadButton"] button:hover {
    background: var(--blue-dark);
    color: #FFFFFF !important;
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(8, 126, 173, 0.25);
}

/* Dividers & Captions */
hr {
    border: none;
    border-top: 1px solid var(--border);
    margin: 26px 0 !important;
}

[data-testid="stCaptionContainer"] p {
    font-size: 0.83rem !important;
    color: var(--muted) !important;
}

/* Footer */
.footer {
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 24px 28px;
    text-align: center;
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-sm);
    margin-top: 8px;
}

.footer h3 {
    color: var(--navy) !important;
    font-family: 'Poppins', sans-serif !important;
    font-size: 1.15rem !important;
    margin: 0 0 6px 0 !important;
}

.footer p {
    color: var(--muted) !important;
    font-size: 0.85rem !important;
    margin: 2px 0 !important;
}

.footer-badges {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 12px;
}

.footer-badge {
    background: var(--sky-tint);
    border: 1px solid var(--border);
    color: var(--navy-soft);
    font-size: 0.76rem;
    font-weight: 600;
    padding: 4px 11px;
    border-radius: 999px;
}

/* =========================================================
   Responsive Breakpoints (Tablet, Mobile 430px, Mobile 375px)
   ========================================================= */

@media (max-width: 1024px) {
    .block-container {
        padding: 1.35rem 1.4rem 2.75rem;
    }

    .metric-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 14px;
    }

    .hero {
        padding: 28px 30px;
    }

    .hero-icon {
        right: 24px;
        padding: 14px;
    }
}

@media (max-width: 768px) {
    .block-container {
        padding: 1rem 0.95rem 2.5rem;
    }

    .hero {
        padding: 22px 20px;
        border-radius: 16px;
        margin-bottom: 18px;
    }

    .hero-icon {
        display: none;
    }

    .filter-bar {
        padding: 10px 14px;
        margin-bottom: 16px;
    }

    .metric-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 12px;
    }

    .custom-metric {
        padding: 16px;
    }

    .metric-icon {
        width: 38px;
        height: 38px;
        border-radius: 10px;
    }

    [data-testid="stPlotlyChart"] {
        padding: 6px 6px 4px;
        border-radius: 12px;
    }

    /* Scale Plotly SVG text smoothly on tablets & phones */
    .js-plotly-plot .plotly .gtitle {
        font-size: 14.5px !important;
    }

    .js-plotly-plot .plotly .xtick text,
    .js-plotly-plot .plotly .ytick text {
        font-size: 11px !important;
    }

    .js-plotly-plot .plotly .g-xtitle text,
    .js-plotly-plot .plotly .g-ytitle text {
        font-size: 12px !important;
    }

    .js-plotly-plot .plotly .legend text {
        font-size: 11px !important;
    }

    .js-plotly-plot .plotly .heatmaplayer text,
    .st-key-corr_chart_box .js-plotly-plot .plotly .annotation-text {
        font-size: 10.5px !important;
    }

    div[data-testid="stDownloadButton"] button {
        width: 100%;
    }
}

@media (max-width: 580px) {
    /* On mobile screens (375px - 430px), hide dense heatmap cell annotations
       so they never overlap; exact values remain accessible via tap/hover tooltips */
    .js-plotly-plot .plotly .heatmaplayer text,
    .st-key-corr_chart_box .js-plotly-plot .plotly .annotation,
    .st-key-corr_chart_box .js-plotly-plot .plotly .annotation-text {
        display: none !important;
    }

    .js-plotly-plot .plotly .modebar {
        display: none !important;
    }

    .js-plotly-plot .plotly .gtitle {
        font-size: 13.5px !important;
    }

    .js-plotly-plot .plotly .xtick text,
    .js-plotly-plot .plotly .ytick text {
        font-size: 10px !important;
    }

    .js-plotly-plot .plotly .cbaxis text {
        font-size: 9.5px !important;
    }
}

@media (max-width: 480px) {
    .block-container {
        padding: 0.85rem 0.75rem 2.25rem;
    }

    .hero {
        padding: 18px 16px;
    }

    .hero-tag {
        font-size: 0.68rem;
        padding: 4px 10px;
    }

    .metric-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 10px;
    }

    .custom-metric {
        padding: 14px 12px;
    }

    .metric-top {
        margin-bottom: 8px;
    }

    .metric-icon {
        width: 34px;
        height: 34px;
    }

    .metric-label {
        font-size: 0.78rem;
    }

    .metric-value {
        font-size: 1.3rem !important;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 8px 13px;
        font-size: 0.82rem !important;
    }

    .footer {
        padding: 18px 16px;
    }
}

@media (max-width: 350px) {
    .metric-grid {
        grid-template-columns: 1fr;
    }
}
</style>
""", unsafe_allow_html=True)


def section_heading(eyebrow, title, subtitle=None):
    subtitle_html = f'<p class="section-subtitle">{subtitle}</p>' if subtitle else ""
    st.html(
        f'<div class="section-header">'
        f'<span class="section-eyebrow">{eyebrow}</span>'
        f'<h2>{title}</h2>'
        f'{subtitle_html}'
        f'</div>'
    )


def style_chart(fig, height=480, show_legend=True):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(
            family="DM Sans, sans-serif",
            color="#1E3A5F",
            size=13
        ),
        title=dict(
            font=dict(
                family="Poppins, sans-serif",
                size=17,
                color="#0F2942"
            ),
            x=0.01,
            xanchor="left",
            y=0.96,
            yanchor="top"
        ),
        height=height,
        autosize=True,
        margin=dict(l=48, r=22, t=64, b=68 if show_legend else 52),
        hoverlabel=dict(
            bgcolor="#0F2942",
            bordercolor="#0F2942",
            font=dict(family="DM Sans, sans-serif", color="#FFFFFF", size=13)
        ),
        showlegend=show_legend,
        legend=dict(
            font=dict(size=12, color="#1E3A5F"),
            orientation="h",
            yanchor="top",
            y=-0.16,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0)"
        )
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#EDF4F9",
        linecolor="#D5E5F0",
        tickfont=dict(size=12, color="#4A6378"),
        title_font=dict(size=13, color="#1E3A5F"),
        automargin=True
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#EDF4F9",
        linecolor="#D5E5F0",
        tickfont=dict(size=12, color="#4A6378"),
        title_font=dict(size=13, color="#1E3A5F"),
        automargin=True
    )

    return fig


CHART_CONFIG = {
    "displayModeBar": "hover",
    "responsive": True,
    "displaylogo": False
}


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


# Hero Section
hero_html = (
    '<div class="hero">'
    '<div class="hero-content">'
    '<div class="hero-top">'
    '<div class="hero-tag">'
    '<span class="hero-tag-dot"></span>'
    'WEATHER INTELLIGENCE &middot; DATA ANALYTICS'
    '</div>'
    '</div>'
    '<h1>WeatherProjector</h1>'
    '<p>Discover the patterns behind every season.</p>'
    '<p>Explore historical temperatures, rainfall, humidity and atmospheric behaviour through interactive visual analytics.</p>'
    '</div>'
    f'<div class="hero-icon">{weather_icon("sun", "#FFD166", 68)}</div>'
    '</div>'
)
st.html(hero_html)


# Sidebar Controls
st.sidebar.html(
    '<div style="padding: 4px 0 14px 0; border-bottom: 1px solid #DCEBF5; margin-bottom: 16px;">'
    '<div style="font-size: 0.72rem; font-weight: 700; color: #087EAD; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 4px;">'
    'Filter Parameters'
    '</div>'
    '<h2 style="font-size: 1.35rem; color: #0F2942; margin: 0 0 4px 0;">Dashboard Controls</h2>'
    '<p style="font-size: 0.85rem; color: #5A7184; margin: 0;">Personalise your weather exploration.</p>'
    '</div>'
)

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


# Active Filter Summary Bar
active_start = filtered_df["DATE"].min().strftime("%b %d, %Y")
active_end = filtered_df["DATE"].max().strftime("%b %d, %Y")
st.html(
    f'<div class="filter-bar">'
    f'<div class="filter-bar-left">'
    f'<span>Active Dataset Window:</span>'
    f'<span class="filter-pill">{active_start} &ndash; {active_end}</span>'
    f'<span class="filter-pill filter-pill-orange">{len(selected_conditions)} of {len(conditions)} Conditions</span>'
    f'</div>'
    f'<div class="filter-bar-left">'
    f'<span class="filter-pill">{len(filtered_df):,} Observations</span>'
    f'</div>'
    f'</div>'
)


# 1. Weather Overview KPI Cards
section_heading(
    "Key Metrics",
    "Weather Overview",
    "Summary indicators calculated across the selected date range and atmospheric conditions."
)

metrics = [
    (
        "temperature",
        "Average Temperature",
        f"{filtered_df['temp'].mean():.1f}°",
        "#F27438",
        "#FFF3EC"
    ),
    (
        "humidity",
        "Average Humidity",
        f"{filtered_df['humidity'].mean():.1f}%",
        "#087EAD",
        "#EBF5FB"
    ),
    (
        "rain",
        "Total Rainfall",
        f"{filtered_df['precip'].sum():,.2f}",
        "#189AB4",
        "#E8F7FA"
    ),
    (
        "cloud",
        "Rainfall Days",
        f"{int((filtered_df['precip'] > 0).sum()):,}",
        "#E59838",
        "#FFF6E9"
    )
]

metric_html = '<div class="metric-grid">'

for kind, label, value, color, bg_color in metrics:
    metric_html += (
        f'<div class="custom-metric" style="--card-accent: {color}; --icon-bg: {bg_color};">'
        f'<div class="metric-top">'
        f'<div class="metric-label">{label}</div>'
        f'<div class="metric-icon">{weather_icon(kind, color, 24)}</div>'
        f'</div>'
        f'<div class="metric-value">{value}</div>'
        f'</div>'
    )

metric_html += "</div>"

st.html(metric_html)

st.caption(
    f"Displaying {len(filtered_df):,} records | "
    f"{filtered_df['DATE'].min().date()} to "
    f"{filtered_df['DATE'].max().date()}"
)


# 2. Monthly Weather Analysis
st.divider()
section_heading(
    "Temporal Trends",
    "Monthly Weather Analysis",
    "Aggregated monthly temperature envelopes, precipitation totals, humidity levels and wind patterns."
)

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
        name="Max Temp",
        mode="lines+markers",
        line=dict(color="#F27438", width=3),
        marker=dict(size=5.5),
        hovertemplate="%{y:.1f}°<extra>Max Temp</extra>"
    ))

    fig_temp.add_trace(go.Scatter(
        x=monthly["DATE"],
        y=monthly["temp"],
        name="Avg Temp",
        mode="lines+markers",
        line=dict(color="#087EAD", width=3),
        marker=dict(size=5.5),
        hovertemplate="%{y:.1f}°<extra>Avg Temp</extra>"
    ))

    fig_temp.add_trace(go.Scatter(
        x=monthly["DATE"],
        y=monthly["tempmin"],
        name="Min Temp",
        mode="lines+markers",
        line=dict(color="#38A3D1", width=2.5),
        marker=dict(size=5),
        hovertemplate="%{y:.1f}°<extra>Min Temp</extra>"
    ))

    fig_temp.update_layout(
        title="Monthly Temperature Trends",
        xaxis_title="Month",
        yaxis_title="Temperature (°)",
        hovermode="x unified"
    )

    fig_temp = style_chart(fig_temp, height=470, show_legend=True)

    st.plotly_chart(
        fig_temp,
        width="stretch",
        config=CHART_CONFIG
    )


with tab2:
    fig_rain = px.bar(
        monthly,
        x="DATE",
        y="precip",
        title="Monthly Total Rainfall",
        labels={
            "DATE": "Month",
            "precip": "Rainfall"
        },
        color="precip",
        color_continuous_scale=[
            "#D8F3FC",
            "#38A3D1",
            "#087EAD",
            "#065A82"
        ]
    )

    fig_rain.update_traces(
        hovertemplate="<b>%{x|%b %Y}</b><br>Rainfall: %{y:.2f}<extra></extra>"
    )
    fig_rain.update_layout(coloraxis_showscale=False)
    fig_rain = style_chart(fig_rain, height=440, show_legend=False)

    st.plotly_chart(
        fig_rain,
        width="stretch",
        config=CHART_CONFIG
    )

    fig_rain_daily = px.area(
        filtered_df,
        x="DATE",
        y="precip",
        title="Daily Rainfall Distribution",
        labels={
            "DATE": "Date",
            "precip": "Rainfall"
        }
    )

    fig_rain_daily.update_traces(
        line_color="#087EAD",
        fillcolor="rgba(56, 163, 209, 0.22)",
        hovertemplate="<b>%{x|%b %d, %Y}</b><br>Rainfall: %{y:.2f}<extra></extra>"
    )

    fig_rain_daily = style_chart(fig_rain_daily, height=430, show_legend=False)

    st.plotly_chart(
        fig_rain_daily,
        width="stretch",
        config=CHART_CONFIG
    )


with tab3:
    col_a, col_b = st.columns(2, gap="medium")

    with col_a:
        fig_humidity = px.line(
            monthly,
            x="DATE",
            y="humidity",
            title="Monthly Average Humidity",
            labels={
                "DATE": "Month",
                "humidity": "Humidity (%)"
            },
            markers=True
        )

        fig_humidity.update_traces(
            line_color="#189AB4",
            line_width=3,
            marker_size=6,
            hovertemplate="<b>%{x|%b %Y}</b><br>Humidity: %{y:.1f}%<extra></extra>"
        )

        fig_humidity = style_chart(fig_humidity, height=420, show_legend=False)

        st.plotly_chart(
            fig_humidity,
            width="stretch",
            config=CHART_CONFIG
        )

    with col_b:
        fig_wind = px.bar(
            monthly,
            x="DATE",
            y="windspeed",
            title="Monthly Average Wind Speed",
            labels={
                "DATE": "Month",
                "windspeed": "Wind Speed"
            },
            color="windspeed",
            color_continuous_scale=[
                "#FFE8D6",
                "#FFB45B",
                "#F27438",
                "#C85018"
            ]
        )

        fig_wind.update_traces(
            hovertemplate="<b>%{x|%b %Y}</b><br>Wind Speed: %{y:.1f}<extra></extra>"
        )
        fig_wind.update_layout(coloraxis_showscale=False)
        fig_wind = style_chart(fig_wind, height=420, show_legend=False)

        st.plotly_chart(
            fig_wind,
            width="stretch",
            config=CHART_CONFIG
        )


# 3. Weather Correlation Analysis (Responsive Heatmap)
st.divider()
section_heading(
    "Multivariate Relationships",
    "Weather Correlation Analysis",
    "Pearson correlation coefficients across primary meteorological variables (-1.0 to +1.0)."
)

correlation_columns = [
    "tempmax",
    "tempmin",
    "temp",
    "humidity",
    "precip",
    "windspeed",
    "sealevelpressure"
]

column_labels = {
    "tempmax": "Max Temp",
    "tempmin": "Min Temp",
    "temp": "Avg Temp",
    "humidity": "Humidity",
    "precip": "Rainfall",
    "windspeed": "Wind Speed",
    "sealevelpressure": "Sea Pressure"
}

available_columns = [
    col for col in correlation_columns
    if col in filtered_df.columns
]

correlation = filtered_df[available_columns].corr()
readable_labels = [column_labels.get(col, col) for col in available_columns]
correlation_display = correlation.copy()
correlation_display.index = readable_labels
correlation_display.columns = readable_labels

show_corr_values = st.toggle(
    "Show correlation values on cells (automatically hidden on narrow mobile screens)",
    value=True
)

fig_corr = px.imshow(
    correlation_display,
    text_auto=False,
    color_continuous_scale=[
        "#065A82",
        "#38A3D1",
        "#F8FBFE",
        "#FFB45B",
        "#F27438",
        "#B83B2A"
    ],
    zmin=-1,
    zmax=1,
    aspect="auto",
    title="Relationship Between Weather Variables"
)

fig_corr.update_traces(
    hovertemplate="<b>%{y} &times; %{x}</b><br>Correlation: <b>%{z:.2f}</b><extra></extra>",
    xgap=2,
    ygap=2
)

fig_corr = style_chart(fig_corr, height=540, show_legend=False)

if show_corr_values:
    corr_annotations = []
    for y_idx, y_label in enumerate(readable_labels):
        for x_idx, x_label in enumerate(readable_labels):
            val = correlation_display.iloc[y_idx, x_idx]
            text_color = "#FFFFFF" if abs(val) >= 0.55 else "#0F2942"
            corr_annotations.append(
                dict(
                    x=x_label,
                    y=y_label,
                    text=f"{val:.2f}",
                    showarrow=False,
                    font=dict(
                        family="DM Sans, sans-serif",
                        size=12,
                        color=text_color
                    )
                )
            )
    fig_corr.update_layout(annotations=corr_annotations)

fig_corr.update_layout(
    margin=dict(l=40, r=20, t=64, b=95),
    coloraxis_colorbar=dict(
        title=dict(text="Correlation (r)", side="top", font=dict(size=12, color="#1E3A5F")),
        orientation="h",
        yanchor="top",
        y=-0.22,
        xanchor="center",
        x=0.5,
        len=0.78,
        thickness=12,
        tickvals=[-1.0, -0.5, 0.0, 0.5, 1.0],
        tickfont=dict(size=11, color="#4A6378")
    )
)

fig_corr.update_xaxes(
    tickangle=-35,
    side="bottom",
    showgrid=False,
    automargin=True
)

fig_corr.update_yaxes(
    showgrid=False,
    automargin=True
)

with st.container(key="corr_chart_box"):
    st.plotly_chart(
        fig_corr,
        width="stretch",
        config=CHART_CONFIG
    )


# 4. Extreme Weather Records
st.divider()
section_heading(
    "Historical Peaks",
    "Extreme Weather Records",
    "Top 5 most extreme daily observations recorded within the filtered period."
)

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
        width="stretch",
        hide_index=True,
        height=240
    )

with extreme_tab2:
    st.dataframe(
        filtered_df.nsmallest(5, "tempmin")[
            ["DATE", "tempmax", "tempmin", "humidity"]
        ],
        width="stretch",
        hide_index=True,
        height=240
    )

with extreme_tab3:
    st.dataframe(
        filtered_df.nlargest(5, "precip")[
            ["DATE", "precip", "humidity", "conditions"]
        ],
        width="stretch",
        hide_index=True,
        height=240
    )


# 5. Dataset Explorer & Export
st.divider()
section_heading(
    "Raw Data & Export",
    "Dataset Explorer",
    "Inspect individual daily weather records or export the filtered dataset as CSV."
)

with st.expander("Explore all weather records"):
    st.dataframe(
        filtered_df,
        width="stretch",
        hide_index=True,
        height=480
    )

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Dataset (CSV)",
    data=csv_data,
    file_name="WeatherProjector_Filtered_Data.csv",
    mime="text/csv"
)


# Footer
st.divider()

st.html(
    '<div class="footer">'
    '<h3>WeatherProjector</h3>'
    '<p>Turning historical weather data into meaningful insights.</p>'
    '<div class="footer-badges">'
    '<span class="footer-badge">Python</span>'
    '<span class="footer-badge">Pandas</span>'
    '<span class="footer-badge">Plotly</span>'
    '<span class="footer-badge">Streamlit</span>'
    '</div>'
    '</div>'
)
