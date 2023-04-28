import streamlit as st
from ._page_utils import make_prediction
from ._page_config import SEGMENT_MODELS

def midsize(segment):

    col1, col2 = st.columns(2)
    pred_data = {}
    with col1:

        pred_data['odometer'] = st.slider('Odometer', 0, 300000, 1000)
        pred_data['year'] = st.selectbox(
        'Model Year',
        tuple(range(2023, 1989, -1)))

        pred_data['condition'] = st.selectbox(
        'Condition',
        ('good', 'excellent', 'like new', 'fair', 'salvage', 'new'))

        pred_data['model'] = st.selectbox(
        'Condition',
        SEGMENT_MODELS[segment])

    with col2:

        pred_data['transmission'] = st.selectbox(
        'Transmission',
        ('automatic', 'manual'))

        pred_data['drive'] = st.selectbox(
        'Drive',
        ('FWD', 'AWD', 'RWD'))

        pred_data['paint_color'] = st.selectbox(
        'Paint Color',
        ('white', 'silver', 'red', 'green', 
        'blue', 'custom', 'grey', 'black', 
        'brown', 'yellow', 'purple', 'orange'))

    pred = str(int(make_prediction(pred_data, segment)[0])) + "$"
    st.header(f"Your car would be worth: {pred}")

    


    
