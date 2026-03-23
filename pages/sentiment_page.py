import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def show_sentiment():
    st.markdown("""
    <style>
    .verdict-card {
        border-radius: 14px;
        padding: 36px 40px;
        text-align: center;
        margin: 24px 0;
    }
    .verdict-label {
        font-size: 11px;
        letter-spacing: 4px;
        text-transform: uppercase;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .verdict-badge {
        font-size: 52px;
        font-weight: 900;
        letter-spacing: 3px;
        line-height: 1;
    }
    .verdict-desc {
        font-size: 15px;
        margin-top: 12px;
        max-width: 480px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.6;
    }
    .kw-chip {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 4px;
        font-size: 13px;
        margin: 3px;
    }
    .section-divider {
        border: none;
        border-top: 1px solid #1a1a1a;
        margin: 28px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="border-left:4px solid #E50914;padding:4px 20px;margin-bottom:20px">
      <h1 style="color:#fff;margin:0">Sentiment Analyser</h1>
      <p style="color:#888;margin:4px 0 0">
        Paste any review, logline or synopsis — get an instant NLP verdict
      </p>
    </div>
    """, unsafe_allow_html=True)

    # Novelty explainer
    st.markdown("""
    <div style="background:#1a0000;border:1px solid #E50914;border-radius:10px;
                padding:18px 24px;margin-bottom:28px">
      <span style="color:#E50914;font-size:11px;letter-spacing:3px;
                   text-transform:uppercase;font-weight:700">Project Novelty — M5</span>
      <div style="color:#fff;font-size:15px;font-weight:600;margin:6px 0 6px">
        Two-Layer NLP Pipeline
      </div>
      <div style="color:#aaa;font-size:14px;line-height:1.7">
        <b style="color:#fff">Layer 1 — TextBlob Polarity:</b>
        Scores the overall tone of the text from −1.0 (very negative) to +1.0 (very positive).<br>
        <b style="color:#fff">Layer 2 — Keyword Hype Detector:</b>
        Scans for power words like <em>"masterpiece"</em> or <em>"flop"</em> and applies
        a micro-multiplier. Both layers combine into a final revenue adjustment multiplier.
      </div>
    </div>
    """, unsafe_allow_html=True)

    review = st.text_area(
        "Paste your review, synopsis, or trailer description below",
        height=140,
        placeholder="Type or paste any text here and click Analyse...",
        label_visibility="visible",
    )

    st.markdown("<br>", unsafe_allow_html=True)
    analyse_clicked = st.button("Analyse Sentiment", use_container_width=True)

    if analyse_clicked and review.strip():
        from utils.sentiment import (
            get_sentiment_score, keyword_bonus, clean_text,
            polarity_multiplier, HYPE_POS, HYPE_NEG,
        )

        score     = get_sentiment_score(review)
        pol       = score['polarity']
        subj      = score['subjectivity']
        label     = score['label']
        kw_mult, ph, nh = keyword_bonus(review)
        pol_mult  = polarity_multiplier(pol)
        total_mult = round(pol_mult * kw_mult, 3)

        # ── Verdict colors & messaging ─────────────────────────────────────
        if label == 'Positive':
            color    = '#4CAF50'
            bg       = '#0a1a0a'
            border   = '#4CAF50'
            icon     = '▲'
            verdict  = 'POSITIVE BUZZ'
            summary  = (
                f"The review carries a strongly positive tone (polarity {pol:+.2f}). "
                f"Audience sentiment is likely to drive word-of-mouth and boost opening weekend performance."
            )
            rev_impact = f"Revenue multiplier: {total_mult:.2f}x — prediction boosted upward."
        elif label == 'Negative':
            color    = '#F44336'
            bg       = '#1a0a0a'
            border   = '#F44336'
            icon     = '▼'
            verdict  = 'NEGATIVE BUZZ'
            summary  = (
                f"The review carries a negative tone (polarity {pol:+.2f}). "
                f"Poor audience reception is likely to suppress box office performance and limit theatrical run."
            )
            rev_impact = f"Revenue multiplier: {total_mult:.2f}x — prediction adjusted downward."
        else:
            color    = '#FFC107'
            bg       = '#1a1600'
            border   = '#FFC107'
            icon     = '◆'
            verdict  = 'NEUTRAL / MIXED'
            summary  = (
                f"The review is neither clearly positive nor negative (polarity {pol:+.2f}). "
                f"Mixed buzz typically results in average opening performance with limited legs."
            )
            rev_impact = f"Revenue multiplier: {total_mult:.2f}x — no significant adjustment."

        # ── Verdict card ───────────────────────────────────────────────────
        st.markdown(f"""
        <div class="verdict-card"
             style="background:{bg};border:2px solid {border};">
          <div class="verdict-label" style="color:{color}">NLP Verdict</div>
          <div class="verdict-badge" style="color:{color}">{icon} {verdict}</div>
          <div class="verdict-desc" style="color:#cccccc">{summary}</div>
          <div style="color:{color};font-size:13px;margin-top:14px;
                      font-weight:600;letter-spacing:1px">{rev_impact}</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Score metrics ──────────────────────────────────────────────────
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Polarity Score",       f"{pol:+.4f}",  help="−1.0 = very negative · +1.0 = very positive")
        m2.metric("Subjectivity",         f"{subj:.4f}",  help="0 = objective · 1 = very subjective")
        m3.metric("Revenue Multiplier",   f"{total_mult:.3f}×")
        m4.metric("Keyword Influence",    f"+{ph} / −{nh}", help="Positive / negative power words found")

        # ── Polarity gauge ─────────────────────────────────────────────────
        pct = int((pol + 1) / 2 * 100)
        st.markdown(f"""
        <div style="background:#141414;border-radius:10px;padding:20px 24px;margin-top:4px">
          <div style="color:#666;font-size:11px;letter-spacing:2px;
                      text-transform:uppercase;margin-bottom:10px">Polarity Gauge</div>
          <div style="background:#2a2a2a;border-radius:6px;height:12px;overflow:hidden">
            <div style="background:{color};width:{pct}%;height:100%;
                        border-radius:6px;transition:width 0.5s ease"></div>
          </div>
          <div style="display:flex;justify-content:space-between;
                      color:#444;font-size:11px;margin-top:6px">
            <span>−1.0  Very Negative</span>
            <span>0.0  Neutral</span>
            <span>+1.0  Very Positive</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

        # ── Keyword chips ──────────────────────────────────────────────────
        lower = review.lower()
        found_pos = [w for w in HYPE_POS if w in lower]
        found_neg = [w for w in HYPE_NEG if w in lower]

        kc1, kc2 = st.columns(2)
        with kc1:
            st.markdown("**Positive Keywords Detected**")
            if found_pos:
                chips = " ".join([
                    f'<span class="kw-chip" style="background:#0a2a0a;color:#4CAF50;'
                    f'border:1px solid #4CAF5055">{w}</span>'
                    for w in found_pos
                ])
                st.markdown(chips, unsafe_allow_html=True)
            else:
                st.markdown("<span style='color:#444;font-size:14px'>None detected</span>",
                            unsafe_allow_html=True)

        with kc2:
            st.markdown("**Negative Keywords Detected**")
            if found_neg:
                chips = " ".join([
                    f'<span class="kw-chip" style="background:#2a0a0a;color:#F44336;'
                    f'border:1px solid #F4433655">{w}</span>'
                    for w in found_neg
                ])
                st.markdown(chips, unsafe_allow_html=True)
            else:
                st.markdown("<span style='color:#444;font-size:14px'>None detected</span>",
                            unsafe_allow_html=True)

        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

        # ── Multiplier breakdown ───────────────────────────────────────────
        st.markdown("**How the Multiplier Was Calculated**")
        st.markdown(f"""
        <div style="background:#141414;border-radius:8px;padding:18px 22px;
                    color:#aaa;font-size:14px;line-height:2">
          <span style="color:#fff">Layer 1 — Polarity multiplier:</span>
          &nbsp;{pol_mult:.2f}×
          &nbsp;<span style="color:#555">(from TextBlob polarity {pol:+.4f})</span><br>
          <span style="color:#fff">Layer 2 — Keyword hype multiplier:</span>
          &nbsp;{kw_mult:.3f}×
          &nbsp;<span style="color:#555">(+{ph} positive words, −{nh} negative words × 2% each)</span><br>
          <span style="color:#fff">Combined multiplier:</span>
          &nbsp;<span style="color:{color};font-weight:700;font-size:16px">{total_mult:.3f}×</span>
          &nbsp;<span style="color:#555">(applied to ML base revenue prediction)</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

        # ── Cleaned text ───────────────────────────────────────────────────
        with st.expander("Show cleaned text (after stop-word removal)"):
            cleaned = clean_text(review)
            st.markdown(
                f'<div style="background:#1a1a1a;border-radius:6px;padding:14px 16px;'
                f'color:#666;font-size:13px;font-family:monospace;word-break:break-word">'
                f'{cleaned}</div>',
                unsafe_allow_html=True,
            )

    elif analyse_clicked and not review.strip():
        st.warning("Please paste some text before clicking Analyse.")