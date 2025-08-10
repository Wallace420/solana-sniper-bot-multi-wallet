from typing import List
from collections import Counter

try:  # Optional scikit-learn import
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.decomposition import NMF
except Exception:  # pragma: no cover - fallback when sklearn missing
    CountVectorizer = None
    NMF = None

POSITIVE_WORDS = {"gain", "bullish", "up", "increase", "profit"}
NEGATIVE_WORDS = {"loss", "bearish", "down", "decrease", "selloff"}

def simple_sentiment_score(text: str) -> float:
    """Compute a very naive sentiment score based on word occurrences."""
    tokens: List[str] = text.lower().split()
    pos = sum(1 for t in tokens if t in POSITIVE_WORDS)
    neg = sum(1 for t in tokens if t in NEGATIVE_WORDS)
    total = pos + neg
    if total == 0:
        return 0.0
    return (pos - neg) / total


def extract_topics(texts: List[str], n_topics: int = 2, n_words: int = 3) -> List[List[str]]:
    """Return top keywords for ``n_topics`` discovered in ``texts``.

    Uses scikit-learn's NMF when available; otherwise falls back to simple
    frequency counts across the corpus.
    """
    if not texts:
        return []
    if CountVectorizer and NMF:
        vec = CountVectorizer(stop_words="english")
        X = vec.fit_transform(texts)
        model = NMF(n_components=n_topics, init="random", random_state=0, max_iter=200)
        W = model.fit_transform(X)
        H = model.components_
        vocab = vec.get_feature_names_out()
        topics: List[List[str]] = []
        for comp in H:
            indices = comp.argsort()[-n_words:][::-1]
            topics.append([vocab[i] for i in indices])
        return topics
    # Fallback: global word frequency
    counter = Counter()
    for text in texts:
        counter.update(word for word in text.lower().split() if word.isalpha())
    most_common = [word for word, _ in counter.most_common(n_words)]
    return [most_common]
