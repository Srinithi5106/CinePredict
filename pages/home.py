import streamlit as st

def show_home():
    st.markdown("""
    <style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css');

    .hero {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a0000 60%, #0a0a0a 100%);
        border-radius: 16px;
        padding: 64px 52px;
        margin-bottom: 36px;
        border: 1px solid #1a1a1a;
    }
    .hero-title {
        color: #FFFFFF;
        font-size: 64px;
        font-weight: 900;
        letter-spacing: 3px;
        margin: 0;
        line-height: 1;
    }
    .hero-title span { color: #E50914; }
    .hero-tagline {
        color: #AAAAAA;
        font-size: 17px;
        margin: 18px 0 0;
        max-width: 560px;
        line-height: 1.7;
    }
    .stat-strip {
        background: #111111;
        border: 1px solid #1e1e1e;
        border-radius: 12px;
        padding: 22px 16px;
        text-align: center;
        border-bottom: 3px solid #E50914;
    }
    .stat-num   { color: #FFFFFF; font-size: 34px; font-weight: 900; line-height: 1; }
    .stat-label { color: #666; font-size: 11px; letter-spacing: 2px;
                  text-transform: uppercase; margin-top: 6px; }
    .feature-card {
        background: #111111;
        border: 1px solid #1e1e1e;
        border-radius: 12px;
        padding: 28px 22px;
        margin-bottom: 16px;
    }
    .feature-icon  { color: #E50914; font-size: 26px; margin-bottom: 12px; }
    .feature-title { color: #FFFFFF; font-size: 16px; font-weight: 700; margin-bottom: 8px; }
    .feature-desc  { color: #777; font-size: 14px; line-height: 1.7; }
    .tier-card {
        background: #111;
        border: 1px solid #1e1e1e;
        border-radius: 10px;
        padding: 18px 12px;
        text-align: center;
    }
    .novelty-block {
        background: #0e0000;
        border: 1px solid #E50914;
        border-radius: 14px;
        padding: 32px 36px;
    }
    .section-title {
        color: #FFFFFF;
        font-size: 20px;
        font-weight: 800;
        margin: 28px 0 16px;
        padding-bottom: 10px;
        border-bottom: 1px solid #1a1a1a;
    }
    .section-title span { color: #E50914; }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    """, unsafe_allow_html=True)

    # ── Hero ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero">
      <div class="hero-title">CINE<span>PREDICT</span></div>
      <div class="hero-tagline">
        Forecast box office revenue, classify hits and flops, and estimate
        production budgets for any movie — powered by machine learning and
        real-time sentiment analysis.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Stats ─────────────────────────────────────────────────────────────
    for col, (val, label) in zip(st.columns(5), [
        ("3,800+", "Movies Trained On"),
        ("11",     "ML Features"),
        ("3",      "Models Compared"),
        ("5",      "App Pages"),
        ("2-Layer","Sentiment NLP"),
    ]):
        col.markdown(f"""
        <div class="stat-strip">
          <div class="stat-num">{val}</div>
          <div class="stat-label">{label}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Features ──────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">App <span>Features</span></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    features_left = [
        ("fa-solid fa-chart-line", "Revenue Prediction",
         "Enter budget, genre, runtime, cast size and release month — get an instant box office revenue forecast built on XGBoost trained across 3,800 real movies."),
        ("fa-solid fa-tag", "Hit / Flop Classification",
         "Every prediction is automatically classified — Blockbuster, Hit, Average, Below Average, or Flop — with a verdict on commercial viability."),
    ]
    features_mid = [
        ("fa-solid fa-coins", "Budget Estimator & ROI",
         "Enter your planned budget and get a recommended production spend, estimated net profit, and ROI % using the industry 2.5× break-even rule."),
        ("fa-solid fa-brain", "Sentiment-Fused Prediction",
         "Paste any review or synopsis — the two-layer NLP engine scores tone and adjusts the revenue forecast. Positive buzz boosts it; negative reviews lower it."),
    ]
    features_right = [
        ("fa-solid fa-chart-bar", "EDA Dashboard",
         "Seven interactive dark-themed charts — revenue distribution, correlation heatmap, genre breakdown, seasonal trends, budget vs revenue, top 20 films, and decade analysis."),
        ("fa-solid fa-sliders", "Model Metrics",
         "Compare R² scores across all three models, view actual vs predicted scatter, and inspect feature importance rankings to understand every prediction."),
    ]

    for col, features in zip([c1, c2, c3], [features_left, features_mid, features_right]):
        for icon, title, desc in features:
            col.markdown(f"""
            <div class="feature-card">
              <div class="feature-icon"><i class="{icon}"></i></div>
              <div class="feature-title">{title}</div>
              <div class="feature-desc">{desc}</div>
            </div>""", unsafe_allow_html=True)

    # ── Classification tiers ──────────────────────────────────────────────
    st.markdown('<div class="section-title">Classification <span>Tiers</span></div>', unsafe_allow_html=True)

    tiers = [
        ("fa-solid fa-trophy",        "BLOCKBUSTER", "$500M+",        "#FFD700", "Franchise-level. Top 1%."),
        ("fa-solid fa-circle-check",  "HIT",          "$150M–$500M",  "#4CAF50", "Strong commercial success."),
        ("fa-solid fa-minus",         "AVERAGE",      "$50M–$150M",   "#FFC107", "Moderate. Breaks even."),
        ("fa-solid fa-circle-minus",  "BELOW AVG",    "$10M–$50M",    "#FF9800", "Below expectations."),
        ("fa-solid fa-circle-xmark",  "FLOP",         "Under $10M",   "#F44336", "Poor outlook."),
    ]
    for col, (icon, name, rng, color, desc) in zip(st.columns(5), tiers):
        col.markdown(f"""
        <div class="tier-card" style="border-top:3px solid {color}">
          <div style="color:{color};font-size:22px;margin-bottom:8px"><i class="{icon}"></i></div>
          <div style="color:{color};font-size:13px;font-weight:800">{name}</div>
          <div style="color:#fff;font-size:15px;font-weight:900;margin:4px 0">{rng}</div>
          <div style="color:#555;font-size:12px">{desc}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Novelty block ─────────────────────────────────────────────────────
    st.markdown("""
    <div class="novelty-block">
      <div style="color:#E50914;font-size:11px;letter-spacing:4px;
                  text-transform:uppercase;font-weight:700;margin-bottom:10px">
        <i class="fa-solid fa-star"></i> &nbsp; What Makes This Different
      </div>
      <div style="color:#FFFFFF;font-size:20px;font-weight:800;margin-bottom:12px">
        Sentiment-Fused Revenue Prediction
      </div>
      <div style="color:#999;font-size:14px;line-height:1.8;max-width:800px">
        Most box office models rely only on structured data — budget, genre, cast.
        CinePredict adds a <strong style="color:#fff">two-layer NLP pipeline</strong>:
        TextBlob scores the overall polarity of any review or synopsis, while a
        40-word keyword detector catches hype signals like <em>"masterpiece"</em> or
        <em>"flop"</em>. Both layers multiply the ML base prediction — mimicking
        how real audience buzz drives opening weekend numbers.
      </div>
      <div style="margin-top:18px">
        <span style="background:#1a0000;border:1px solid #E50914;color:#E50914;
                     padding:5px 14px;border-radius:4px;font-size:12px;
                     font-weight:700;margin-right:8px">
          <i class="fa-solid fa-comments"></i> &nbsp; TextBlob Polarity
        </span>
        <span style="background:#1a0000;border:1px solid #E50914;color:#E50914;
                     padding:5px 14px;border-radius:4px;font-size:12px;
                     font-weight:700;margin-right:8px">
          <i class="fa-solid fa-magnifying-glass"></i> &nbsp; Keyword Hype Detector
        </span>
        <span style="background:#1a0000;border:1px solid #E50914;color:#E50914;
                     padding:5px 14px;border-radius:4px;font-size:12px;font-weight:700">
          <i class="fa-solid fa-arrow-trend-up"></i> &nbsp; Revenue Multiplier Fusion
        </span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CTA ───────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:#111;border:1px solid #1e1e1e;border-radius:12px;
                padding:28px 32px;text-align:center">
      <div style="color:#fff;font-size:18px;font-weight:700;margin-bottom:6px">
        <i class="fa-solid fa-film" style="color:#E50914"></i> &nbsp; Ready to predict?
      </div>
      <div style="color:#666;font-size:14px">
        Go to <strong style="color:#E50914">Predict Revenue</strong> in the sidebar,
        enter your movie parameters, and get an instant forecast.
      </div>
    </div>
    """, unsafe_allow_html=True)