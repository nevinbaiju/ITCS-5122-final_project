import streamlit as st
import  streamlit_toggle as tog
from ._page_config import SEGMENT_MODELS
from ._page_utils import load_data
from ._plot_utils import *

def analyze_resale_value(segment):

    df = load_data(segment)

    head_1, head2 = st.columns(2)

    with head2:
        model_analysis = tog.st_toggle_switch(label="Model level", 
                                                key="Key1", 
                                                default_value=False, 
                                                label_after = False, 
                                                inactive_color = '#D3D3D3', 
                                                active_color="#ff4b4b", 
                                                track_color="#36373f"
                                                )        
    model = ""                                                                                
    with head_1:                                            
        if model_analysis:
            model = st.selectbox(
                'Model',
                SEGMENT_MODELS[segment], key='analyze_resale_model_sel')

    if model_analysis:
        st.header(f'{model.capitalize()} Resale Price analysis')
    else:
        st.header(f'{model.capitalize()} Segment Price analysis')

        fig = plot_segment_volume_altair(df)
        st.write(fig)
    

    section_left, section_right = st.columns(2)

    with section_left:
        if model_analysis:
            st.write(plot_choropleth(df, 'price', model))
            st.write(plot_scatter_with_age(df, model, 'price'))
        else:
            fig = plot_price_with_age(df)
            st.write(fig)
    with section_right:
        if model_analysis:
            st.image(f'img/{model}.png', width=570)
            st.write(plot_scatter_with_age(df, model, 'odometer'))
        else:
            fig = plot_mileage_with_age(df)
            st.write(fig)