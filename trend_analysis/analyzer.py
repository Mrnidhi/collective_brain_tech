from collections import Counter
from typing import List, Tuple

def rank_keywords(keywords: List[Tuple[str, float]]) -> List[Tuple[str, float]]:
    return sorted(keywords, key=lambda x: x[1], reverse=True)

def rank_entities(entities: List[str]) -> List[Tuple[str, int]]:
    counter = Counter(entities)
    return counter.most_common()

def rank_tags(tags: List[str]) -> List[Tuple[str, int]]:
    counter = Counter(tags)
    return counter.most_common()

def rank_repos(repos: List[str]) -> List[Tuple[str, int]]:
    counter = Counter(repos)
    return counter.most_common() 