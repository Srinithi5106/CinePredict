import streamlit as st
import joblib
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@st.cache_resource
def _load_all():
    base     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    m_path   = os.path.join(base, 'models', 'best_model.pkl')
    mt_path  = os.path.join(base, 'models', 'metrics.pkl')
    model    = joblib.load(m_path)
    metrics  = joblib.load(mt_path)
    return model, metrics

def show_metrics():
    st.markdown("""
    <div style="border-left:4px solid #E50914;padding:4px 20px;margin-bottom:28px">
      <h1 style="color:#fff;margin:0">Model Metrics</h1>
      <p style="color:#888;margin:4px 0 0">Training results, R² comparison, and feature importances</p>
    </div>
    """, unsafe_allow_html=True)

    try:
        model, metrics = _load_all()
    except Exception:
        st.error("Model not found. Run: `python train.py` first.")
        return

    best_name = max(metrics, key=lambda k: metrics[k]['r2'])

    # Score cards
    st.markdown("#### Model Scores")
    cols = st.columns(len(metrics))
    for col, (name, res) in zip(cols, metrics.items()):
        is_best = (name == best_name)
        border  = '#E50914' if is_best else '#2a2a2a'
        badge   = '<span style="background:#E50914;color:#fff;font-size:10px;padding:2px 8px;border-radius:3px;margin-left:8px">BEST</span>' if is_best else ''
        col.markdown(f"""
        <div style="background:#1a1a1a;border:1px solid {border};border-radius:10px;
                    padding:20px;text-align:center">
          <div style="color:#aaa;font-size:13px;margin-bottom:4px">{name}{badge}</div>
          <div style="color:#E50914;font-size:38px;font-weight:900">{res['r2']:.3f}</div>
          <div style="color:#555;font-size:12px">R² Score</div>
          <div style="color:#888;font-size:15px;margin-top:10px">MAE: {res['mae']:.3f}</div>
          <div style="color:#666;font-size:13px">RMSE: {res.get('rmse', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts row
    from utils.model import plot_r2_comparison, plot_actual_vs_predicted, plot_feature_importance, FEATURES
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### R² Comparison")
        fig = plot_r2_comparison(metrics)
        st.pyplot(fig)
    with c2:
        st.markdown("#### Actual vs Predicted")
        fig2 = plot_actual_vs_predicted(metrics)
        if fig2:
            st.pyplot(fig2)

    st.markdown("<hr style='border-color:#222'>", unsafe_allow_html=True)

    # Feature importance
    st.markdown("#### Feature Importances")
    fig3 = plot_feature_importance(model, FEATURES)
    if fig3:
        st.pyplot(fig3)
    else:
        st.info("Feature importances are not available for Linear Regression.")

    st.markdown("<br>", unsafe_allow_html=True)

    # Expected R² explanation
    st.markdown("""
    <div style="background:#141414;border:1px solid #222;border-radius:10px;padding:20px 24px">
      <div style="color:#fff;font-size:15px;font-weight:700;margin-bottom:10px">
        Interpreting the Scores
      </div>
      <div style="color:#aaa;font-size:14px;line-height:1.8">
        <b style="color:#fff">R² (Coefficient of Determination)</b> — measures how much variance the model explains.
        1.0 is perfect; 0.0 means the model is no better than predicting the mean. An R² of ~0.78
        means XGBoost explains 78% of the variance in log(revenue).<br><br>
        <b style="color:#fff">MAE (Mean Absolute Error)</b> — average log-dollar prediction error.
        Lower is better. Since predictions are in log space, the actual dollar error grows exponentially
        with larger budgets.<br><br>
        <b style="color:#fff">Why XGBoost wins</b> — it handles non-linear relationships between
        budget, popularity, and revenue better than Linear Regression, and its 300-tree ensemble
        with subsampling reduces overfitting versus a simple Random Forest.
      </div>
    </div>
    """, unsafe_allow_html=True)