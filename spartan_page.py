from pathlib import Path
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

import os

from correlation_page import correlation_page
from TF_page import TF_page


path_data = Path(f"./data/CLR1norm") 

def spartan_page(setting):

    choose_spartan = option_menu("", ["Data overview", "TF activity analysis", "Protein-TF correlations"],
                                icons=['clipboard-data',
                                        'lightning-charge', 'bar-chart-line'],
                                menu_icon="arrow-return-right", default_index=0, orientation="horizontal",
                                styles={
                "container": {"padding": "5!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "18px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#FD5816"},
            }
            )
        

    if choose_spartan == "Protein-TF correlations":
        
        correlation_page(path_data)

    elif choose_spartan == "TF activity analysis":
        
        TF_page(path_data)

    elif choose_spartan == "Data overview":

        
        spartan_data = pd.read_csv(path_data/"celltype_info.csv", index_col=0)

        spartan_data.dropna(inplace=True)
        
        st.dataframe(spartan_data.style.format(
            {'RNArate': '{:.2f}', 'number of genes': '{:.0f}', 'number of TFs': '{:.0f}', 'number of proteins': '{:.0f}' }), use_container_width=True)
   
    
   

