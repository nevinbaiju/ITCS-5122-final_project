import streamlit as st

from pages.predictions import predict_page
from pages.analyze_resale import analyze_resale_value
from config.page_settings import SEGMENTS

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
# st.markdown("<style> ul {display: none;} </style>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Estimate resale value", "Trends in Resale value", "Analyze cars"])

with tab1:
    segment = st.selectbox(
        'Select the segment of cars you want to analyze',
        SEGMENTS, key='1')

    predict_page(segment)

with tab2:
    segment = st.selectbox(
        'Select the segment of cars you want to analyze',
        SEGMENTS, key='2')
    
    analyze_resale_value(segment)

with tab3:
    segment = st.selectbox(
        'Select the segment of cars you want to analyze',
        SEGMENTS, key='3')

