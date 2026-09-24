"""JanMitra — AI-Powered Government Scheme Assistant
Entry point. Run: streamlit run app.py
"""
import streamlit as st
import joblib
import pandas as pd
import os

st.set_page_config(
    page_title="JanMitra — Scheme Assistant",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Premium CSS — Streamlit 1.59 compatible ───────────────────────────────────
st.markdown("""
<style>
/* ─────────────────────────────────────────────
   RESET & FONT
───────────────────────────────────────────── */
html, body, [class*="st-"], [class*="css"] {
    font-family: -apple-system, "Segoe UI", system-ui, sans-serif !important;
}

/* ─────────────────────────────────────────────
   PAGE BACKGROUND
───────────────────────────────────────────── */
.stApp {
    background-color: #f5f5f7 !important;
}
.main .block-container {
    max-width: 1080px !important;
    padding: 1.5rem 2rem 4rem 2rem !important;
    margin: 0 auto !important;
}

/* ─────────────────────────────────────────────
   HIDE STREAMLIT CHROME
───────────────────────────────────────────── */
#MainMenu { visibility: hidden !important; }
footer    { visibility: hidden !important; }
header    { visibility: hidden !important; }
.stDeployButton { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }

/* ─────────────────────────────────────────────
   TOP NAVIGATION BAR
───────────────────────────────────────────── */
[data-testid="stNavbar"],
nav[class*="Nav"] {
    background: #ffffff !important;
    border-bottom: 1px solid #e5e5ea !important;
    padding: 0 24px !important;
}
[data-testid="stNavbar"] a,
[data-testid="stNavbar"] button {
    color: #1d1d1f !important;
    font-weight: 500 !important;
    font-size: 14px !important;
}
[data-testid="stNavbar"] a[aria-current="page"],
[data-testid="stNavbar"] button[aria-current="page"] {
    color: #0071e3 !important;
    font-weight: 700 !important;
}

/* ─────────────────────────────────────────────
   CARDS (stContainer with border)
───────────────────────────────────────────── */
div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #ffffff !important;
    border-radius: 16px !important;
    border: 1px solid #e5e5ea !important;
    padding: 20px !important;
    box-shadow: 0 1px 8px rgba(0,0,0,0.07) !important;
}

/* ─────────────────────────────────────────────
   BUTTONS
───────────────────────────────────────────── */
/* Primary */
div[data-testid="stFormSubmitButton"] > button,
button[kind="primaryFormSubmit"],
.stButton > button[kind="primary"] {
    background: #0071e3 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 10px 28px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: -0.01em !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: background 0.15s !important;
}
div[data-testid="stFormSubmitButton"] > button:hover,
.stButton > button[kind="primary"]:hover {
    background: #0064cc !important;
}
/* Secondary */
.stButton > button[kind="secondary"] {
    background: #ffffff !important;
    color: #0071e3 !important;
    border: 1.5px solid #0071e3 !important;
    border-radius: 12px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}
/* Link button */
.stLinkButton a {
    background: #0071e3 !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    padding: 8px 20px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    text-decoration: none !important;
    display: inline-block !important;
}
.stLinkButton a:hover {
    background: #0064cc !important;
}

/* ─────────────────────────────────────────────
   INPUTS & SELECTS
───────────────────────────────────────────── */
.stTextInput input,
.stNumberInput input {
    background: #ffffff !important;
    color: #1d1d1f !important;
    border: 1.5px solid #d2d2d7 !important;
    border-radius: 10px !important;
    font-size: 15px !important;
    padding: 10px 14px !important;
}
.stTextInput input:focus,
.stNumberInput input:focus {
    border-color: #0071e3 !important;
    box-shadow: 0 0 0 3px rgba(0,113,227,0.15) !important;
    outline: none !important;
}
/* Selectbox */
div[data-baseweb="select"] > div {
    background: #ffffff !important;
    color: #1d1d1f !important;
    border: 1.5px solid #d2d2d7 !important;
    border-radius: 10px !important;
    font-size: 14px !important;
}
div[data-baseweb="select"] > div:focus-within {
    border-color: #0071e3 !important;
}
/* Selectbox dropdown */
div[data-baseweb="popover"] {
    background: #ffffff !important;
    border-radius: 12px !important;
    border: 1px solid #e5e5ea !important;
    box-shadow: 0 8px 30px rgba(0,0,0,0.12) !important;
}
div[data-baseweb="menu"] li {
    color: #1d1d1f !important;
    font-size: 14px !important;
}
div[data-baseweb="menu"] li:hover {
    background: #f0f7ff !important;
}

/* Slider */
div[data-baseweb="slider"] [role="slider"] {
    background: #0071e3 !important;
    border: 2px solid #0071e3 !important;
}
div[data-baseweb="slider"] [data-testid="stSliderTrackFill"] {
    background: #0071e3 !important;
}
.stSlider > div > div > div > div {
    background: #0071e3 !important;
}

/* Checkbox */
label[data-baseweb="checkbox"] span {
    background: #ffffff !important;
    border: 1.5px solid #d2d2d7 !important;
    border-radius: 5px !important;
}
label[data-baseweb="checkbox"] input:checked + span {
    background: #0071e3 !important;
    border-color: #0071e3 !important;
}

/* ─────────────────────────────────────────────
   METRICS
───────────────────────────────────────────── */
div[data-testid="stMetric"] {
    background: #f0f7ff !important;
    border: 1px solid #d0e5ff !important;
    border-radius: 12px !important;
    padding: 14px 16px !important;
}
div[data-testid="stMetricValue"] {
    color: #0071e3 !important;
    font-weight: 700 !important;
    font-size: 20px !important;
}
div[data-testid="stMetricLabel"] {
    color: #6e6e73 !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

/* ─────────────────────────────────────────────
   PROGRESS BAR
───────────────────────────────────────────── */
.stProgress > div > div {
    background: #e5e5ea !important;
    border-radius: 6px !important;
    height: 6px !important;
}
.stProgress > div > div > div {
    background: linear-gradient(90deg, #0071e3, #34aadc) !important;
    border-radius: 6px !important;
}

/* ─────────────────────────────────────────────
   TABS
───────────────────────────────────────────── */
div[data-testid="stTabs"] [role="tablist"] {
    background: #e5e5ea !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 2px !important;
    border-bottom: none !important;
}
div[data-testid="stTabs"] [role="tab"] {
    background: transparent !important;
    color: #6e6e73 !important;
    border-radius: 9px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    padding: 8px 18px !important;
    border: none !important;
}
div[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: #ffffff !important;
    color: #0071e3 !important;
    font-weight: 700 !important;
    box-shadow: 0 1px 6px rgba(0,0,0,0.10) !important;
}

/* ─────────────────────────────────────────────
   EXPANDER
───────────────────────────────────────────── */
details[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid #e5e5ea !important;
    border-radius: 12px !important;
    padding: 0 16px !important;
}
details[data-testid="stExpander"] summary {
    color: #1d1d1f !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 12px 0 !important;
}

/* ─────────────────────────────────────────────
   ALERTS (success / info / warning)
───────────────────────────────────────────── */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
    font-size: 14px !important;
}
div[data-testid="stAlert"][data-baseweb="notification"][kind="success"] {
    background: #f0fdf4 !important;
    border-left: 4px solid #34c759 !important;
    color: #166534 !important;
}
div[data-testid="stAlert"][data-baseweb="notification"][kind="info"] {
    background: #eff6ff !important;
    border-left: 4px solid #0071e3 !important;
    color: #1e40af !important;
}
div[data-testid="stAlert"][data-baseweb="notification"][kind="warning"] {
    background: #fffbeb !important;
    border-left: 4px solid #ff9f0a !important;
    color: #92400e !important;
}

/* ─────────────────────────────────────────────
   FORM
───────────────────────────────────────────── */
div[data-testid="stForm"] {
    background: #ffffff !important;
    border-radius: 20px !important;
    border: 1px solid #e5e5ea !important;
    padding: 28px !important;
    box-shadow: 0 2px 16px rgba(0,0,0,0.05) !important;
}

/* ─────────────────────────────────────────────
   TYPOGRAPHY
───────────────────────────────────────────── */
h1, .stMarkdown h1 {
    color: #1d1d1f !important;
    font-weight: 700 !important;
    letter-spacing: -0.03em !important;
    line-height: 1.15 !important;
}
h2, .stMarkdown h2 {
    color: #1d1d1f !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em !important;
}
h3, .stMarkdown h3 {
    color: #1d1d1f !important;
    font-weight: 600 !important;
}
p, .stMarkdown p, li {
    color: #1d1d1f !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
}
.stCaption p {
    color: #6e6e73 !important;
    font-size: 12px !important;
}
strong {
    color: #1d1d1f !important;
}

/* ─────────────────────────────────────────────
   CHART BACKGROUND
───────────────────────────────────────────── */
.stVegaLiteChart, .element-container canvas {
    background: #ffffff !important;
    border-radius: 12px !important;
}

/* ─────────────────────────────────────────────
   LABEL TEXT above inputs
───────────────────────────────────────────── */
label[data-testid="stWidgetLabel"] p,
.stSlider label p,
.stNumberInput label p,
.stSelectbox label p,
.stCheckbox label p,
.stTextInput label p {
    color: #1d1d1f !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    margin-bottom: 4px !important;
}

/* ─────────────────────────────────────────────
   HR divider
───────────────────────────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid #e5e5ea !important;
    margin: 20px 0 !important;
}
</style>
""", unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@st.cache_resource(show_spinner="Loading AI models…")
def load_recommender():
    path = os.path.join(BASE_DIR, "models", "scheme_recommender.pkl")
    return joblib.load(path) if os.path.exists(path) else None


@st.cache_resource(show_spinner=False)
def load_intent_model():
    path = os.path.join(BASE_DIR, "models", "intent_classifier.pkl")
    return joblib.load(path) if os.path.exists(path) else None


@st.cache_data(show_spinner=False)
def load_schemes_df():
    for name in ("schemes_master.csv", "schemes_processed.csv",
                 "indian_government_schemes.csv"):
        for sub in ("data/processed", "data/raw/schemes"):
            p = os.path.join(BASE_DIR, sub, name)
            if os.path.exists(p):
                return pd.read_csv(p, on_bad_lines="skip")
    return pd.DataFrame()


# ── Session state ──────────────────────────────────────────────────────────────
for key, default in [("profile", {}), ("results", []), ("score", 0), ("submitted", False)]:
    if key not in st.session_state:
        st.session_state[key] = default

st.session_state["_recommender"]  = load_recommender()
st.session_state["_intent_model"] = load_intent_model()
st.session_state["_schemes_df"]   = load_schemes_df()

# ── Navigation ─────────────────────────────────────────────────────────────────
page = st.navigation(
    [
        st.Page("app_pages/citizen_input.py",
                title="My Profile",
                icon=":material/person:"),
        st.Page("app_pages/eligible_schemes.py",
                title="Eligible Schemes",
                icon=":material/verified:"),
        st.Page("app_pages/ask_language.py",
                title="Ask JanMitra",
                icon=":material/translate:"),
    ],
    position="top",
)
page.run()

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:28px 0 8px;
            color:#6e6e73;font-size:12px;
            border-top:1px solid #e5e5ea;margin-top:32px">
  Built by <strong style="color:#1d1d1f">VeereshMath</strong>
  &nbsp;·&nbsp; AICTE &nbsp;·&nbsp; IBM SkillsBuild
  &nbsp;·&nbsp; BharatCares &nbsp;·&nbsp; 2026
</div>
""", unsafe_allow_html=True)
