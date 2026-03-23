import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import joblib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_absolute_error
from utils.features import build_feature_matrix, FEATURES, apply_log_transforms, encode_language, add_count_features

RED   = '#E50914'
DARK  = '#141414'
DARK2 = '#1a1a1a'
WHITE = '#F5F5F5'

def split_data(X, y, test_size=0.2, seed=42):
    return train_test_split(X, y, test_size=test_size, random_state=seed)

def get_models():
    return {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(
            n_estimators=200, max_depth=8, min_samples_leaf=5,
            random_state=42, n_jobs=-1),
        'XGBoost': XGBRegressor(
            n_estimators=300, learning_rate=0.05, max_depth=6,
            subsample=0.8, colsample_bytree=0.8, random_state=42, verbosity=0),
    }

def train_and_evaluate(X_train, X_test, y_train, y_test):
    models  = get_models()
    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        r2    = r2_score(y_test, preds)
        mae   = mean_absolute_error(y_test, preds)
        rmse  = float(np.sqrt(np.mean((y_test - preds)**2)))
        results[name] = {
            'model': model,
            'r2':   round(float(r2), 4),
            'mae':  round(float(mae), 4),
            'rmse': round(rmse, 4),
            'preds': [float(p) for p in preds],
            'actual': [float(a) for a in y_test],
        }
        print(f"  {name:20s}  R2={r2:.3f}  MAE={mae:.3f}  RMSE={rmse:.3f}")
    return results

def save_best_model(results):
    best_name  = max(results, key=lambda k: results[k]['r2'])
    best_model = results[best_name]['model']
    models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models')
    os.makedirs(models_dir, exist_ok=True)
    joblib.dump(best_model, os.path.join(models_dir, 'best_model.pkl'))
    metrics = {
        name: {k: v for k, v in res.items() if k != 'model'}
        for name, res in results.items()
    }
    joblib.dump(metrics, os.path.join(models_dir, 'metrics.pkl'))
    print(f"[M4] Best: {best_name} → saved to models/best_model.pkl")
    return best_name, best_model

def load_model():
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, '..', 'models', 'best_model.pkl')
    return joblib.load(path)

def predict_revenue(model, input_dict):
    d = input_dict.copy()
    d['log_budget']     = np.log1p(d['budget'])
    d['log_popularity'] = np.log1p(d['popularity'])
    d['log_vote_count'] = np.log1p(d['vote_count'])
    df_in = pd.DataFrame([d])
    log_pred = model.predict(df_in[FEATURES])[0]
    return float(np.expm1(log_pred))

def plot_feature_importance(model, feature_names=None):
    if feature_names is None:
        feature_names = FEATURES
    if not hasattr(model, 'feature_importances_'):
        return None
    imp = model.feature_importances_
    idx = np.argsort(imp)[::-1]
    fig, ax = plt.subplots(figsize=(10, 5), facecolor=DARK)
    ax.set_facecolor(DARK2)
    ax.barh([feature_names[i] for i in idx], imp[idx], color=RED, edgecolor='none')
    ax.set_title('Feature Importances', color=WHITE, fontsize=14, pad=12)
    ax.tick_params(colors=WHITE)
    for spine in ax.spines.values():
        spine.set_color('#333')
    plt.tight_layout()
    return fig

def plot_r2_comparison(metrics):
    names = list(metrics.keys())
    r2s   = [metrics[n]['r2'] for n in names]
    fig, ax = plt.subplots(figsize=(8, 4), facecolor=DARK)
    ax.set_facecolor(DARK2)
    bars = ax.bar(names, r2s, color=[RED if r == max(r2s) else '#555' for r in r2s], edgecolor='none')
    ax.set_title('Model R² Comparison', color=WHITE, fontsize=14, pad=12)
    ax.set_ylabel('R² Score', color=WHITE)
    ax.tick_params(colors=WHITE)
    ax.set_ylim(0, 1)
    for bar, val in zip(bars, r2s):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{val:.3f}', ha='center', color=WHITE, fontsize=12, fontweight='bold')
    for spine in ax.spines.values():
        spine.set_color('#333')
    plt.tight_layout()
    return fig

def plot_actual_vs_predicted(metrics):
    best = max(metrics, key=lambda k: metrics[k]['r2'])
    actual = np.array(metrics[best].get('actual', []))
    preds  = np.array(metrics[best].get('preds', []))
    if len(actual) == 0:
        return None
    fig, ax = plt.subplots(figsize=(7, 6), facecolor=DARK)
    ax.set_facecolor(DARK2)
    ax.scatter(actual, preds, alpha=0.45, color=RED, s=20, edgecolors='none')
    mn, mx = min(actual.min(), preds.min()), max(actual.max(), preds.max())
    ax.plot([mn, mx], [mn, mx], color='#888', linewidth=1.2, linestyle='--')
    ax.set_xlabel('Actual log(Revenue)', color=WHITE)
    ax.set_ylabel('Predicted log(Revenue)', color=WHITE)
    ax.set_title(f'Actual vs Predicted  [{best}]', color=WHITE, fontsize=13, pad=12)
    ax.tick_params(colors=WHITE)
    for spine in ax.spines.values():
        spine.set_color('#333')
    plt.tight_layout()
    return fig

if __name__ == '__main__':
    df = pd.read_csv('data/cleaned_movies.csv')
    X, y = build_feature_matrix(df)
    X_tr, X_te, y_tr, y_te = split_data(X, y)
    results = train_and_evaluate(X_tr, X_te, y_tr, y_te)
    save_best_model(results)