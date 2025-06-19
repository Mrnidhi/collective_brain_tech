import streamlit as st
import pandas as pd
import json
import os

@st.cache_data
def load_fetched_data():
    # Look for file in parent directory
    file_path = '../fetched_data.json'
    if not os.path.exists(file_path):
        file_path = 'fetched_data.json'  # Fallback to current directory
    df = pd.read_json(file_path)
    return df

@st.cache_data
def load_trends():
    # Look for file in parent directory
    file_path = '../trends.json'
    if not os.path.exists(file_path):
        file_path = 'trends.json'  # Fallback to current directory
    with open(file_path) as f:
        trends = json.load(f)
    return trends 