"""
train.py — One-click pipeline runner.
Run from inside the cinepredict/ folder:
    python train.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=" * 60)
    print("  CinePredict — Full Training Pipeline")
    print("=" * 60)

    # Step 1: Preprocess
    print("\n[1/2]  Preprocessing data...")
    try:
        from data.preprocess import run_preprocessing
        df = run_preprocessing()
        print(f"       Done. {len(df)} rows.")
    except FileNotFoundError as e:
        print(f"\n  ERROR: {e}")
        sys.exit(1)

    # Step 2: Train models
    print("\n[2/2]  Training models...")
    import pandas as pd
    from utils.features import build_feature_matrix
    from utils.model import split_data, train_and_evaluate, save_best_model

    raw     = pd.read_csv(os.path.join('data', 'cleaned_movies.csv'))
    X, y    = build_feature_matrix(raw)
    X_tr, X_te, y_tr, y_te = split_data(X, y)
    results = train_and_evaluate(X_tr, X_te, y_tr, y_te)
    best_name, _ = save_best_model(results)

    print("\n" + "=" * 60)
    print(f"  Training complete. Best model: {best_name}")
    print("  Run: streamlit run app.py")
    print("=" * 60)

if __name__ == '__main__':
    main()