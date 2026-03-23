import pandas as pd
import numpy as np
import ast
import os

def parse_names(obj, key='name', limit=3):
    try:
        lst = ast.literal_eval(str(obj))
        return [d[key] for d in lst[:limit]]
    except:
        return []

def get_director(crew_str):
    try:
        crew = ast.literal_eval(str(crew_str))
        for p in crew:
            if p.get('job') == 'Director':
                return p['name']
    except:
        pass
    return 'Unknown'

def run_preprocessing():
    base = os.path.dirname(os.path.abspath(__file__))
    movies_path  = os.path.join(base, 'tmdb_5000_movies.csv')
    credits_path = os.path.join(base, 'tmdb_5000_credits.csv')

    if not os.path.exists(movies_path) or not os.path.exists(credits_path):
        raise FileNotFoundError(
            "Dataset CSVs not found in /data folder.\n"
            "Download from: https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata\n"
            "Place tmdb_5000_movies.csv and tmdb_5000_credits.csv in the data/ folder."
        )

    print("[M1] Loading CSVs...")
    movies  = pd.read_csv(movies_path)
    credits = pd.read_csv(credits_path)

    if 'movie_id' in credits.columns:
        credits.rename(columns={'movie_id': 'id'}, inplace=True)
    if 'title' in credits.columns:
        credits.rename(columns={'title': 'title_credit'}, inplace=True)

    df = movies.merge(credits, on='id')

    drop_cols = [
        'homepage','tagline','overview','status','original_title',
        'spoken_languages','production_companies','production_countries','title_credit',
    ]
    df.drop(columns=[c for c in drop_cols if c in df.columns], inplace=True)

    df = df[(df['budget'] > 0) & (df['revenue'] > 0)]
    df.dropna(subset=['runtime','release_date'], inplace=True)
    print(f"[M1] After filter: {df.shape}")

    df['genres']   = df['genres'].apply(parse_names)
    df['keywords'] = df['keywords'].apply(parse_names)
    df['cast']     = df['cast'].apply(parse_names)
    df['director'] = df['crew'].apply(get_director)
    df.drop(columns=['crew'], inplace=True)

    df['release_date']  = pd.to_datetime(df['release_date'], errors='coerce')
    df['release_year']  = df['release_date'].dt.year
    df['release_month'] = df['release_date'].dt.month
    df.drop(columns=['release_date'], inplace=True)

    for col in ['genres','keywords','cast']:
        df[col] = df[col].apply(lambda x: ','.join(x) if isinstance(x, list) else str(x))

    out = os.path.join(base, 'cleaned_movies.csv')
    df.to_csv(out, index=False)
    print(f"[M1] Saved cleaned_movies.csv  shape={df.shape}")
    return df

if __name__ == '__main__':
    run_preprocessing()