import streamlit as st

st.set_page_config(
    page_title="CinePredict — Box Office Engine",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global Netflix CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Reset & Base ── */
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}
.stApp {
    background-color: #080808;
    color: #F5F5F5;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #0a0a0a !important;
    border-right: 1px solid #1a1a1a;
}
[data-testid="stSidebar"] > div {
    padding-top: 0 !important;
}

/* ── Main content padding ── */
.main .block-container {
    padding-top: 28px;
    padding-bottom: 40px;
    max-width: 1200px;
}

/* ── Buttons ── */
.stButton > button {
    background: #E50914 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 4px !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    padding: 12px 24px !important;
    letter-spacing: 0.5px;
    transition: background 0.2s ease, transform 0.1s ease;
}
.stButton > button:hover {
    background: #FF1A1A !important;
    transform: translateY(-1px);
}
.stButton > button:active {
    transform: translateY(0);
}

/* ── Inputs & Sliders ── */
.stTextArea textarea, .stTextInput input, .stNumberInput input {
    background: #1a1a1a !important;
    color: #F5F5F5 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 6px !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #E50914 !important;
    box-shadow: 0 0 0 1px #E50914 !important;
}
.stSelectbox > div > div {
    background: #1a1a1a !important;
    border: 1px solid #2a2a2a !important;
    color: #F5F5F5 !important;
}
[data-testid="stSlider"] .stSlider > div > div > div {
    background: #E50914;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: #141414;
    border-radius: 8px;
    padding: 14px 16px;
    border: 1px solid #2a2a2a;
}
[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-weight: 700;
}
[data-testid="stMetricLabel"] {
    color: #888888 !important;
}

/* ── Headings ── */
h1, h2, h3, h4 { color: #FFFFFF !important; }

/* ── Plotly chart backgrounds ── */
.js-plotly-plot .plotly .modebar {
    background: transparent !important;
}

/* ── Alerts / info boxes ── */
.stAlert {
    background: #1a1a1a !important;
    color: #F5F5F5 !important;
    border-radius: 8px;
}

/* ── Radio buttons ── */
[data-testid="stRadio"] label {
    color: #CCCCCC !important;
    font-size: 15px;
    padding: 4px 0;
}
[data-testid="stRadio"] label:hover {
    color: #FFFFFF !important;
}

/* ── Dividers ── */
hr { border-color: #1a1a1a !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0a0a; }
::-webkit-scrollbar-thumb { background: #3a0000; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #E50914; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="background:linear-gradient(180deg,#1a0000 0%,#0a0a0a 100%);
                padding:28px 20px 20px;border-bottom:1px solid #1a1a1a;margin-bottom:8px">
      <div style="color:#E50914;font-size:26px;font-weight:900;letter-spacing:2px">
        CINEPREDICT
      </div>
      <div style="color:#555;font-size:12px;letter-spacing:2px;text-transform:uppercase;margin-top:2px">
        Box Office Engine
      </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["Home", "EDA Dashboard", "Predict Revenue", "Sentiment Analyser", "Model Metrics"],
        label_visibility="collapsed",
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="padding:0 4px">
      <div style="color:#444;font-size:11px;text-transform:uppercase;letter-spacing:2px;margin-bottom:10px">Pipeline</div>
      <div style="color:#666;font-size:13px;line-height:2">
        M1 · Preprocessing<br>
        M2 · EDA & Charts<br>
        M3 · Feature Eng.<br>
        M4 · Model Training<br>
        M5 · Sentiment NLP<br>
        M6 · Streamlit UI
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="position:fixed;bottom:20px;left:0;width:220px;padding:0 16px;
                color:#333;font-size:11px;text-align:center">
      ML Lab Project · Team 6
    </div>
    """, unsafe_allow_html=True)

# ── Page routing ─────────────────────────────────────────────────────────────
if page == "Home":
    from pages.home import show_home
    show_home()

elif page == "EDA Dashboard":
    from pages.eda_page import show_eda
    show_eda()

elif page == "Predict Revenue":
    from pages.predict import show_predict
    show_predict()

elif page == "Sentiment Analyser":
    from pages.sentiment_page import show_sentiment
    show_sentiment()

elif page == "Model Metrics":
    from pages.metrics_page import show_metrics
    show_metrics()