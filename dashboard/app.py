import streamlit as st
import os
import subprocess
from components.load_data import load_fetched_data, load_trends
from components.filters import sidebar_filters
from components.charts import show_bar_chart, show_wordcloud, show_table, show_line_chart
from components.alerts import show_alerts

# Page config
st.set_page_config(
    page_title="Tech Trends Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for GitHub-like styling
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .st-emotion-cache-16txtl3 h1 {
        font-weight: 600;
        font-size: 32px;
        margin-bottom: 16px;
    }
    .st-emotion-cache-16txtl3 h2 {
        font-weight: 600;
        font-size: 24px;
        margin-top: 24px;
        margin-bottom: 16px;
    }
    .st-emotion-cache-16txtl3 h3 {
        font-weight: 600;
        font-size: 20px;
        margin-top: 24px;
        margin-bottom: 16px;
    }
    .stButton button {
        background-color: #2ea44f;
        color: white;
        border: none;
        padding: 6px 16px;
        border-radius: 6px;
        font-weight: 500;
    }
    .stButton button:hover {
        background-color: #2c974b;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        background-color: #f6f8fa;
        border-radius: 6px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2ea44f !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🧠 Tech Trends Dashboard")

# Sidebar
with st.sidebar:
    st.subheader("Dashboard Controls")
    
    # Refresh button
    if st.button('🔄 Refresh Data'):
        with st.spinner('Refreshing data...'):
            if os.path.exists('run_fetch.py'):
                subprocess.run(['python', 'run_fetch.py'])
            if os.path.exists('trend_analysis/run_trends.py'):
                subprocess.run(['python', 'trend_analysis/run_trends.py'])
            st.cache_data.clear()
            st.rerun()
    
    # Show critical alerts only
    show_alerts(location='sidebar', max_alerts=3)

# Data loading
fetched_data_path = "../fetched_data.json" if os.path.exists("../fetched_data.json") else "fetched_data.json"
trends_path = "../trends.json" if os.path.exists("../trends.json") else "trends.json"

if not (os.path.exists(fetched_data_path) and os.path.exists(trends_path)):
    st.warning("⚠️ Data files not found. Please run the data pipeline first.")
    st.code("""
# Generate data by running:
python run_fetch.py
python trend_analysis/run_trends.py
    """)
    st.stop()

data = load_fetched_data()
trends = load_trends()

# Filters
filters = sidebar_filters(data)
df = filters['filtered_df']
platforms = filters['platforms']
view_by = filters['view_by']
top_n = filters['top_n']

# Search
search_query = st.text_input('🔍 Search topics, tags, or keywords').strip().lower()

# Platform tabs
tab_labels = ["📊 Overview", "🐙 GitHub", "💬 Stack Overflow", "👽 Reddit"]
tabs = st.tabs(tab_labels)
platform_map = {
    "📊 Overview": None,
    "🐙 GitHub": "github",
    "💬 Stack Overflow": "stackoverflow",
    "👽 Reddit": "reddit"
}

for i, tab in enumerate(tabs):
    with tab:
        platform = platform_map[tab_labels[i]]
        df_tab = df[df['source'] == platform] if platform else df
        
        if df_tab.empty:
            st.info('No data available for the selected filters.')
            continue
            
        # Apply search filter
        if search_query:
            mask = (
                df_tab['text'].str.lower().str.contains(search_query) |
                df_tab['tags'].apply(lambda tags: any(search_query in str(tag).lower() for tag in tags))
            )
            df_tab = df_tab[mask]
        
        # Platform stats
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader(f"Top Topics - {tab_labels[i]}")
            tags = trends['top_tags'] if not platform else [t for t in trends['top_tags'] if t[0] in set(tag for tags in df_tab['tags'] for tag in tags)]
            if search_query:
                tags = [t for t in tags if search_query in t[0].lower()]
            show_bar_chart(tags, 'Most Discussed Topics', 'Topic', 'Mentions', top_n)
        
        with col2:
            st.subheader("Topic Cloud")
            show_wordcloud([t[0] for t in tags[:top_n]], '')
        
        # Trend analysis
        st.subheader("Trend Analysis")
        if 'timestamp' in df_tab.columns:
            show_line_chart(df_tab, search_query, min(5, top_n))
        
        # Recent discussions
        st.subheader("Recent Discussions")
        show_table(df_tab, view_by, min(10, top_n), search_query)

# Optional auto-refresh
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=300000, limit=None, key="refresh")
except ImportError:
    pass

