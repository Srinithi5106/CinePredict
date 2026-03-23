import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import joblib
import os
import sys

FEATURES = [
    'log_budget',
    'log_popularity',
    'log_vote_count',
    'runtime',
    'vote_average',
    'release_month',
    'release_year',
    'lang_enc',
    'genre_count',
    'keyword_count',
    'cast_count',
]
TARGET = 'log_revenue'

def apply_log_transforms(df):
    dfc = df.copy()
    dfc['log_budget']     = np.log1p(dfc['budget'])
    dfc['log_revenue']    = np.log1p(dfc['revenue'])
    dfc['log_popularity'] = np.log1p(dfc['popularity'])
    dfc['log_vote_count'] = np.log1p(dfc['vote_count'])
    return dfc

def encode_language(df, le=None):
    dfc = df.copy()
    if le is None:
        le = LabelEncoder()
        dfc['lang_enc'] = le.fit_transform(dfc['original_language'].fillna('en'))
        models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models')
        os.makedirs(models_dir, exist_ok=True)
        joblib.dump(le, os.path.join(models_dir, 'lang_encoder.pkl'))
    else:
        known = set(le.classes_)
        dfc['original_language'] = dfc['original_language'].fillna('en').apply(
            lambda x: x if x in known else 'en'
        )
        dfc['lang_enc'] = le.transform(dfc['original_language'])
    return dfc, le

def add_count_features(df):
    dfc = df.copy()
    dfc['genre_count']   = dfc['genres'].apply(lambda x: len(str(x).split(',')) if pd.notna(x) else 0)
    dfc['keyword_count'] = dfc['keywords'].apply(lambda x: len(str(x).split(',')) if pd.notna(x) else 0)
    dfc['cast_count']    = dfc['cast'].apply(lambda x: len(str(x).split(',')) if pd.notna(x) else 0)
    return dfc

def build_feature_matrix(df):
    df = apply_log_transforms(df)
    df, _ = encode_language(df)
    df = add_count_features(df)
    df = df.dropna(subset=FEATURES + [TARGET])
    X = df[FEATURES]
    y = df[TARGET]
    print(f"[M3] Feature matrix: {X.shape}")
    return X, y

if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    raw = pd.read_csv('data/cleaned_movies.csv')
    X, y = build_feature_matrix(raw)
    print('Sample:')
    print(X.head())