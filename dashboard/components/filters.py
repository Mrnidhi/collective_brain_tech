import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def sidebar_filters(df: pd.DataFrame):
    st.sidebar.markdown("---")
    st.sidebar.subheader("Data Filters")
    
    # Platform selection
    platforms = st.sidebar.multiselect(
        "Platforms",
        options=['github', 'stackoverflow', 'reddit'],
        default=['github', 'stackoverflow', 'reddit'],
        format_func=lambda x: {
            'github': '🐙 GitHub',
            'stackoverflow': '💬 Stack Overflow',
            'reddit': '👽 Reddit'
        }[x]
    )
    
    # Date range
    st.sidebar.markdown("##### Time Range")
    
    # Calculate default date range (last 7 days)
    end_date = df['timestamp'].max().date()
    start_date = end_date - timedelta(days=7)
    
    # Date inputs
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start = st.date_input("From", value=start_date, max_value=end_date)
    with col2:
        end = st.date_input("To", value=end_date, min_value=start)
    
    # View options
    st.sidebar.markdown("##### View Options")
    
    # Number of items to show
    top_n = st.sidebar.slider(
        "Items to show",
        min_value=5,
        max_value=50,
        value=10,
        step=5
    )
    
    # Sort options
    view_by = st.sidebar.selectbox(
        "Sort by",
        options=['recent', 'popular', 'trending'],
        format_func=lambda x: {
            'recent': '📅 Most Recent',
            'popular': '🔥 Most Popular',
            'trending': '📈 Trending'
        }[x]
    )
    
    # Apply filters
    mask = (
        df['source'].isin(platforms) &
        (pd.to_datetime(df['timestamp']).dt.date >= start) &
        (pd.to_datetime(df['timestamp']).dt.date <= end)
    )
    filtered_df = df[mask].copy()
    
    # Sort data
    if view_by == 'recent':
        filtered_df = filtered_df.sort_values('timestamp', ascending=False)
    elif view_by == 'popular':
        filtered_df = filtered_df.sort_values('score', ascending=False)
    else:  # trending
        filtered_df = filtered_df.sort_values(['timestamp', 'score'], ascending=[False, False])
    
    return {
        'filtered_df': filtered_df,
        'platforms': platforms,
        'view_by': view_by,
        'top_n': top_n,
        'date_range': (start, end)
    } 