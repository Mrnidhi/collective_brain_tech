import streamlit as st
import pandas as pd
import json

@st.cache_data
def load_fetched_data():
    df = pd.read_json('fetched_data.json')
    return df

@st.cache_data
def load_trends():
    with open('trends.json') as f:
        trends = json.load(f)
    return trends 