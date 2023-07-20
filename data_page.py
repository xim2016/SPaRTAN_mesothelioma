from pathlib import Path
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from utils import hide_table_index, hide_dataframe_index
import os
from PIL import Image



path = "./data"
protein_names = pd.read_csv(Path(path)/"protein_names.csv", index_col=0).T
celltype_names = pd.read_csv(Path(path)/"celltype_names.csv", index_col=0).T
dataset_info = pd.read_csv(Path(path)/"dataset_info.csv", index_col=0)
celltypes = celltype_names.iloc[0,:].tolist()
cell_count = pd.read_csv(Path(path)/"cell_count.csv")
cell_count.index.name = None

# get the gene names of mRNA violin plot
path_mRNA = ("./data/mRNA_data/violinPlot")

gene_list = sorted([x.split(".")[0][11:] for x in os.listdir(path_mRNA)])


def data_page(path_data):

    path_data = Path(f"./data/CLR1norm") 
    spartan_data = pd.read_csv(
        path_data/"celltype_info.csv", index_col=0)

    spartan_data.dropna(inplace=True)
    # if "RNArate" in spartan_data.columns:
    #     spartan_data['RNArate'] = spartan_data['RNArate'] .round(
    #         decimals=1).astype(object)
    

    selected = option_menu(None, ["Metadata", "Cell-type Overview", "Protein", "mRNA", "inferCNV","PROGENy pathway"],
                        #    icons=["clipboard", "hdd-fill",
                        #           "hdd-stack", "clipboard-plus", 'bar-chart-line', "bi bi-align-end"],
                           menu_icon="cast", default_index=0, orientation="horizontal",
                           styles={
        "container": {"padding": "5!important", "background-color": "#eee"},
        "icon": {"color": "orange", "font-size": "18px"},
        "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "--hover-color": "#fafafa"},
        "nav-link-selected": {"background-color": "#FD5816"},
        # "separator":"."
    })

    if selected == "Metadata":

        hide_dataframe_index()
        # st.write("Donors (4):")
        st.markdown('''###### Patients (3):''')
        st.dataframe(dataset_info)

        hide_table_index()
        # st.write("Cell types (24):")
        st.markdown('''###### Cell types (13):''')
        st.table(celltype_names)

        # write_text("Proteins (52):", fontsize=10)
        # st.write("")
        st.markdown('''###### Proteins (52):''')
        st.table(protein_names)

        # show_dataframe_index()
        st.markdown('''###### Cell count:''')
        st.table(cell_count)
    
    elif selected ==  "Cell-type Overview":
        path = "./data"
        imgfile = str(Path(path) / f"Mesothelioma_scRNAseq_CelltypeAssignment_3Patients.png")

        st.image(imgfile)

    elif selected == "Protein":

        selected_sub = option_menu(None, ["by Protein", "by Patient"],
                                   #    icons=["clipboard", "hdd-fill", "hdd-stack", "clipboard-plus"],
                                   menu_icon="cast", default_index=0, orientation="horizontal",
                                   styles={
            "container": {"padding": "5!important", "background-color": "#eee"},
            # "icon": {"color": "orange", "font-size": "14px"},
            "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "--hover-color": "#fafafa"},
            "nav-link-selected": {"background-color": "#80adcc"},
            # "separator":"."
        }
        )
        # 858d83
        if selected_sub == "by Protein":

            path_ADT = Path("./data/ADT_data/violinPlot")
            _, c1, _ = st.columns([1,9,1])
            pro_selected = c1.selectbox(
                'Protein',
                list(protein_names.loc['x', :]),
                0
            )

            imgfile = str(path_ADT / f"ViolinPlot_ByCLR1_{pro_selected}-TotalSeqC.png"
                          )

            c1.image(imgfile)

        elif selected_sub == "by Patient":

            path_ADT = Path("./data/ADT_data/heatmap")
            # c3,c4 = st.columns(2)
            pat_selected = st.selectbox(
                'Patient',
                dataset_info.index.tolist(),
                0
            )

            imgfile = str(path_ADT / f"{pat_selected} CLR margin=2 ADT mean.png"
                          )

            st.image(imgfile)

    elif selected == "mRNA":

        selected_sub2 = option_menu(None, ["Violin plot", "Heatmap"],
                                    #    icons=["clipboard", "hdd-fill", "hdd-stack", "clipboard-plus"],
                                    menu_icon="cast", default_index=0, orientation="horizontal",
                                    styles={
            "container": {"padding": "5!important", "background-color": "#eee"},
            # "icon": {"color": "orange", "font-size": "14px"},
            "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "--hover-color": "#fafafa"},
            "nav-link-selected": {"background-color": "#80adcc"},
            # "separator":"."
        }
        )
        # 858d83
        if selected_sub2 == "Violin plot":

            path_gene = Path("./data/mRNA_data/violinPlot")
            _,c1, _= st.columns([1,9,1])
            gene_selected = c1.selectbox(
                'Gene',
                gene_list,
                0
            )

            imgfile = str(path_gene / f"ViolinPlot_{gene_selected}.png"
                          )

            c1.image(imgfile)
        elif selected_sub2 == "Heatmap":
            path_plot = Path("./data/mRNA_data/heatmap")

            c3, c4 = st.columns(2)
            list3 = ["Cytoskeleton",  "CytokineReceptor", "IRFGene",
                     "InterestingGene", "ImmuneGene", "ImmuneCheckpoint"]
            list4 = ["AllCellType", "ImmuneCellType", "NonImmuneCellType"]
            sel_3 = c3.selectbox(
                'Gene type',
                list3,
                0
            )
            sel_4 = c4.selectbox(
                'Cell type',
                list4,
                0
            )

            imgfile = str(
                path_plot / f"OutComplexHeatmap_Mesothelioma_{sel_3}_{sel_4}_SCTNormalExp_Reorder.pdf")

            # image = Image.open(imgfile)
            # show_pdf(imgfile)
            # st.image(image)


    elif selected == "inferCNV":

        # title = f'<p style="font-size: 28px;text-align: center; font-weight: 900">InferCNV analysis</p>'
        # st.markdown(title, unsafe_allow_html=True)

        st.info('InferCNV analysis explores tumor single cell RNA-Seq data to identify evidence for large-scale chromosomal copy number variations, such as gains or deletions of entire chromosomes or large segments of chromosomes.')
        selected_sub3 = option_menu(None, ["By cell-type", "By patient"],
                                    #    icons=["clipboard", "hdd-fill", "hdd-stack", "clipboard-plus"],
                                    menu_icon="cast", default_index=0, orientation="horizontal",
                                    styles={
            "container": {"padding": "5!important", "background-color": "#eee"},
            # "icon": {"color": "orange", "font-size": "14px"},
            "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "--hover-color": "#fafafa"},
            "nav-link-selected": {"background-color": "#80adcc"},
            # "separator":"."
        }
        )
        # 858d83
        if selected_sub3 == "By cell-type":

            path_violin = Path("./data/inferCNV/violinPlot")

            # c1, c2 = st.columns([21,20])
            # type_selected = c1.selectbox(
            #     'Cell types',
            #     celltypes,
            #     0
            # )
            types = ["LungEpithelium","MalignantEpithelial","ProliferatingCell"]
            c1,c2=st.columns([2,2])

            imgfile1 = str(path_violin/ f"ViolinPlot_InferCNV_{types[0]}.png")
            imgfile2 = str(path_violin/ f"ViolinPlot_InferCNV_{types[1]}.png")
            imgfile3 = str(path_violin/ f"ViolinPlot_InferCNV_{types[2]}.png")              
            # c1.markdown(f'''   #### {types[0]}''')
            # c1.text("    ")
           
            title = f'<p style="font-size: 20px;text-align: center; font-weight: 600">{types[0]} </p>'
            c1.markdown(title, unsafe_allow_html=True)
            # c1.write(f"#### {types[0]}")
            c1.image(imgfile1)
            title = f'<p style="font-size: 20px;text-align: center; font-weight: 600">{types[1]}</p>'
            c2.markdown(title, unsafe_allow_html=True)
            c2.image(imgfile2)
            c1.write("#")
            title = f'<p style="font-size: 20px;text-align: center; font-weight: 600">{types[2]}</p>'
            c1.markdown(title, unsafe_allow_html=True)
            c1.image(imgfile3)

        elif selected_sub3 == "By patient":
            path_heatmap = Path("./data/inferCNV/heatmap")
            
            type_selected = st.selectbox(
                'Patients',
                ["Patient 1", "Patient 2", "Patient 3"],
                0
            )

            p_number = type_selected.split(" ")[1]

            imgfile = str(path_heatmap / f"InfercnvHeatmap_NewCellTypebCutoff0.001_Pt{p_number}.png")
                          

            st.image(imgfile)
    elif selected == "PROGENy pathway":

        title = f'<p style="font-size: 26px;text-align: center; font-weight: 800">PROGENy pathway</p>'
        st.markdown(title, unsafe_allow_html=True)

        st.info("PROGENy is resource that leverages a large compendium of publicly available signaling perturbation experiments to yield a common core of pathway responsive genes for human and mouse.")

        path_violin = Path("./data/PROGENy/violinPlot")

        _,c1, _ = st.columns([2,5,2])
        type_selected = c1.selectbox(
            'Cell types',
            celltypes,
            0
        )
        
        imgfile = str(path_violin/ f"ViolinPlot_PROGENyPathwayActivity_IndividualPt_{type_selected}.png")
                        
        c1.image(imgfile)

        # elif selected_sub4 == "Heatmap":
        #     path_heatmap = Path("./data/inferCNV/heatmap")
            
        #     c3, c4 = st.columns([21,20])
        #     type_selected = c3.selectbox(
        #         'Cell types',
        #         celltypes,
        #         0
        #     )
          
        #     imgfile = str(path_heatmap/ f"ComplexHeatmapCorrel_PathwayAct_CytoskeletonExp_{type_selected}.png")
                         
        #     st.image(imgfile)
