import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd

# GitHub theme colors
COLORS = {
    'primary': '#2ea44f',
    'secondary': '#6e7681',
    'background': '#f6f8fa',
    'text': '#24292e',
    'grid': '#d0d7de'
}

def set_github_style():
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams['figure.facecolor'] = COLORS['background']
    plt.rcParams['axes.facecolor'] = COLORS['background']
    plt.rcParams['grid.color'] = COLORS['grid']
    plt.rcParams['text.color'] = COLORS['text']
    plt.rcParams['axes.labelcolor'] = COLORS['text']
    plt.rcParams['xtick.color'] = COLORS['text']
    plt.rcParams['ytick.color'] = COLORS['text']
    plt.rcParams['font.family'] = 'sans-serif'

def show_bar_chart(data, title, xlabel, ylabel, top_n=10):
    if not data:
        st.info('No data to display.')
        return
    
    set_github_style()
    items = data[:top_n]
    labels, values = zip(*items)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(labels, values)
    
    # Style the bars
    for bar in bars:
        bar.set_color(COLORS['primary'])
        bar.set_alpha(0.8)
    
    # Customize the plot
    ax.set_title(title, pad=20, fontsize=14, fontweight='bold')
    ax.set_xlabel(xlabel, labelpad=10)
    ax.set_ylabel(ylabel, labelpad=10)
    
    # Rotate labels for better readability
    plt.xticks(rotation=45, ha='right')
    
    # Adjust layout
    plt.tight_layout()
    st.pyplot(fig)

def show_wordcloud(words, title):
    if not words:
        st.info('No data to display.')
        return
    
    # Create and configure the word cloud
    wc = WordCloud(
        width=800,
        height=400,
        background_color=COLORS['background'],
        colormap='YlGn',  # Green-focused colormap
        max_words=50,
        prefer_horizontal=0.7
    ).generate(' '.join(words))
    
    # Create the figure
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    if title:
        ax.set_title(title, pad=20, fontsize=14, fontweight='bold')
    
    # Adjust layout
    plt.tight_layout()
    st.pyplot(fig)

def show_line_chart(df: pd.DataFrame, search_query: str, top_n: int):
    if 'timestamp' not in df.columns or df.empty:
        return
    
    set_github_style()
    df = df.copy()  # Create a copy to avoid SettingWithCopyWarning
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    
    # Get top keywords
    from collections import Counter
    all_words = [w.lower() for txt in df['text'] for w in str(txt).split()]
    if search_query:
        all_words = [w for w in all_words if search_query in w]
    top_words = [w for w, _ in Counter(all_words).most_common(top_n)]
    
    # Prepare time series data
    df['date'] = df['timestamp'].dt.date
    data = {w: [] for w in top_words}
    dates = sorted(df['date'].unique())
    
    for w in top_words:
        for d in dates:
            count = df[(df['date'] == d) & (df['text'].str.lower().str.contains(w))].shape[0]
            data[w].append(count)
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Plot each keyword
    for i, w in enumerate(top_words):
        color = plt.cm.YlGn(0.3 + (i * 0.7 / len(top_words)))  # Green color gradient
        ax.plot(dates, data[w], label=w, color=color, linewidth=2, alpha=0.8)
    
    # Customize the plot
    ax.set_title('Trend Over Time', pad=20, fontsize=14, fontweight='bold')
    ax.set_xlabel('Date', labelpad=10)
    ax.set_ylabel('Mentions', labelpad=10)
    
    # Add legend
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Adjust layout
    plt.tight_layout()
    st.pyplot(fig)

def show_table(df: pd.DataFrame, view_by: str, top_n: int, search_query: str = None):
    icon_map = {'github': '🐙', 'stackoverflow': '💬', 'reddit': '👽'}
    
    # Prepare the data
    if view_by == 'tags':
        df = df.explode('tags')
        show_cols = ['source', 'timestamp', 'tags', 'text']
    else:
        show_cols = ['source', 'timestamp', 'text']
    
    # Apply search filter
    if search_query:
        mask = (
            df['text'].str.lower().str.contains(search_query) |
            df['tags'].apply(lambda tags: any(search_query in str(tag).lower() for tag in tags))
        )
        df = df[mask]
    
    # Prepare display table
    table = df[show_cols].head(top_n).copy()
    
    # Add platform icons and format links
    table['platform'] = table['source'].map(icon_map)
    table['link'] = df['meta'].apply(lambda m: m.get('url', ''))
    
    def make_clickable(row):
        text = row['text'][:100] + '...' if len(row['text']) > 100 else row['text']
        return f"[{text}]({row['link']})" if row['link'] else text
    
    table['content'] = table.apply(make_clickable, axis=1)
    
    # Display columns
    display_cols = ['platform', 'timestamp', 'content']
    if 'tags' in table.columns:
        display_cols.insert(-1, 'tags')
    
    # Convert to markdown
    st.markdown(
        table[display_cols].to_markdown(index=False),
        unsafe_allow_html=True
    ) 