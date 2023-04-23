import streamlit as st

from pages.predictions import midsize
from pages.analyze_resale import analyze_resale_value
from config.page_settings import SEGMENTS

st.set_page_config(layout="wide")

tab1, tab2, tab3 = st.tabs(["Estimate resale value", "Trends in Resale value", "Analyze cars"])

with tab1:
    segment = st.selectbox(
        'Select the segment of cars you want to analyze',
        SEGMENTS, key='1')

    midsize(segment)

with tab2:
    segment = st.selectbox(
        'Select the segment of cars you want to analyze',
        SEGMENTS, key='2')
    
    analyze_resale_value(segment)

with tab3:
    segment = st.selectbox(
        'Select the segment of cars you want to analyze',
        SEGMENTS, key='3')

