
import streamlit as st

from streamlit_option_menu import option_menu

# from main_page import main_page

from register_load_widget_state import  load_widget_state

from pathlib import Path

# from correlation_page import correlation_page
# from data_page import data_page
# from TF_page import TF_page
from nanostring_page import nanostring_page
from main_page import main_page

from PIL import Image
Image.MAX_IMAGE_PIXELS = None

# from utils import set_page_container_style
# def set_page_container_style(prcnt_width: int = 75):
max_width_str = f"max-width: {85}%;"
st.markdown(f"""
            <style> 
            
            .appview-container .main .block-container{{{max_width_str}}}
            </style>    
            """,
            unsafe_allow_html=True,
            )

st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}  
    footer  {visibility: hidden;}  
    div.css-1vq4p4l.e1fqkh3o4{padding: 2rem 1rem 1.5rem;}
    div.block-container{padding-top:3rem;}
    </style>    
    """,
    unsafe_allow_html=True,
    )

# st.write('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
# st.write('<style>div.css-1vq4p4l.e1fqkh3o4{padding: 4rem 1rem 1.5rem;}</style>', unsafe_allow_html=True)

# st.markdown(page_style, unsafe_allow_html=True)



# with st.sidebar:
#     choose1 = option_menu("Testing set", ["CLR1norm","CLR2norm"],
#                          icons=['clipboard-data',
#                                 'lightning-charge'],
#                          menu_icon="app-indicator", default_index=0,
#                          styles={
#         "container": {"padding": "5!important", "background-color": "#fafafa"},
#         "icon": {"color": "orange", "font-size": "22px"},
#         "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
#         "nav-link-selected": {"background-color": "#02ab21"},
#     }
#     )
# cleaned_setting = choose1.replace(" ","_")
# load_widget_state()
# main_page(choose1, cleaned_setting)

load_widget_state()
path_data = Path(f"./data/CLR1norm") 

with st.sidebar:
    
    choose1 = option_menu("Menu", ["nCounter immunology panel","Human CITE-seq data"],
                        icons=['clipboard-data',
                                'lightning-charge'],
                        menu_icon="arrow-return-right", default_index=0,
                        styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "18px"},
        "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "orange"},
    }
    )






if choose1 == "nCounter immunology panel":
    nanostring_page()


elif choose1 == "Human CITE-seq data":
    main_page(choose1)



