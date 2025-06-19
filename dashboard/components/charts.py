import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd


def show_bar_chart(data, title, xlabel, ylabel, top_n=10):
    items = data[:top_n]
    if not items:
        st.info('No data to display.')
        return
    labels, values = zip(*items)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(labels, values, color='skyblue')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)


def show_wordcloud(words, title):
    if not words:
        st.info('No data to display.')
        return
    text = ' '.join(words)
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    ax.set_title(title)
    st.pyplot(fig)


def show_line_chart(df: pd.DataFrame, search_query: str, top_n: int):
    if 'timestamp' not in df.columns or df.empty:
        return
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    # Use top N keywords in this filtered df
    from collections import Counter
    all_words = [w.lower() for txt in df['text'] for w in str(txt).split()]
    if search_query:
        all_words = [w for w in all_words if search_query in w]
    top_words = [w for w, _ in Counter(all_words).most_common(top_n)]
    # Build time series for each word
    df['date'] = df['timestamp'].dt.date
    data = {w: [] for w in top_words}
    dates = sorted(df['date'].unique())
    for w in top_words:
        for d in dates:
            count = df[(df['date'] == d) & (df['text'].str.lower().str.contains(w))].shape[0]
            data[w].append(count)
    fig, ax = plt.subplots(figsize=(10, 4))
    for w in top_words:
        ax.plot(dates, data[w], label=w)
    ax.set_title('Trend Over Time (Top Keywords)')
    ax.set_xlabel('Date')
    ax.set_ylabel('Frequency')
    ax.legend()
    st.pyplot(fig)


def show_table(df: pd.DataFrame, view_by: str, top_n: int, search_query: str = None):
    icon_map = {'github': '🐙', 'stackoverflow': '🟧', 'reddit': '👽'}
    if view_by == 'tags':
        col = 'tags'
    elif view_by == 'keywords':
        col = 'text'
    elif view_by == 'repos':
        col = 'meta'
    elif view_by == 'entities':
        col = 'text'
    else:
        col = 'text'
    # Filter by search
    if search_query:
        mask = (
            df['text'].str.lower().str.contains(search_query) |
            df['tags'].apply(lambda tags: any(search_query in str(tag).lower() for tag in tags))
        )
        df = df[mask]
    # Show top N rows
    show_cols = ['source', 'timestamp', 'text']
    if col == 'meta':
        df = df[df['meta'].apply(lambda m: m.get('repo', '')) != '']
        df = df.head(top_n)
        table = df[['source', 'timestamp', 'text']].copy()
        table['repo'] = df['meta'].apply(lambda m: m.get('repo', ''))
        table['link'] = df['meta'].apply(lambda m: m.get('url', ''))
    elif col == 'tags':
        df = df.explode('tags')
        df = df.head(top_n)
        table = df[['source', 'timestamp', 'tags', 'text']].copy()
        table['link'] = df['meta'].apply(lambda m: m.get('url', ''))
    else:
        table = df[show_cols].head(top_n).copy()
        table['link'] = df['meta'].apply(lambda m: m.get('url', ''))
    # Add platform icon
    table['platform'] = table['source'].map(icon_map)
    # Show as clickable links if available
    def make_link(row):
        if row['link']:
            return f"[{row['text'][:60]}...]({row['link']})"
        return row['text'][:60]
    table['snippet'] = table.apply(make_link, axis=1)
    display_cols = ['platform', 'timestamp', 'snippet']
    if 'tags' in table.columns:
        display_cols.append('tags')
    if 'repo' in table.columns:
        display_cols.append('repo')
    st.markdown(table[display_cols].to_markdown(index=False), unsafe_allow_html=True) 