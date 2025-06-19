import streamlit as st
import os
import subprocess
from components.load_data import load_fetched_data, load_trends
from components.filters import sidebar_filters
from components.charts import show_bar_chart, show_wordcloud, show_table, show_line_chart
from components.alerts import show_alerts

st.set_page_config(page_title="Collective Brain Dashboard", layout="wide")

st.title("🧠 Collective Brain of Tech Students")

# Show alerts in sidebar
show_alerts(location='sidebar')

# Sidebar: Refresh Data Button
if st.sidebar.button('🔄 Refresh Trends'):
    with st.spinner('Refreshing data...'):
        if os.path.exists('run_fetch.py'):
            subprocess.run(['python', 'run_fetch.py'])
        if os.path.exists('trend_analysis/run_trends.py'):
            subprocess.run(['python', 'trend_analysis/run_trends.py'])
        st.cache_data.clear()
        st.experimental_rerun()

# Data loading
if not (os.path.exists("fetched_data.json") and os.path.exists("trends.json")):
    st.warning("fetched_data.json or trends.json not found. Please run the data pipeline first.\n\nTo generate data, run:\n\npython run_fetch.py\npython trend_analysis/run_trends.py")
    st.stop()

data = load_fetched_data()
trends = load_trends()

# Sidebar filters
filters = sidebar_filters(data)
df = filters['filtered_df']
platforms = filters['platforms']
view_by = filters['view_by']
top_n = filters['top_n']

# Debug print for GitHub data after filtering
st.write("GitHub rows in DataFrame after filtering:", df[df['source'] == 'github'].shape[0])

# Search box
search_query = st.text_input('🔍 Search tags, keywords, or text:').strip().lower()

# Tabs for platform-specific insights
tab_labels = ["📁 All Platforms", "🐙 GitHub", "💬 Stack Overflow", "👽 Reddit"]
tabs = st.tabs(tab_labels)
platform_map = {
    "📁 All Platforms": None,
    "🐙 GitHub": "github",
    "💬 Stack Overflow": "stackoverflow",
    "👽 Reddit": "reddit"
}

for i, tab in enumerate(tabs):
    with tab:
        platform = platform_map[tab_labels[i]]
        if platform:
            df_tab = df[df['source'] == platform]
        else:
            df_tab = df
        if df_tab.empty:
            st.info('No data found for this platform/filter.')
            continue
        # Filter by search
        if search_query:
            mask = (
                df_tab['text'].str.lower().str.contains(search_query) |
                df_tab['tags'].apply(lambda tags: any(search_query in str(tag).lower() for tag in tags))
            )
            df_tab = df_tab[mask]
        # Show key stats
        st.subheader(f"Key Stats - {tab_labels[i]}")
        st.write(f"Total posts: {len(df_tab)}")
        # Top tags/keywords/entities/repos
        st.markdown("**Top Tags:**")
        tags = trends['top_tags'] if not platform else [t for t in trends['top_tags'] if t[0] in set(tag for tags in df_tab['tags'] for tag in tags)]
        if search_query:
            tags = [t for t in tags if search_query in t[0].lower()]
        show_bar_chart(tags, 'Top Tags', 'Tag', 'Count', top_n)
        show_wordcloud([t[0] for t in tags[:top_n]], 'Tag Word Cloud')
        st.markdown("**Top Keywords:**")
        keywords = trends['top_keywords'] if not platform else [k for k in trends['top_keywords'] if any(k[0] in str(txt).lower() for txt in df_tab['text'])]
        if search_query:
            keywords = [k for k in keywords if search_query in k[0].lower()]
        show_bar_chart(keywords, 'Top Keywords', 'Keyword', 'Score', top_n)
        show_wordcloud([k[0] for k in keywords[:top_n]], 'Keyword Word Cloud')
        st.markdown("**Top Entities:**")
        entities = trends['top_entities'] if not platform else [e for e in trends['top_entities'] if any(e[0] in str(txt) for txt in df_tab['text'])]
        if search_query:
            entities = [e for e in entities if search_query in e[0].lower()]
        show_bar_chart(entities, 'Top Entities', 'Entity', 'Count', top_n)
        st.markdown("**Top Repos:**")
        repos = trends['top_repos'] if not platform else [r for r in trends['top_repos'] if any(r[0] in str(meta.get('repo','')) for meta in df_tab['meta'])]
        if search_query:
            repos = [r for r in repos if search_query in r[0].lower()]
        show_bar_chart(repos, 'Top GitHub Repos', 'Repo', 'Count', top_n)
        # Trend over time
        if 'timestamp' in df_tab.columns:
            show_line_chart(df_tab, search_query, top_n)
        # Top posts/discussions table
        st.subheader("Top Posts/Discussions")
        show_table(df_tab, view_by, top_n, search_query)

from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=300000, limit=None, key="refresh")

