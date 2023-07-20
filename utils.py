from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import seaborn as sns
# from statsmodels.formula.api import ols 
# import statsmodels.api as sm


# def set_page_container_style(prcnt_width: int = 75):
#     max_width_str = f"max-width: {prcnt_width}%;"
#     st.markdown(f"""
#                 <style> 
                
#                 .appview-container .main .block-container{{{max_width_str}}}
#                 </style>    
#                 """,
#                 unsafe_allow_html=True,
#                 )

def img2buf(img_path: str):
    img = Image.open(img_path)
    buf = BytesIO()
    img.save(buf, format="PNG")
    bufval = buf.getvalue()
    return (bufval)


@st.cache
def load_data(datafile):
    df = pd.read_csv(datafile, index_col=0)
    return df


@st.cache
def convert_df_to_csv(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

# def anova_test(df, tf):
#     if len(set(df['Dataset']))== 1: return(pd.NA)
#     model = ols(f'{tf} ~ C(Dataset)', data=df).fit()
#     anova_table = sm.stats.anova_lm(model, typ=2)
#     pvalue = anova_table.iloc[0,3]
#     return(pvalue)    


def violin_plot(title, data_group, x, y, width, height, pvalue=pd.NA):
    fig, ax = plt.subplots(figsize=(width, height))
    if x=="Celltype":
        sns.violinplot(x=x, y=y, data=data_group, ax=ax, order=[ "Bcell","CD4Tcell","CD8Tcell","cDC","M2Macrophage","Macrophage","NKcell","NKTcell", "Endothelium","Fibroblast","LungEpithelium","MalignantEpithelial", "ProliferatingCell"])
    else:
        sns.violinplot(x=x, y=y, data=data_group, ax=ax)
    if pd.isnull(pvalue):
        ax.set_title("{} ".format(title),  fontsize=26)
    else:
        ax.set_title("{}    Anova test pvalue = {:.2E}".format(title, pvalue),  fontsize=26)
    ax.set_ylabel("TF rank", fontsize=20)
    ax.set_xlabel("")
    plt.xticks(rotation=45, fontsize=16)
    plt.setp(ax.xaxis.get_majorticklabels(), ha='right')
    return (fig)

def write_text(text,fontsize=10, color="blue"):
    st.markdown(f'<h1 style=f"color:{color};font-size:10px;">{text}</h1>', unsafe_allow_html=True)


def hide_table_index():
    hide_table_row_index = """
                    <style>
                    thead tr th:first-child {display:none}
                    tbody th {display:none}
                    </style>
                    """

    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)


def hide_dataframe_index():
    hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """

    # Inject CSS with Markdown
    st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)

def show_dataframe_index():
    show_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:block}
            .blank {display:block}
            </style>
            """

    # Inject CSS with Markdown
    st.markdown(show_dataframe_row_index, unsafe_allow_html=True)