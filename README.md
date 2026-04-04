# CinePredict 🎬 CinePredict — Box Office Revenue Prediction Engine

ML Lab Project | Netflix-Styled Streamlit App | Team of 6

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Download TMDB dataset from Kaggle and place in /data:
#    - tmdb_5000_movies.csv
#    - tmdb_5000_credits.csv

# 3. Preprocess data (Member 1)
python data/preprocess.py

# 4. Train and save model (Member 4)
python utils/model.py

# 5. Launch the app (Member 6)
streamlit run app.py
```

## Project Structure

```
cinepredict/
├── app.py                    ← Main Streamlit app (M6)
├── requirements.txt
├── .streamlit/
│   └── config.toml           ← Netflix dark theme
├── data/
│   ├── preprocess.py         ← M1: Data cleaning
│   ├── tmdb_5000_movies.csv  ← Download from Kaggle
│   └── tmdb_5000_credits.csv ← Download from Kaggle
├── utils/
│   ├── eda.py                ← M2: EDA charts (all Plotly)
│   ├── features.py           ← M3: Feature engineering
│   ├── model.py              ← M4: Model training & inference
│   └── sentiment.py          ← M5: NLP sentiment fusion (NOVELTY)
├── pages/
│   ├── home.py               ← Home / hero page
│   ├── eda_page.py           ← EDA Dashboard
│   ├── predict.py            ← Revenue prediction
│   ├── sentiment_page.py     ← Sentiment analyzer
│   └── metrics_page.py       ← Model metrics
└── models/
    ├── best_model.pkl         ← Auto-saved after training
    ├── lang_encoder.pkl       ← Label encoder
    └── metrics.pkl            ← Saved model comparison metrics
```

## Team Split

| Member | Role                         | File(s)                      |
|--------|------------------------------|------------------------------|
| M1     | Data Collection & Cleaning   | `data/preprocess.py`         |
| M2     | EDA & Visualization          | `utils/eda.py`               |
| M3     | Feature Engineering          | `utils/features.py`          |
| M4     | Model Building & Evaluation  | `utils/model.py`             |
| M5     | Sentiment Novelty (NLP)      | `utils/sentiment.py`         |
| M6     | Netflix UI & Integration     | `app.py` + `pages/`          |

## Novelty Feature

Standard box office models use only structured metadata.
**CinePredict adds a 2-layer NLP pipeline:**
1. **TextBlob polarity** → revenue multiplier (0.72× to 1.30×)
2. **Keyword hype detection** → fine adjustment (±2.5% per keyword)

This mimics how real audience buzz drives opening weekend performance.
