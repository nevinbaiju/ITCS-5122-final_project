import streamlit as st

from pages.predictions import midsize
from config.page_settings import SEGMENTS

st.set_page_config(layout="wide")

tab1, tab2, tab3 = st.tabs(["Estimate resale value", "Trends in Resale value", "Analyze cars"])

with tab1:
    option = st.selectbox(
        'Select the segment of cars you want to analyze',
        SEGMENTS, key='1')

    midsize()

with tab2:
    option = st.selectbox(
        'Select the segment of cars you want to analyze',
        SEGMENTS, key='2')

with tab3:
    option = st.selectbox(
        'Select the segment of cars you want to analyze',
        SEGMENTS, key='3')

