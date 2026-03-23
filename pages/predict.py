import streamlit as st
import numpy as np
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@st.cache_resource(show_spinner="Loading model...")
def _get_model():
    from utils.model import load_model
    return load_model()

def classify_movie(revenue_m):
    """Classify movie based on predicted revenue in millions."""
    if revenue_m >= 500:
        return "BLOCKBUSTER", "#FFD700", "Franchise-level box office. Top 1% of all releases."
    elif revenue_m >= 150:
        return "HIT", "#4CAF50", "Strong commercial success. Likely profitable with wide release."
    elif revenue_m >= 50:
        return "AVERAGE", "#FFC107", "Moderate performer. Breaks even or modest profit."
    elif revenue_m >= 10:
        return "BELOW AVERAGE", "#FF9800", "Below expectations. Limited theatrical window likely."
    else:
        return "FLOP", "#F44336", "Poor box office outlook. VOD/streaming release recommended."

def estimate_budget(revenue_m, genre_count, runtime, popularity):
    """
    Estimate a recommended production budget based on projected revenue.
    Uses industry rule-of-thumb: P&A (prints & advertising) is ~50% of production budget,
    and a film needs ~2.5x production budget in revenue to break even.
    """
    # Break-even back-calculation: revenue / 2.5 = production budget
    raw_budget = revenue_m / 2.5

    # Genre complexity modifier
    genre_mod = 1.0 + (genre_count - 1) * 0.05  # more genres = slightly higher budget

    # Runtime modifier (longer = more expensive)
    runtime_mod = 1.0 + max(0, (runtime - 100) / 200)

    # Popularity/marketing scale modifier
    pop_mod = 1.0 + min(popularity / 500, 0.3)

    est = raw_budget * genre_mod * runtime_mod * pop_mod
    est = max(1.0, min(est, 400.0))  # clamp between $1M and $400M
    return round(est, 1)

def roi_estimate(predicted_rev_m, budget_m):
    """Estimate ROI % — accounts for P&A spend (50% of production budget)."""
    total_cost = budget_m * 1.5   # production + P&A
    profit     = predicted_rev_m - total_cost
    roi        = (profit / total_cost) * 100
    return round(roi, 1)

