import json
import pandas as pd
from trend_analysis.cleaner import clean_text_advanced
from trend_analysis.extractor import extract_keywords_tfidf, extract_keywords_keybert, extract_entities_spacy
from trend_analysis.analyzer import rank_keywords, rank_entities, rank_tags, rank_repos
from trend_analysis.visualizer import plot_bar, plot_wordcloud


def main():
    # Load data
    with open('fetched_data.json') as f:
        data = json.load(f)
    df = pd.DataFrame(data)

    # Clean text
    df['clean_text'] = df['text'].apply(clean_text_advanced)

    # Extract all tags and repos
    all_tags = [tag for tags in df['tags'] for tag in tags]
    all_repos = [meta['repo'] for meta in df['meta'] if 'repo' in meta and meta['repo']]

    # Keyword extraction
    tfidf_keywords = extract_keywords_tfidf(df['clean_text'].tolist(), top_n=20)
    keybert_keywords = extract_keywords_keybert(df['clean_text'].tolist(), top_n=20)
    entities = extract_entities_spacy(df['clean_text'].tolist())

    # Ranking
    ranked_keywords = rank_keywords(tfidf_keywords)
    ranked_entities = rank_entities(entities)
    ranked_tags = rank_tags(all_tags)
    ranked_repos = rank_repos(all_repos)

    # Save trends
    trends = {
        'top_keywords': ranked_keywords,
        'top_entities': ranked_entities,
        'top_tags': ranked_tags,
        'top_repos': ranked_repos,
        'keybert_keywords': keybert_keywords
    }
    with open('trends.json', 'w') as f:
        json.dump(trends, f, indent=2)

    # Visualizations
    plot_bar(ranked_keywords, 'Top Keywords (TF-IDF)', 'Keyword', 'Score')
    plot_bar(ranked_tags, 'Top Tags', 'Tag', 'Count')
    plot_bar(ranked_repos, 'Top GitHub Repos', 'Repo', 'Count')
    plot_wordcloud([kw[0] for kw in ranked_keywords], 'Keyword Word Cloud')
    if ranked_entities:
        plot_bar(ranked_entities, 'Top Entities (NER)', 'Entity', 'Count')

if __name__ == '__main__':
    main() 