import random
from pathlib import Path

import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

from utils import convert_df_to_csv, img2buf, load_data, violin_plot   #, anova_test
from register_load_widget_state import  persist


def TF_page(path_data):

      
    files = (path_data / "TFrank/within_celltype").iterdir()
    files = [i.name.replace('TFrank_samples_', '') for i in files]
    files = list(filter(lambda x: x != "figure", files))
    celltypeAll = list([i[:-4] for i in files])

    @st.cache
    def load_rootdata(path_data):
        fname = str(
            path_data / "celltype_info.csv")
        df_info = pd.read_csv(fname, index_col=0)
        fname = str(path_data / "TFrank_all_celltypeAll_samples.csv")

        df_ranks_all = pd.read_parquet(path_data/"TFranks_all.parquet.gzip")
        return ((df_info, df_ranks_all))


    cached_data = load_rootdata(path_data)
    df_info = cached_data[0]
    df_ranks_all = cached_data[1]
    tfall = sorted(df_ranks_all.columns[:-2])

    type2ds = {}
    for type in list(df_info.index):
        snames = df_info.loc[type, "sample names"]
        if pd.isna(snames):
            continue
        snames = [x.strip() for x in snames.split(',')]
        type2ds[type] = snames

    
   

    selected = option_menu(None, ["Analysis by TFs (across all cell-types)", "Analysis by TFs (cell-type specific view)", "Analysis by cell-type"],
                        #    icons=["bi bi-grid-3x3", "bi bi-align-end",
                        #           "bi bi-align-bottom"],
                           menu_icon="cast", default_index=0, orientation="horizontal",
                           styles={
        "container": {"padding": "20!important", "background-color": "#eee"},
        "icon": {"color": "orange", "font-size": "18px"},
        "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "--hover-color": "#fafafa"},
        "nav-link-selected": {"background-color": "#80adcc"},
        "separator": "A"
    })

    datafile = ""
   

    if selected == 'Analysis by TFs (across all cell-types)':
        st.info('For each TF, violin plot shows its ranks across cell types. You can select multiple TFs of your interest from TFs list for comparison.')
       

        # if "tfpage_tab1_tf" in st.session_state:
        #     if not set(st.session_state.tfpage_tab1_tf).issubset(set(tfall)): 
        #          st.session_state.tfpage_tab1_tf = list(set(st.session_state.tfpage_tab1_tf) & set(tfall))

        
        TFs_selected = st.multiselect('TFs', tfall, default=tfall[0],  key=persist("tfpage_tab1_tf"))
        _, c, _ = st.columns([1,9,1])
        for tf in TFs_selected:
            df_ranks = df_ranks_all.loc[:, [tf, "Celltype", "Dataset"]]
            patients = sorted(set(df_ranks["Dataset"]))
            for p in patients:
                df_ranks_p = df_ranks.loc[df_ranks['Dataset']==p,]
                fig = violin_plot(tf + " of " + p, df_ranks_p, "Celltype",tf, 25, 3)
                c.pyplot(fig)
        s_TFs = "_".join(TFs_selected)
        s_TFs if len(s_TFs) <= 100 else s_TFs[:100]
        datafile_out = f"TFranks--{s_TFs}.csv"

       
        df_data = df_ranks_all[['Celltype', 'Dataset'] + TFs_selected]
        c_checkbox, _, c_dwdata = st.columns([3, 9, 3])
        cb = c_checkbox.checkbox("Show data", key="TFrank")


        btn_data = c_dwdata.download_button(
            label='📩 '+"Download Data",
            data=convert_df_to_csv(df_data),
            file_name=datafile_out,
            mime="text/csv",
            key='download-csv',
            disabled=not cb
        )

        if cb:
            st.dataframe(df_data.style.format(precision=0), use_container_width=True)

    elif selected == "Analysis by TFs (cell-type specific view)":
        c3_1, c3_2 = st.columns(2)

       
        # if "tfpage_tab3_tf" in st.session_state:
        #     if not set(st.session_state.tfpage_tab3_tf).issubset(set(tfall)): 
        #          st.session_state.tfpage_tab3_tf = list(set(st.session_state.tfpage_tab3_tf) & set(tfall))

        
        tf3_selected = st.multiselect('TFs', tfall, default=tfall[0], key=persist("tfpage_tab3_tf"))

        type3_selected = st.multiselect(f'Cell types', celltypeAll, default=celltypeAll[0],  key=persist("tfpage_tab3_type"),
                                 format_func=lambda x: x + " (Num of patients: " + str(len(type2ds[x])) + ")")

        _, c, _ = st.columns([1,9,1])
        for tf in tf3_selected:
            for type in type3_selected:
                df_ranks_2 = df_ranks_all.loc[df_ranks_all['Celltype']==type, [tf, "Dataset"]]
                # group_order_donor = type2ds[type]
                # pvalue = anova_test(df_ranks_2, tf)
                fig = violin_plot(f"{tf} in {type}", df_ranks_2, "Dataset", tf, 25,5)
                c.pyplot(fig)

        s3_TFs = "_".join(tf3_selected)
        s3_types = "_".join(type3_selected)
        datafile_out = f"TFranks--{s3_TFs}--{s3_types}.csv"

        
        df_data = df_ranks_all.loc[df_ranks_all["Celltype"].isin(type3_selected), ['Celltype', 'Dataset'] + tf3_selected]
        c_checkbox, _, c_dwdata = st.columns([3, 9, 3])
        cb = c_checkbox.checkbox("Show data", key="TFrank")

        btn_data = c_dwdata.download_button(
            label='📩 '+"Download Data",
            data=convert_df_to_csv(df_data),
            file_name=datafile_out,
            mime="text/csv",
            key='download-csv',
            disabled=not cb
        )

        if cb:
            st.dataframe(df_data.style.format(precision=0), use_container_width=True)


    elif selected == 'Analysis by cell-type':

        st.info('For each cell type, check the similarity and difference among samples of each TF rank. Cell types that have only one sample are not included in the dropdown list')

        
        s_celltype = st.selectbox(f'Cell type ({len(celltypeAll)})', celltypeAll,  key=persist("tfpage_tab2_type"),   
                                  format_func=lambda x: x + " (Num of patients: " + str(len(type2ds[x])) + ")")
        
        imgfile = str(
            path_data / f"TFrank/within_celltype/figure/heatmap_TFrank_samples_{s_celltype}.png")
        imgfile_out = f"heatmap_TFrank_within_{s_celltype}.png"

        _, c, _ = st.columns([1,9,1])
        c.image(imgfile)

        datafile = str(
            path_data / f"TFrank/within_celltype/TFrank_samples_{s_celltype}.csv")
        datafile_out = f"TFranks_within_{s_celltype}.csv"

        df_data = load_data(datafile)

        c_checkbox, _, c_dwdata, c_dwimg = st.columns([3, 5, 3, 3])

        cb = c_checkbox.checkbox("Show data", key=imgfile)

        btn_img = c_dwimg.download_button(
            label='📥 '+"Download Image",
            data=img2buf(imgfile),
            file_name=imgfile_out
        )

        btn_data = c_dwdata.download_button(
            label='📩 '+"Download Data",
            data=convert_df_to_csv(df_data),
            file_name=datafile_out,
            mime="text/csv",
            key='download-csv',
            disabled=not cb
        )

        if cb:
            st.dataframe(df_data.style.format(precision=0), use_container_width=True)