def show_predict():
    st.markdown("""
    <style>
    .result-card {
        background: #1a1a1a;
        border: 2px solid #E50914;
        border-radius: 14px;
        padding: 40px 36px;
        text-align: center;
        box-shadow: 0 0 50px rgba(229,9,20,0.18);
        margin: 20px 0;
    }
    .result-label {
        color: #E50914;
        font-size: 11px;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .result-value {
        color: #FFFFFF;
        font-size: 76px;
        font-weight: 900;
        margin: 0;
        line-height: 1;
    }
    .result-sub {
        color: #666;
        font-size: 14px;
        margin-top: 8px;
    }
    .classification-badge {
        display: inline-block;
        padding: 10px 28px;
        border-radius: 6px;
        font-size: 22px;
        font-weight: 900;
        letter-spacing: 3px;
        margin: 16px 0 6px;
    }
    .budget-card {
        background: #141414;
        border: 1px solid #2a2a2a;
        border-radius: 10px;
        padding: 24px;
        text-align: center;
    }
    .budget-label { color: #888; font-size: 12px; letter-spacing: 2px; text-transform: uppercase; }
    .budget-value { color: #FFFFFF; font-size: 32px; font-weight: 900; margin: 6px 0; }
    .budget-sub   { color: #555; font-size: 13px; }
    .section-head {
        color: #E50914;
        font-size: 11px;
        letter-spacing: 3px;
        text-transform: uppercase;
        font-weight: 700;
        margin-bottom: 14px;
        padding-bottom: 6px;
        border-bottom: 1px solid #1a1a1a;
    }
    .future-badge {
        background: #1a0a00;
        border: 1px solid #E50914;
        border-radius: 8px;
        padding: 12px 20px;
        color: #FFA500;
        font-size: 13px;
        margin-bottom: 24px;
        display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="border-left:4px solid #E50914;padding:4px 20px;margin-bottom:16px">
      <h1 style="color:#fff;margin:0">Future Movie Predictor</h1>
      <p style="color:#888;margin:4px 0 0">
        Predict box office revenue, recommended budget &amp; classification for any unreleased movie
      </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="future-badge">
      This predictor works for future/unreleased movies — no TMDB data needed.
      Enter any hypothetical movie parameters and get an instant forecast.
    </div>
    """, unsafe_allow_html=True)

    # ── Input form ──────────────────────────────────────────────────────────
    st.markdown('<div class="section-head">Movie Parameters</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("**Production**")
        budget_input = st.number_input(
            "Your Production Budget ($M)",
            min_value=0.5, max_value=500.0, value=100.0, step=0.5,
            help="Enter your planned production budget in millions. Leave at 0 to auto-estimate."
        )
        runtime  = st.slider("Runtime (minutes)", 60, 240, 120)
        vote_avg = st.slider("Target Rating (0–10)", 0.0, 10.0, 7.0, 0.1,
                              help="Expected critical/audience rating based on comparable films")

    with c2:
        st.markdown("**Release Strategy**")
        month_labels = ['Jan','Feb','Mar','Apr','May','Jun',
                        'Jul','Aug','Sep','Oct','Nov','Dec']
        m_sel  = st.selectbox("Target Release Month", month_labels, index=4)
        m_num  = month_labels.index(m_sel) + 1
        year   = st.slider("Release Year", 2024, 2035, 2025)
        lang   = st.selectbox("Original Language",
                               [0,1,2,3],
                               format_func=lambda x: ['English','French','Spanish','Other'][x])

    with c3:
        st.markdown("**Content Profile**")
        pop    = st.slider("Projected Popularity Score", 0.0, 300.0, 60.0, 1.0,
                            help="TMDB-style popularity. Blockbusters score 100–300. Indies 10–40.")
        g_cnt  = st.slider("Number of Genres", 1, 6, 2)
        k_cnt  = st.slider("Number of Keywords / Themes", 1, 15, 5)
        c_cnt  = st.slider("Top-Billed Cast Size", 1, 5, 3)
        vote_cnt = st.number_input("Projected Vote Count", 100, 100_000, 5000, step=500)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-head">Sentiment Input — Novelty (M5)</div>', unsafe_allow_html=True)
    review = st.text_area(
        "Paste a logline, synopsis, trailer description, or early reviews",
        placeholder="e.g. 'A breathtaking epic — stunning visuals and a masterpiece performance. Must-watch blockbuster.'",
        height=100,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col_btn, _ = st.columns([1, 2])
    predict_clicked = col_btn.button("Predict This Movie", use_container_width=True)

    if predict_clicked:
        try:
            model = _get_model()
        except Exception:
            st.error("Model not found. Run `python train.py` first.")
            return

        # Build input dict — budget in dollars
        budget_dollars = budget_input * 1_000_000

        inp = {
            'budget':        budget_dollars,
            'popularity':    pop,
            'vote_count':    vote_cnt,
            'runtime':       runtime,
            'vote_average':  vote_avg,
            'release_month': m_num,
            'release_year':  year,
            'lang_enc':      lang,
            'genre_count':   g_cnt,
            'keyword_count': k_cnt,
            'cast_count':    c_cnt,
        }

        from utils.model import predict_revenue
        base_rev = predict_revenue(model, inp)

        # Sentiment fusion
        if review.strip():
            from utils.sentiment import sentiment_adjusted_revenue
            res      = sentiment_adjusted_revenue(base_rev, review)
            final    = res['final_revenue']
            sent_label = res['sentiment']['label']
            polarity   = res['sentiment']['polarity']
            tmult      = res['total_mult']
            ph, nh     = res['pos_hits'], res['neg_hits']
        else:
            final, sent_label, polarity, tmult, ph, nh = base_rev, 'N/A', 0.0, 1.0, 0, 0

        final_m = final / 1_000_000

        # Classification
        cls_label, cls_color, cls_desc = classify_movie(final_m)

        # Budget estimation
        auto_budget_m = estimate_budget(final_m, g_cnt, runtime, pop)
        roi            = roi_estimate(final_m, budget_input)

        # ── MAIN RESULT ────────────────────────────────────────────────────
        st.markdown(f"""
        <div class="result-card">
          <div class="result-label">Predicted Box Office Revenue</div>
          <div class="result-value">${final_m:.1f}M</div>
          <div class="result-sub">
            Base ML prediction: ${base_rev/1e6:.1f}M
            &nbsp;·&nbsp; Sentiment multiplier: {tmult:.2f}x
          </div>
          <div class="classification-badge"
               style="background:{cls_color}22;color:{cls_color};border:2px solid {cls_color}">
            {cls_label}
          </div>
          <div style="color:#aaa;font-size:14px;max-width:520px;margin:0 auto">{cls_desc}</div>
        </div>
        """, unsafe_allow_html=True)

        # ── BUDGET + ROI ROW ───────────────────────────────────────────────
        st.markdown("#### Budget & Financial Forecast")
        b1, b2, b3, b4 = st.columns(4)

        b1.markdown(f"""
        <div class="budget-card">
          <div class="budget-label">Your Budget</div>
          <div class="budget-value">${budget_input:.0f}M</div>
          <div class="budget-sub">Entered production cost</div>
        </div>""", unsafe_allow_html=True)

        b2.markdown(f"""
        <div class="budget-card">
          <div class="budget-label">Recommended Budget</div>
          <div class="budget-value">${auto_budget_m:.0f}M</div>
          <div class="budget-sub">To break even on ${final_m:.0f}M revenue</div>
        </div>""", unsafe_allow_html=True)

        roi_color = '#4CAF50' if roi > 0 else '#F44336'
        b3.markdown(f"""
        <div class="budget-card">
          <div class="budget-label">Estimated ROI</div>
          <div class="budget-value" style="color:{roi_color}">{roi:+.0f}%</div>
          <div class="budget-sub">After production + P&A costs</div>
        </div>""", unsafe_allow_html=True)

        profit_m = final_m - (budget_input * 1.5)
        profit_color = '#4CAF50' if profit_m > 0 else '#F44336'
        b4.markdown(f"""
        <div class="budget-card">
          <div class="budget-label">Est. Net Profit</div>
          <div class="budget-value" style="color:{profit_color}">${profit_m:.0f}M</div>
          <div class="budget-sub">Revenue minus total spend</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── CLASSIFICATION BREAKDOWN ───────────────────────────────────────
        st.markdown("#### Classification Breakdown")
        tiers = [
            ("BLOCKBUSTER", "$500M+", "#FFD700", final_m >= 500),
            ("HIT",         "$150M–$500M", "#4CAF50", 150 <= final_m < 500),
            ("AVERAGE",     "$50M–$150M",  "#FFC107", 50 <= final_m < 150),
            ("BELOW AVG",   "$10M–$50M",   "#FF9800", 10 <= final_m < 50),
            ("FLOP",        "< $10M",       "#F44336", final_m < 10),
        ]
        tier_cols = st.columns(5)
        for col, (name, rng, color, active) in zip(tier_cols, tiers):
            bg      = f"{color}22" if active else "#141414"
            border  = color if active else "#2a2a2a"
            opacity = "1" if active else "0.4"
            col.markdown(f"""
            <div style="background:{bg};border:2px solid {border};border-radius:8px;
                        padding:16px 10px;text-align:center;opacity:{opacity}">
              <div style="color:{color};font-size:13px;font-weight:800">{name}</div>
              <div style="color:#aaa;font-size:12px;margin-top:4px">{rng}</div>
              {'<div style="color:'+color+';font-size:18px;margin-top:6px">✓</div>' if active else ''}
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── METRICS ROW ───────────────────────────────────────────────────
        st.markdown("#### Prediction Summary")
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Revenue Forecast", f"${final_m:.1f}M")
        m2.metric("Classification",   cls_label)
        m3.metric("Your Budget",      f"${budget_input:.0f}M")
        m4.metric("Recommended Budget", f"${auto_budget_m:.0f}M")
        m5.metric("ROI Estimate",     f"{roi:+.0f}%")

        # ── SENTIMENT BREAKDOWN ────────────────────────────────────────────
        if review.strip():
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### Sentiment Analysis (M5 Novelty)")
            sent_color = '#4CAF50' if sent_label=='Positive' else ('#F44336' if sent_label=='Negative' else '#FFC107')
            s1, s2, s3, s4 = st.columns(4)
            s1.metric("Sentiment", sent_label)
            s2.metric("Polarity Score", f"{polarity:.3f}")
            s3.metric("Positive Keywords", ph)
            s4.metric("Negative Keywords", nh)

            pct = int((polarity + 1) / 2 * 100)
            st.markdown(f"""
            <div style="background:#141414;border-radius:8px;padding:16px 20px;margin-top:8px">
              <div style="color:#aaa;font-size:12px;margin-bottom:8px;letter-spacing:1px">
                POLARITY GAUGE
              </div>
              <div style="background:#2a2a2a;border-radius:6px;height:10px;overflow:hidden">
                <div style="background:{sent_color};width:{pct}%;height:100%;border-radius:6px"></div>
              </div>
              <div style="display:flex;justify-content:space-between;
                          color:#555;font-size:11px;margin-top:6px">
                <span>−1.0  Very Negative</span>
                <span>0.0  Neutral</span>
                <span>+1.0  Very Positive</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

        # ── RELEASE TIMING TIP ────────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        peak_months = {5,6,7,11,12}
        timing_msg  = (
            f"May–July or November–December are peak box office windows. "
            f"Your chosen release month ({m_sel}) is in a {'peak' if m_num in peak_months else 'non-peak'} period."
        )
        timing_color = '#4CAF50' if m_num in peak_months else '#FFC107'
        st.markdown(f"""
        <div style="background:#141414;border-left:4px solid {timing_color};
                    border-radius:6px;padding:14px 18px;color:#aaa;font-size:14px">
          <b style="color:{timing_color}">Release Timing:</b> {timing_msg}
        </div>
        """, unsafe_allow_html=True)