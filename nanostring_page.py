from pathlib import Path
import streamlit as st

from os import listdir
from os.path import isfile, join
from register_load_widget_state import  persist
import os


def nanostring_page():
    
    #############################################
    # Mouse


    path_mouse = "./data/Nanostring_data/mouse"

    filenames = [f for f in listdir(path_mouse) if isfile(join(path_mouse, f))]
    genepaths = [x.split("_")[2] + "_"+ x.split("_")[3].split(".")[0] for x in filenames]
    genenames = [ x.split("_")[3].split(".")[0] for x in filenames]

    gene2path = dict(zip(genenames, genepaths))

     
    # title = f'<p style="font-size: 28px;text-align: center; font-weight: 900">nCounter immunology panel </p>'
    # st.markdown(title, unsafe_allow_html=True)

    gene_selected = st.selectbox(
        'Genes',
        sorted(genenames),
        0
    )
    

    title = f'<p style="font-size: 22px;text-align: center; color:#00559c; font-weight: 900">nCounter mouse immunology panel </p>'
    c1,c2=st.columns([3,2])
    c1.markdown(title, unsafe_allow_html=True)

    imgfile_mouse = str(Path(path_mouse) / f"Dotplot_Nanostring_{gene2path[gene_selected]}.png")
    st.image(imgfile_mouse)
    
    
  ##################################################
   # TCGA
    
    path_TCGA = "./data/Nanostring_data/TCGA"
    geneUpper = gene_selected.upper()
    imgfile_TCGA = str(Path(path_TCGA) / f"Dotplot_Nanostring_MutationType_{geneUpper}.png")
    
    if os.path.isfile(imgfile_TCGA):
      
        title2 = f'<p style="font-size: 22px;text-align: center; color:#00559c; font-weight: 900">nCounter TCGA immunology panel </p>'
        c3,c4=st.columns([3,2])
        c3.markdown(title2, unsafe_allow_html=True)
        st.image(imgfile_TCGA) 
        