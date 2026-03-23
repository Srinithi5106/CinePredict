import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@st.cache_data
def _load():
    from utils.eda import load_data
    return load_data()

def show_eda():
    st.markdown("""
    <div style="border-left:4px solid #E50914;padding:4px 20px;margin-bottom:28px">
      <h1 style="color:#fff;margin:0">Exploratory Data Analysis</h1>
      <p style="color:#888;margin:4px 0 0">Visual insights from the TMDB 5000 Movies dataset</p>
    </div>
    """, unsafe_allow_html=True)

    try:
        df = _load()
    except FileNotFoundError:
        st.error("cleaned_movies.csv not found. Run: `python train.py` first.")
        return

    from utils.eda import (
        plot_revenue_distribution, plot_correlation,
        plot_genre_revenue, plot_monthly_trend,
        plot_budget_revenue, plot_top_movies, plot_decade_revenue,
    )

    # Chart 1
    st.markdown("#### Revenue Distribution — Why Log Transform?")
    st.markdown("<p style='color:#888;font-size:14px'>Revenue is heavily right-skewed. Log-transforming compresses the scale and dramatically improves model accuracy.</p>", unsafe_allow_html=True)
    st.pyplot(plot_revenue_distribution(df))

    st.markdown("<hr style='border-color:#222'>", unsafe_allow_html=True)

    # Chart 2 + 3
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Correlation Heatmap")
        st.markdown("<p style='color:#888;font-size:14px'>Budget and popularity show the strongest positive correlation with revenue.</p>", unsafe_allow_html=True)
        st.pyplot(plot_correlation(df))
    with c2:
        st.markdown("#### Revenue by Genre")
        st.markdown("<p style='color:#888;font-size:14px'>Action and Adventure genres consistently outperform Drama and Horror.</p>", unsafe_allow_html=True)
        st.plotly_chart(plot_genre_revenue(df), use_container_width=True)

    st.markdown("<hr style='border-color:#222'>", unsafe_allow_html=True)

    # Chart 4
    st.markdown("#### Seasonal Release Month Trend")
    st.markdown("<p style='color:#888;font-size:14px'>Summer (May–Jul) and holidays (Nov–Dec) are peak box office periods.</p>", unsafe_allow_html=True)
    st.plotly_chart(plot_monthly_trend(df), use_container_width=True)

    st.markdown("<hr style='border-color:#222'>", unsafe_allow_html=True)

    # Chart 5
    st.markdown("#### Budget vs Revenue")
    st.markdown("<p style='color:#888;font-size:14px'>Strong positive relationship — but outliers reveal low-budget hits and high-budget flops.</p>", unsafe_allow_html=True)
    st.plotly_chart(plot_budget_revenue(df), use_container_width=True)

    st.markdown("<hr style='border-color:#222'>", unsafe_allow_html=True)

    # Chart 6 + 7
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Top 20 Highest Grossing Movies")
        st.plotly_chart(plot_top_movies(df), use_container_width=True)
    with c2:
        st.markdown("#### Revenue by Decade")
        st.markdown("<p style='color:#888;font-size:14px'>2000s–2010s saw the biggest revenue growth driven by franchise filmmaking.</p>", unsafe_allow_html=True)
        st.plotly_chart(plot_decade_revenue(df), use_container_width=True)