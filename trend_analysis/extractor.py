from typing import List, Tuple
import re

def extract_keywords_tfidf(texts: List[str], top_n: int = 10) -> List[Tuple[str, float]]:
    from sklearn.feature_extraction.text import TfidfVectorizer
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    X = vectorizer.fit_transform(texts)
    scores = X.sum(axis=0).A1
    keywords = [(word, scores[idx]) for word, idx in vectorizer.vocabulary_.items()]
    keywords.sort(key=lambda x: x[1], reverse=True)
    return keywords[:top_n]


def extract_keywords_keybert(texts: List[str], top_n: int = 10) -> List[Tuple[str, float]]:
    try:
        from keybert import KeyBERT
        kw_model = KeyBERT()
        joined = ' '.join(texts)
        keywords = kw_model.extract_keywords(joined, top_n=top_n)
        return keywords
    except ImportError:
        return []


def extract_entities_spacy(texts: List[str], model: str = 'en_core_web_sm') -> List[str]:
    try:
        import spacy
        nlp = spacy.load(model)
        joined = ' '.join(texts)
        doc = nlp(joined)
        return list(set(ent.text for ent in doc.ents if len(ent.text) > 2))
    except ImportError:
        return []
    except OSError:
        return [] 