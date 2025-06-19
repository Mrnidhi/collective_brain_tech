import streamlit as st
import pandas as pd

def sidebar_filters(df: pd.DataFrame):
    st.sidebar.header('Filters')
    # Date range filter
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        # Make timestamps timezone-naive for comparison
        if hasattr(df['timestamp'].dt, 'tz') and df['timestamp'].dt.tz is not None:
            df['timestamp'] = df['timestamp'].dt.tz_localize(None)
        min_date, max_date = df['timestamp'].min(), df['timestamp'].max()
        date_range = st.sidebar.date_input('Date range', [min_date, max_date])
        if len(date_range) == 2:
            df = df[(df['timestamp'] >= pd.to_datetime(date_range[0])) & (df['timestamp'] <= pd.to_datetime(date_range[1]))]
    # Platform checkboxes
    platforms = st.sidebar.multiselect('Platforms', ['github', 'stackoverflow', 'reddit'], default=['github', 'stackoverflow', 'reddit'])
    df = df[df['source'].isin(platforms)]
    # View by dropdown
    view_by = st.sidebar.selectbox('View by', ['tags', 'keywords', 'repos', 'entities'], format_func=lambda x: {'tags':'🔧 Tags','keywords':'🏷️ Keywords','repos':'📁 Repos','entities':'🧠 Named Entities'}[x])
    # Top N slider
    top_n = st.sidebar.slider('Top N', 5, 30, 10)
    return {'filtered_df': df, 'platforms': platforms, 'view_by': view_by, 'top_n': top_n} 