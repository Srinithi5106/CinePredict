from textblob import TextBlob
import nltk
import re

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

STOP = set(stopwords.words('english'))

HYPE_POS = [
    'masterpiece','oscar','must watch','brilliant','epic','spectacular',
    'stunning','breathtaking','blockbuster','unforgettable','emotional',
    'powerful','incredible','outstanding','magnificent','exceptional',
    'phenomenal','thrilling','riveting','captivating',
]
HYPE_NEG = [
    'boring','terrible','awful','waste','disaster','flop','unwatchable',
    'disappointing','skip','dreadful','painful','forgettable','mediocre',
    'generic','predictable','cliche','lifeless','sluggish','bloated',
]

def clean_text(text):
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.lower().strip()
    try:
        tokens = word_tokenize(text)
        tokens = [t for t in tokens if t not in STOP and len(t) > 2]
        return ' '.join(tokens)
    except Exception:
        return text

def get_sentiment_score(text):
    cleaned  = clean_text(text)
    blob     = TextBlob(cleaned)
    polarity = blob.sentiment.polarity
    subj     = blob.sentiment.subjectivity
    if polarity > 0.1:
        label = 'Positive'
    elif polarity < -0.1:
        label = 'Negative'
    else:
        label = 'Neutral'
    return {
        'polarity':     round(polarity, 4),
        'subjectivity': round(subj, 4),
        'label':        label,
    }

def polarity_multiplier(polarity):
    if   polarity >=  0.8: return 1.25
    elif polarity >=  0.1: return 1.10
    elif polarity >= -0.1: return 1.00
    elif polarity >= -0.8: return 0.90
    else:                  return 0.75

def keyword_bonus(text):
    lower    = text.lower()
    pos_hits = sum(1 for w in HYPE_POS if w in lower)
    neg_hits = sum(1 for w in HYPE_NEG if w in lower)
    mult     = 1.0 + (pos_hits * 0.02) - (neg_hits * 0.02)
    mult     = max(0.50, min(mult, 1.50))
    return round(mult, 3), pos_hits, neg_hits

def sentiment_adjusted_revenue(base_revenue, review_text):
    sentiment  = get_sentiment_score(review_text)
    pol_mult   = polarity_multiplier(sentiment['polarity'])
    kw_mult, ph, nh = keyword_bonus(review_text)
    final      = base_revenue * pol_mult * kw_mult
    return {
        'base_revenue':  round(base_revenue, 2),
        'final_revenue': round(final, 2),
        'sentiment':     sentiment,
        'polarity_mult': pol_mult,
        'keyword_mult':  kw_mult,
        'pos_hits':      ph,
        'neg_hits':      nh,
        'total_mult':    round(pol_mult * kw_mult, 3),
    }

if __name__ == '__main__':
    r = sentiment_adjusted_revenue(100_000_000, 'Absolute masterpiece. Epic and stunning visuals!')
    print(r)