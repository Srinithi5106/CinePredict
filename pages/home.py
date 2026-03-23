import streamlit as st

def show_home():
    st.markdown("""
    <style>
    .hero-banner {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a0000 50%, #0a0a0a 100%);
        border-left: 5px solid #E50914;
        border-radius: 12px;
        padding: 56px 48px;
        margin-bottom: 32px;
    }
    .hero-title { color: #FFFFFF; font-size: 62px; font-weight: 900;
                  letter-spacing: 2px; margin: 0; line-height: 1; }
    .hero-sub   { color: #E50914; font-size: 20px; font-weight: 700;
                  margin: 10px 0 16px; letter-spacing: 3px; text-transform: uppercase; }
    .hero-desc  { color: #AAAAAA; font-size: 17px; max-width: 620px; line-height: 1.6; }
    .member-card {
        background: #1a1a1a;
        border-top: 3px solid #E50914;
        border-radius: 10px;
        padding: 20px 16px;
        text-align: center;
    }
    .member-tag  { color: #E50914; font-size: 22px; font-weight: 900; }
    .member-role { color: #AAAAAA; font-size: 13px; margin-top: 4px; }
    .step-card {
        background: #141414;
        border: 1px solid #2a2a2a;
        border-radius: 10px;
        padding: 24px 20px;
    }
    .step-num   { color: #E50914; font-size: 36px; font-weight: 900; line-height: 1; }
    .step-title { color: #FFFFFF; font-size: 16px; font-weight: 700; margin: 6px 0 4px; }
    .step-desc  { color: #888888; font-size: 14px; line-height: 1.5; }
    .stat-card  {
        background: #1a1a1a;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        border-bottom: 3px solid #E50914;
    }
    .stat-val   { color: #FFFFFF; font-size: 32px; font-weight: 900; }
    .stat-label { color: #888888; font-size: 13px; margin-top: 4px; }
    </style>
    """, unsafe_allow_html=True)

    # Hero
    st.markdown("""
    <div class="hero-banner">
      <div class="hero-title">CINEPREDICT</div>
      <div class="hero-sub">Box Office Prediction Engine</div>
      <div class="hero-desc">
        ML-powered app predicting movie box office revenue using production budget,
        genre metadata, cast, release timing — fused with real-time NLP sentiment analysis.
        Built with XGBoost + TextBlob on the TMDB 5000 dataset.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats row
    c1, c2, c3, c4 = st.columns(4)
    stats = [("~3,800", "Movies in Dataset"), ("11", "ML Features"),
             ("3", "Models Trained"), ("2-Layer", "Sentiment NLP")]
    for col, (val, label) in zip([c1, c2, c3, c4], stats):
        col.markdown(f"""
        <div class="stat-card">
          <div class="stat-val">{val}</div>
          <div class="stat-label">{label}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Team members
    st.markdown("### Team Structure")
    team = [
        ("M1", "Data & Preprocessing", "data/preprocess.py"),
        ("M2", "EDA & Visualization",  "utils/eda.py"),
        ("M3", "Feature Engineering",  "utils/features.py"),
        ("M4", "Model Building",       "utils/model.py"),
        ("M5", "Sentiment NLP",        "utils/sentiment.py"),
        ("M6", "Streamlit UI",         "app.py + pages/"),
    ]
    cols = st.columns(6)
    for col, (tag, role, file) in zip(cols, team):
        col.markdown(f"""
        <div class="member-card">
          <div class="member-tag">{tag}</div>
          <div class="member-role">{role}</div>
          <div style="color:#555;font-size:11px;margin-top:8px">{file}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # How it works
    st.markdown("### How It Works")
    steps = [
        ("01", "Data Preprocessing",  "Merge TMDB CSVs, clean nulls, parse JSON columns, extract date features, save cleaned_movies.csv"),
        ("02", "EDA",                 "Visualise revenue distribution, correlations, genre trends, seasonality — all dark-themed Plotly charts"),
        ("03", "Feature Engineering", "Log transforms on skewed numerics, label-encode language, add genre/keyword/cast count features"),
        ("04", "Model Training",      "Train Linear Regression, Random Forest, XGBoost. Auto-select best by R². Save best_model.pkl"),
        ("05", "Sentiment Fusion",    "TextBlob polarity scoring + keyword hype detection. Adjust base ML prediction with a revenue multiplier"),
        ("06", "Streamlit App",       "Netflix-dark UI with 5 pages: Home, EDA, Predict, Sentiment Analyser, Model Metrics"),
    ]
    c1, c2 = st.columns(2)
    for i, (num, title, desc) in enumerate(steps):
        col = c1 if i % 2 == 0 else c2
        col.markdown(f"""
        <div class="step-card" style="margin-bottom:16px">
          <div class="step-num">{num}</div>
          <div class="step-title">{title}</div>
          <div class="step-desc">{desc}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Novelty callout
    st.markdown("""
    <div style="background:#1a0000;border:1px solid #E50914;border-radius:12px;padding:28px 32px;">
      <div style="color:#E50914;font-size:13px;font-weight:700;letter-spacing:3px;
                  text-transform:uppercase;margin-bottom:8px">
        Project Novelty
      </div>
      <div style="color:#FFFFFF;font-size:20px;font-weight:700;margin-bottom:10px">
        Sentiment-Fused Revenue Prediction
      </div>
      <div style="color:#AAAAAA;font-size:15px;line-height:1.7">
        Standard ML projects predict revenue from structured metadata alone.
        CinePredict adds a <strong style="color:#fff">two-layer NLP pipeline</strong>:
        Layer 1 uses TextBlob polarity scoring to detect overall review sentiment.
        Layer 2 runs a keyword hype detector scanning for power words like
        <em>"masterpiece"</em> or <em>"flop"</em>. Both multipliers are applied
        on top of the XGBoost base prediction — mimicking how real-world
        audience buzz directly affects box office performance.
      </div>
    </div>
    """, unsafe_allow_html=True)