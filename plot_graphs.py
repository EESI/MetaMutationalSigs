import pandas as pd 
import numpy as np
import math
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.offline import plot
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.spatial.distance import squareform, pdist
import plotly.express as px
import sys, distutils, os

np.random.seed(1234)

def make_piecharts(data_df, n_rows, n_cols, fig_title):
    specs_list = []
    subplot_coordinate = []
    for x in range(n_rows):
        temp_spec_list = []
        for  y in range(n_cols):
            temp_spec_list.append({"type": "bar"})
            subplot_coordinate.append([x+1, y+1])
        specs_list.append(temp_spec_list)
    fig = make_subplots(rows=n_rows, cols=n_cols, specs=specs_list, subplot_titles= list(data_df["sample"]))
    for i in range(data_df.shape[0]):
        df = pd.DataFrame(data_df.iloc[i,1:])
        sample_name = data_df.iloc[i,:][0]
        df.rename( columns={i : sample_name}, inplace = True)
        fig.add_trace(go.Bar(x=list(df[sample_name].index), y= df[sample_name].values), subplot_coordinate[i][0] , subplot_coordinate[i][1] )
    fig_width = data_df.shape[0] * 500
    fig_height = 500
    fig.update_layout(width = fig_width, height = fig_height, title_text=fig_title, showlegend=False)
    return fig


def add_scatterplot_layer(data_df, _color , fig ): 
    try:
        data_df["sample"] = [ i.split("_")[0].split(".")[0] for i in data_df["sample"]]
    except:
        pass
    for i in range(len(data_df)):
        fig.add_trace(go.Scatter( name = data_df.iloc[i]["sample"] , legendgroup=data_df.iloc[i]["sample"] ,  marker=dict(color= _color), x = data_df.columns[1:], y = data_df.iloc[i, 1:], mode='markers') )

r_output_file_dir = sys.argv[1] + "/MetaMutationalResults"
# r_output_file_dir = "MetaMutationalResults"

def run_legacy(sigfit = True, sigflow = True, deconstructSigs= True, mutationalPattern = True):

    try:
        legacy_df_list = []
        legacy_df_name_list = []
        if sigflow:
            sigflow_legacy_exposure_df = pd.read_csv(r_output_file_dir + "/sigflow/legacy_fitting_relative_exposure.csv")
            pie_chart_rows = math.ceil(sigflow_legacy_exposure_df.shape[0] / 3) 
            pie_chart_cols = 3
            rows = math.ceil(sigflow_legacy_exposure_df.shape[0] / 6)
            columns = 6

            sigflow_legacy_exposure_df_fig = make_piecharts(sigflow_legacy_exposure_df, pie_chart_rows, pie_chart_cols, "COSMIC V2 'Legacy' SBS exposures data Sigflow")    
            legacy_df_list.append(sigflow_legacy_exposure_df.sort_values(by=["sample"]))
            legacy_df_name_list.append("sigflow")
        if mutationalPattern:
            mutationalPatterns_legacy_exposure_df = pd.read_csv(r_output_file_dir + "/mutational_patterns_results/legacy_sample_exposures.csv")
            mutationalPatterns_legacy_exposure_df = mutationalPatterns_legacy_exposure_df.rename(columns={"Unnamed: 0": "sample"})
            mutationalPatterns_legacy_exposure_df.set_index("sample", inplace = True)
            mutationalPatterns_legacy_exposure_df = mutationalPatterns_legacy_exposure_df.div(mutationalPatterns_legacy_exposure_df.sum(axis=1), axis=0)
            mutationalPatterns_legacy_exposure_df.reset_index(inplace= True)
            pie_chart_rows = math.ceil(mutationalPatterns_legacy_exposure_df.shape[0] / 3) 
            pie_chart_cols = 3
            rows = math.ceil(mutationalPatterns_legacy_exposure_df.shape[0] / 6)
            columns = 6

            mutationalPatterns_strict_legacy_exposure_df = pd.read_csv(r_output_file_dir + "/mutational_patterns_results/legacy_strict_sample_exposures.csv")
            mutationalPatterns_strict_legacy_exposure_df = mutationalPatterns_strict_legacy_exposure_df.rename(columns={"Unnamed: 0": "sample"})
            mutationalPatterns_strict_legacy_exposure_df.set_index("sample", inplace = True)
            mutationalPatterns_strict_legacy_exposure_df = mutationalPatterns_strict_legacy_exposure_df.div(mutationalPatterns_strict_legacy_exposure_df.sum(axis=1), axis=0)
            mutationalPatterns_strict_legacy_exposure_df.reset_index(inplace= True)

            mutationalPatterns_legacy_fig = make_piecharts(mutationalPatterns_legacy_exposure_df, pie_chart_rows, pie_chart_cols, "COSMIC V2 'Legacy' SBS exposures  data MutationalPatterns")    
            mutationalPatterns_strict_legacy_fig = make_piecharts(mutationalPatterns_strict_legacy_exposure_df, pie_chart_rows, pie_chart_cols, "COSMIC V2 'Legacy' SBS exposures data MutationalPatterns Strict")                
            legacy_df_list.append(mutationalPatterns_legacy_exposure_df.sort_values(by=["sample"]))
            legacy_df_name_list.append("mutationalPatterns")
            legacy_df_list.append(mutationalPatterns_strict_legacy_exposure_df.sort_values(by=["sample"]))
            legacy_df_name_list.append("mutationalPatterns_strict")
        if deconstructSigs:
            deconstructSigs_legacy_exposure_df = pd.read_csv(r_output_file_dir + "/deconstructsigs_results/legacy_sample_exposures.csv")
            deconstructSigs_legacy_exposure_df.rename( columns = {"Unnamed: 0": "sample"}, inplace= True)
            pie_chart_rows = math.ceil(deconstructSigs_legacy_exposure_df.shape[0] / 3) 
            pie_chart_cols = 3
            rows = math.ceil(deconstructSigs_legacy_exposure_df.shape[0] / 6)
            columns = 6
            
            deconstructSigs_legacy_exposure_df_fig = make_piecharts(deconstructSigs_legacy_exposure_df, pie_chart_rows, pie_chart_cols, "COSMIC V2 'Legacy' SBS exposures data DeconstructSigs")    

            legacy_df_list.append(deconstructSigs_legacy_exposure_df.sort_values(by=["sample"]))
            legacy_df_name_list.append("deconstructSigs")
        if sigfit:
            sigfit_legacy_exposure_df = pd.read_csv(r_output_file_dir + "/sigfit_results/legacy_sample_exposures.csv")
            sigfit_legacy_exposure_df.rename(columns={"Unnamed: 0": "sample" }, inplace= True)
            sigfit_legacy_exposure_df.columns = ["sample"] +  [ "COSMIC_" + i.split(".")[-1] for i in sigfit_legacy_exposure_df.columns[1:]]
            pie_chart_rows = math.ceil(sigfit_legacy_exposure_df.shape[0] / 3) 
            pie_chart_cols = 3
            rows = math.ceil(sigfit_legacy_exposure_df.shape[0] / 6)
            columns = 6

            sigfit_legacy_exposure_df_fig = make_piecharts(sigfit_legacy_exposure_df, pie_chart_rows, pie_chart_cols, "COSMIC V2 'Legacy' SBS exposures  data Sigfit")    
            legacy_df_list.append(sigfit_legacy_exposure_df.sort_values(by=["sample"]))
            legacy_df_name_list.append("sigfit")

        with open(r_output_file_dir + '/legacy_bar_charts.html', 'a') as f:
            if sigflow:
                f.write(sigflow_legacy_exposure_df_fig.to_html(full_html=False, include_plotlyjs='cdn'))
            if mutationalPattern:
                f.write(mutationalPatterns_legacy_fig.to_html(full_html=False, include_plotlyjs='cdn'))
                f.write(mutationalPatterns_strict_legacy_fig.to_html(full_html=False, include_plotlyjs='cdn'))
            if sigfit:
                f.write(sigfit_legacy_exposure_df_fig.to_html(full_html=False, include_plotlyjs='cdn'))
            if deconstructSigs:
                f.write(deconstructSigs_legacy_exposure_df_fig.to_html(full_html=False, include_plotlyjs='cdn'))
        

        fig = plt.figure(figsize=( 50, 10 ))

        for i in range(len(legacy_df_list)):
            sns.set(font_scale=1.3)
            df = legacy_df_list[i]
            ax = fig.add_subplot(rows, columns, i+1)    
            sns.heatmap(df.set_index("sample") , cmap="YlGnBu" , xticklabels = True, yticklabels= True)
            sns.set(rc={'figure.figsize':(10 , 10)})
            plt.tight_layout()
            plt.title("Heatmap legacy SBS " + legacy_df_name_list[i] )
        
        plt.savefig(r_output_file_dir + "/Heatmap_exposures_all_sigs_legacy.svg", bbox_inches='tight')
        plt.savefig(r_output_file_dir + "/Heatmap_exposures_all_sigs_legacy.png", bbox_inches='tight')
        
        distance_df_list = []
        sample_name_df = list(legacy_df_list[0]["sample"])

        for i in range(legacy_df_list[0].shape[0]):
            temp_df = []
            for index , j in enumerate(legacy_df_list):
                j.iloc[i,0] = legacy_df_name_list[index]
                temp_df.append(list(j.iloc[i,:]))
            _df = pd.DataFrame(temp_df, columns = legacy_df_list[0].columns)
            _df.fillna(0, inplace = True)
            distance_df_list.append(_df)
        fig = plt.figure(figsize=(40  , 8 ))
        sns.set(font_scale=1.7)
        
        for i in range(len(distance_df_list)):
            df = distance_df_list[i]
            df__ = pd.DataFrame(squareform(pdist(df.iloc[:, 1:] , metric="cosine")), columns=df["sample"], index=df["sample"]).apply(lambda x : (x -1)*-1 )
            ax = fig.add_subplot(rows, columns, i+1)    
            heatmap = sns.heatmap(df__)
            heatmap.set(xlabel=None)
            heatmap.set(ylabel=None)

            plt.tight_layout()
            plt.title("Heatmap legacy SBS " + sample_name_df[i] )
        
        plt.savefig(r_output_file_dir + "/Heatmap_legacy.svg", bbox_inches='tight')
        plt.savefig(r_output_file_dir + "/Heatmap_legacy.png", bbox_inches='tight')


    except Exception as e:
        print("No legacy sigs found", e)    
        pass    

def run_sbs(sigfit = True, sigflow = True, deconstructSigs= True, mutationalPattern = True):
    try:
        sbs_df_list = []    
        sbs_df_name_list = []
        if sigflow:
            sigflow_sbs_exposure_df = pd.read_csv(r_output_file_dir + "/sigflow/SBS_fitting_relative_exposure.csv")
            pie_chart_rows = math.ceil(sigflow_sbs_exposure_df.shape[0] / 3) 
            pie_chart_cols = 3
            rows = math.ceil(sigflow_sbs_exposure_df.shape[0] / 6) 
            columns = 6

            sigflow_sbs_exposure_df_fig = make_piecharts(sigflow_sbs_exposure_df, pie_chart_rows, pie_chart_cols, "COSMIC V3 'SBS' exposures data Sigflow")   
            sbs_df_list.append(sigflow_sbs_exposure_df.sort_values(by=["sample"]))
            sbs_df_name_list.append("sigflow")
        if mutationalPattern:
            mutationalPatterns_sbs_exposure_df = pd.read_csv(r_output_file_dir + "/mutational_patterns_results/sample_exposures.csv")
            mutationalPatterns_sbs_exposure_df = mutationalPatterns_sbs_exposure_df
            mutationalPatterns_sbs_exposure_df.rename(columns={"Unnamed: 0": "sample"}, inplace = True)
            mutationalPatterns_sbs_exposure_df.set_index("sample", inplace = True)
            mutationalPatterns_sbs_exposure_df = mutationalPatterns_sbs_exposure_df.rename(columns={"index": "sample"})
            mutationalPatterns_sbs_exposure_df.sum(axis=1)
            mutationalPatterns_sbs_exposure_df = mutationalPatterns_sbs_exposure_df.div(mutationalPatterns_sbs_exposure_df.sum(axis=1), axis=0)
            mutationalPatterns_sbs_exposure_df.reset_index(inplace= True)

            mutationalPatterns_strict_sbs_exposure_df = pd.read_csv(r_output_file_dir + "/mutational_patterns_results/strict_sample_exposures.csv")
            mutationalPatterns_strict_sbs_exposure_df = mutationalPatterns_strict_sbs_exposure_df
            mutationalPatterns_strict_sbs_exposure_df.rename(columns={"Unnamed: 0": "sample"}, inplace = True)
            mutationalPatterns_strict_sbs_exposure_df.set_index("sample", inplace = True)
            mutationalPatterns_strict_sbs_exposure_df = mutationalPatterns_strict_sbs_exposure_df.rename(columns={"index": "sample"})
            mutationalPatterns_strict_sbs_exposure_df.sum(axis=1)
            mutationalPatterns_strict_sbs_exposure_df.div(mutationalPatterns_strict_sbs_exposure_df.sum(axis=1), axis=0)
            mutationalPatterns_strict_sbs_exposure_df.reset_index(inplace= True)

            pie_chart_rows = math.ceil(mutationalPatterns_sbs_exposure_df.shape[0] / 3) 
            pie_chart_cols = 3
            rows = math.ceil((mutationalPatterns_sbs_exposure_df.shape[0] / 6) )
            columns = 6

            sbs_mutational_patters_fig = make_piecharts(mutationalPatterns_sbs_exposure_df, pie_chart_rows, pie_chart_cols, "COSMIC V3 'SBS' exposures  data MutationalPatterns")    
            sbs_mutational_patters_strict_fig = make_piecharts(mutationalPatterns_strict_sbs_exposure_df, pie_chart_rows, pie_chart_cols, "COSMIC V3 'SBS' exposures data MutationalPatterns Strict")    
            sbs_df_list.append(mutationalPatterns_strict_sbs_exposure_df.sort_values(by=["sample"]))
            sbs_df_name_list.append("mutationalPatterns_strict")
            sbs_df_list.append(mutationalPatterns_sbs_exposure_df.sort_values(by=["sample"]))
            sbs_df_name_list.append("mutationalPatterns")
        if deconstructSigs:
            deconstructSigs_sbs_exposure_df = pd.read_csv(r_output_file_dir + "/deconstructsigs_results/sbs_sample_exposures.csv")
            deconstructSigs_sbs_exposure_df.rename( columns = {"Unnamed: 0": "sample"}, inplace= True)
            pie_chart_rows = math.ceil(deconstructSigs_sbs_exposure_df.shape[0] / 3) 
            pie_chart_cols = 3
            rows = math.ceil(deconstructSigs_sbs_exposure_df.shape[0] / 6) 
            columns = 6

            deconstructSigs_sbs_exposure_df_fig = make_piecharts(deconstructSigs_sbs_exposure_df, pie_chart_rows, pie_chart_cols, "COSMIC V3 'SBS' exposures data DeconstructSigs")    
            sbs_df_list.append(deconstructSigs_sbs_exposure_df.sort_values(by=["sample"]))
            sbs_df_name_list.append("deconstructSigs")            
        if sigfit:
            sigfit_sbs_exposure_df = pd.read_csv(r_output_file_dir + "/sigfit_results/sbs_sample_exposures.csv")
            sigfit_sbs_exposure_df.rename(columns={"Unnamed: 0": "sample" }, inplace= True)
            pie_chart_rows = math.ceil(sigfit_sbs_exposure_df.shape[0] / 3) 
            pie_chart_cols = 3
            rows = math.ceil(sigfit_sbs_exposure_df.shape[0] / 6) 
            columns = 6

            sigfit_sbs_exposure_df_fig = make_piecharts(sigfit_sbs_exposure_df, pie_chart_rows, pie_chart_cols, "COSMIC V3 'SBS' exposures data Sigfit")   
            sbs_df_list.append(sigfit_sbs_exposure_df.sort_values(by=["sample"]))
            sbs_df_name_list.append("sigfit")        
        with open(r_output_file_dir + '/sbs_bar_charts.html', 'a') as f:
            if sigflow:
                f.write(sigflow_sbs_exposure_df_fig.to_html(full_html=False, include_plotlyjs='cdn'))
            if mutationalPattern:
                f.write(sbs_mutational_patters_fig.to_html(full_html=False, include_plotlyjs='cdn'))        
                f.write(sbs_mutational_patters_strict_fig.to_html(full_html=False, include_plotlyjs='cdn'))           
            if sigfit:
                f.write(sigfit_sbs_exposure_df_fig.to_html(full_html=False, include_plotlyjs='cdn'))
            if deconstructSigs:
                f.write(deconstructSigs_sbs_exposure_df_fig.to_html(full_html=False, include_plotlyjs='cdn'))
        
        fig = plt.figure(figsize=(75, 15))
        for i in range(len(sbs_df_list)):  
            sns.set(font_scale=1.4)
            df = sbs_df_list[i].set_index("sample").astype(float)
            ax = fig.add_subplot(rows, columns, i+1)
            sns.heatmap(df , cmap="YlGnBu", xticklabels = True, yticklabels= True )
            sns.set(rc={'figure.figsize':(10, 10)})
            plt.title("Heatmap V3 SBS " + str(sbs_df_name_list[i]))
            plt.tight_layout()

        plt.savefig(r_output_file_dir + "/Heatmap_exposures_all_sigs_SBS.svg", bbox_inches='tight')
        plt.savefig(r_output_file_dir + "/Heatmap_exposures_all_sigs_SBS.png", bbox_inches='tight')
        
        distance_df_list = []
        sample_name_df = list(sbs_df_list[0]["sample"])

        for i in range(sbs_df_list[0].shape[0]):
            temp_df = []
            for index , j in enumerate(sbs_df_list):
                j["sample"] = sbs_df_name_list[index]
                temp_df.append(list(j.iloc[i,:]))
            _df = pd.DataFrame(temp_df, columns = sbs_df_list[0].columns)
            _df.fillna(0, inplace= True)
            distance_df_list.append(_df)

        fig = plt.figure(figsize=(40  , 8 ))
        sns.set(font_scale=1.7)
        for i in range(len(distance_df_list)):  
            df = distance_df_list[i]
            df_ = pd.DataFrame(squareform(pdist(df.iloc[:, 1:] , metric="cosine" ) ), columns=df["sample"], index=df["sample"]).apply(lambda x : (x -1)*-1 )
            ax = fig.add_subplot(rows, columns, i+1)    
            heatmap = sns.heatmap(df_)
            heatmap.set(xlabel=None)
            heatmap.set(ylabel=None)

            plt.tight_layout()
            plt.title("Heatmap V3 SBS " + + sample_name_df[i])
        
        plt.savefig(r_output_file_dir + "/Heatmap_SBS.svg", bbox_inches='tight')
        plt.savefig(r_output_file_dir + "/Heatmap_SBS.png", bbox_inches='tight')


    except Exception as e:
        print("No SBS sigs found", e)    
        pass

def run_id(sigfit = True, sigflow = True, deconstructSigs= True, mutationalPattern = True):
    try:
        id_df_list = []
        id_df_name_list = []
        if sigflow:
            sigflow_id_exposure_df = pd.read_csv(r_output_file_dir + "/sigflow/ID_fitting_relative_exposure.csv")
            pie_chart_rows = math.ceil(sigflow_id_exposure_df.shape[0] / 3) 
            pie_chart_cols = 3
            rows = math.ceil(sigflow_id_exposure_df.shape[0] / 6) 
            columns = 6

            sigflow_id_exposure_df_fig = make_piecharts(sigflow_id_exposure_df, pie_chart_rows, pie_chart_cols, "COSMIC V3 'ID' exposures data Sigflow")   
            id_df_list.append(sigflow_id_exposure_df.sort_values(by=["sample"]))
            id_df_name_list.append("sigflow")
        if mutationalPattern:
            mutationalPatterns_id_exposure_df = pd.read_csv(r_output_file_dir + "/mutational_patterns_results/id_sample_exposures.csv")
            mutationalPatterns_id_exposure_df = mutationalPatterns_id_exposure_df.rename(columns={"Unnamed: 0": "sample"})
            mutationalPatterns_id_exposure_df.set_index("sample", inplace = True)
            mutationalPatterns_id_exposure_df = mutationalPatterns_id_exposure_df.div(mutationalPatterns_id_exposure_df.sum(axis=1), axis=0)
            mutationalPatterns_id_exposure_df.reset_index(inplace = True)
            pie_chart_rows = math.ceil(mutationalPatterns_id_exposure_df.shape[0] / 3) 
            pie_chart_cols = 3
            rows = math.ceil(mutationalPatterns_id_exposure_df.shape[0] / 6) 
            columns = 6

            id_mutational_patters_fig = make_piecharts(mutationalPatterns_id_exposure_df, pie_chart_rows, pie_chart_cols, "COSMIC V3 'ID' exposures  data MutationalPatterns")    
            id_df_list.append(mutationalPatterns_id_exposure_df.sort_values(by=["sample"]))
            id_df_name_list.append("mutationalPatterns")
        if deconstructSigs:
            deconstructSigs_id_exposure_df = pd.read_csv(r_output_file_dir + "/deconstructsigs_results/indel_sample_exposures.csv")
            deconstructSigs_id_exposure_df.rename( columns = {"Unnamed: 0": "sample"}, inplace= True)
            id_df_list.append(deconstructSigs_id_exposure_df.sort_values(by=["sample"]) )
            id_df_name_list.append("deconstructSigs")
            pie_chart_rows = math.ceil(deconstructSigs_id_exposure_df.shape[0] / 3) 
            pie_chart_cols = 3
            rows = math.ceil(deconstructSigs_id_exposure_df.shape[0] / 6) 
            columns = 6

            deconstructSigs_id_exposure_df_fig = make_piecharts(deconstructSigs_id_exposure_df, pie_chart_rows, pie_chart_cols, "COSMIC V3 'ID' exposures data DeconstructSigs")    
        if sigfit:
            sigfit_id_exposure_df = pd.read_csv(r_output_file_dir + "/sigfit_results/indel_sample_exposures.csv")
            sigfit_id_exposure_df.rename(columns={"Unnamed: 0": "sample" }, inplace= True)
            pie_chart_rows = math.ceil(sigfit_id_exposure_df.shape[0] / 3) 
            pie_chart_cols = 3
            rows = math.ceil(sigfit_id_exposure_df.shape[0] / 6) 
            columns = 6

            sigfit_id_exposure_df_fig = make_piecharts(sigfit_id_exposure_df, pie_chart_rows, pie_chart_cols, "COSMIC V3 'ID' exposures data Sigfit")   
            id_df_list.append(sigfit_id_exposure_df.sort_values(by=["sample"]))
            id_df_name_list.append("sigfit")        
        with open(r_output_file_dir + '/id_bar_charts.html', 'a') as f:
            if sigflow:
                f.write(sigflow_id_exposure_df_fig.to_html(full_html=False, include_plotlyjs='cdn'))
            if mutationalPattern:
                f.write(id_mutational_patters_fig.to_html(full_html=False, include_plotlyjs='cdn'))        
            if sigfit:
                f.write(sigfit_id_exposure_df_fig.to_html(full_html=False, include_plotlyjs='cdn'))
            if deconstructSigs:
                f.write(deconstructSigs_id_exposure_df_fig.to_html(full_html=False, include_plotlyjs='cdn'))
        
        fig = plt.figure(figsize=(50, 10))
        for i in range(len(id_df_list)):  
            sns.set(font_scale=1.7)
            df = id_df_list[i].set_index("sample").astype(float)
            ax = fig.add_subplot(rows, columns, i+1)
            sns.heatmap(df , cmap="YlGnBu", xticklabels = True, yticklabels= True )
            sns.set(rc={'figure.figsize':(10, 10)})
            plt.tight_layout()
            plt.title("Heatmap ID " + str(id_df_name_list[i]))
        
        plt.savefig(r_output_file_dir + "/Heatmap_exposures_all_sigs_ID.svg", bbox_inches='tight')
        plt.savefig(r_output_file_dir + "/Heatmap_exposures_all_sigs_ID.png", bbox_inches='tight')
        
        distance_df_list = []
        sample_name_df = list(id_df_list[0]["sample"])

        for i in range(id_df_list[0].shape[0]):
            temp_df = []
            for index , j in enumerate(id_df_list):
                j["sample"] = id_df_name_list[index]
                temp_df.append(list(j.iloc[i,:]))
            _df = pd.DataFrame(temp_df, columns = id_df_list[0].columns)
            _df.fillna(0, inplace= True)
            distance_df_list.append(_df)

        fig = plt.figure(figsize=(40  , 8 ))
        sns.set(font_scale=1.7)

        for i in range(len(distance_df_list)):  
            df = distance_df_list[i]
            df_ = pd.DataFrame(squareform(pdist(df.iloc[:, 1:] , metric="cosine") ), columns=df["sample"], index=df["sample"]).apply(lambda x : (x -1)*-1 )
            ax = fig.add_subplot(rows, columns, i+1)    

            heatmap = sns.heatmap(df_)
            heatmap.set(xlabel=None)
            heatmap.set(ylabel=None)

            plt.tight_layout()
            plt.title("Heatmap ID "  + sample_name_df[i])
        
        plt.savefig(r_output_file_dir + "/Heatmap_ID.svg", bbox_inches='tight')
        plt.savefig(r_output_file_dir + "/Heatmap_ID.png", bbox_inches='tight')

        
    except Exception as e:
        print("No ID sigs found", e)    
        pass
    
def run_dbs(sigfit = True, sigflow = True, deconstructSigs= True, mutationalPattern = True):
    try:
        dbs_df_list = []
        dbs_df_name_list = []
        if sigflow:
            sigflow_dbs_exposure_df = pd.read_csv(r_output_file_dir + "/sigflow/DBS_fitting_relative_exposure.csv")
            pie_chart_rows = math.ceil(sigflow_dbs_exposure_df.shape[0] / 3) 
            pie_chart_cols = 3
            rows = math.ceil(sigflow_dbs_exposure_df.shape[0] / 6)
            columns = 6

            sigflow_dbs_exposure_df_fig = make_piecharts(sigflow_dbs_exposure_df, pie_chart_rows, pie_chart_cols, "COSMIC V3 'DBS' exposures data Sigflow")   
            dbs_df_list.append(sigflow_dbs_exposure_df.sort_values(by=["sample"]))
            dbs_df_name_list.append("sigflow")
        if mutationalPattern:
            mutationalPatterns_dbs_exposure_df = pd.read_csv(r_output_file_dir + "/mutational_patterns_results/dbs_sample_exposures.csv")
            mutationalPatterns_dbs_exposure_df = mutationalPatterns_dbs_exposure_df.rename(columns={"Unnamed: 0": "sample"})
            mutationalPatterns_dbs_exposure_df.set_index("sample", inplace = True)
            mutationalPatterns_dbs_exposure_df = mutationalPatterns_dbs_exposure_df.div(mutationalPatterns_dbs_exposure_df.sum(axis=1), axis=0)
            mutationalPatterns_dbs_exposure_df.reset_index(inplace = True)
            pie_chart_rows = math.ceil(mutationalPatterns_dbs_exposure_df.shape[0] / 3) 
            pie_chart_cols = 3
            rows = math.ceil(mutationalPatterns_dbs_exposure_df.shape[0] / 6)
            columns = 6


            dbs_mutational_patters_fig = make_piecharts(mutationalPatterns_dbs_exposure_df, pie_chart_rows, pie_chart_cols, "COSMIC V3 'DBS' exposures  data MutationalPatterns")    
            dbs_df_list.append(mutationalPatterns_dbs_exposure_df.sort_values(by=["sample"]))
            dbs_df_name_list.append("mutationalPatterns")
        if deconstructSigs:
            deconstructSigs_dbs_exposure_df = pd.read_csv(r_output_file_dir + "/deconstructsigs_results/dbs_sample_exposures.csv")
            deconstructSigs_dbs_exposure_df.rename( columns = {"Unnamed: 0": "sample"}, inplace= True)
            pie_chart_rows = math.ceil(deconstructSigs_dbs_exposure_df.shape[0] / 3) 
            pie_chart_cols = 3
            rows = math.ceil(deconstructSigs_dbs_exposure_df.shape[0] / 6)
            columns = 6

            deconstructSigs_dbs_exposure_df_fig = make_piecharts(deconstructSigs_dbs_exposure_df, pie_chart_rows, pie_chart_cols, "COSMIC V3 'DBS' exposures data DeconstructSigs")    
            dbs_df_list.append(deconstructSigs_dbs_exposure_df.sort_values(by=["sample"]))
            dbs_df_name_list.append("deconstructSigs")            
        if sigfit:
            sigfit_dbs_exposure_df = pd.read_csv(r_output_file_dir + "/sigfit_results/dbs_sample_exposures.csv")
            sigfit_dbs_exposure_df.rename(columns={"Unnamed: 0": "sample" }, inplace= True)
            pie_chart_rows = math.ceil(sigfit_dbs_exposure_df.shape[0] / 3) 
            pie_chart_cols = 3
            rows = math.ceil(sigfit_dbs_exposure_df.shape[0] / 6)
            columns = 6

            sigfit_dbs_exposure_df_fig = make_piecharts(sigfit_dbs_exposure_df, pie_chart_rows, pie_chart_cols, "COSMIC V3 'DBS' exposures data Sigfit")   
            dbs_df_list.append(sigfit_dbs_exposure_df.sort_values(by=["sample"]))
            dbs_df_name_list.append("sigfit")
        with open(r_output_file_dir + '/dbs_bar_charts.html', 'a') as f:
            if sigflow:
                f.write(sigflow_dbs_exposure_df_fig.to_html(full_html=False, include_plotlyjs='cdn'))
            if mutationalPattern:
                f.write(dbs_mutational_patters_fig.to_html(full_html=False, include_plotlyjs='cdn'))        
            if sigfit:
                f.write(sigfit_dbs_exposure_df_fig.to_html(full_html=False, include_plotlyjs='cdn'))
            if deconstructSigs:
                f.write(deconstructSigs_dbs_exposure_df_fig.to_html(full_html=False, include_plotlyjs='cdn'))
        
        sns.set(font_scale=1.7)
        fig = plt.figure(figsize=(50, 10))
        for i in range(len(dbs_df_list)):  
            sns.set(font_scale=1.7)
            df = dbs_df_list[i].set_index("sample").astype(float)
            ax = fig.add_subplot(rows, columns, i+1)
            sns.heatmap(df , cmap="YlGnBu", xticklabels = True, yticklabels= True )
            sns.set(rc={'figure.figsize':(10, 10)})
            plt.tight_layout()
            plt.title("Heatmap DBS " + str(dbs_df_name_list[i]))
        
        plt.savefig(r_output_file_dir + "/Heatmap_exposures_all_sigs_DBS.svg", bbox_inches='tight')
        plt.savefig(r_output_file_dir + "/Heatmap_exposures_all_sigs_DBS.png", bbox_inches='tight')
        
        distance_df_list = []
        sample_name_df = list(dbs_df_list[0]["sample"])

        for i in range(dbs_df_list[0].shape[0]):
            temp_df = []
            for index , j in enumerate(dbs_df_list):
                j["sample"] = dbs_df_name_list[index]
                temp_df.append(list(j.iloc[i,:]))
            _df = pd.DataFrame(temp_df, columns = dbs_df_list[0].columns)
            _df.fillna(0, inplace= True)
            distance_df_list.append(_df)

        fig = plt.figure(figsize=( 40 , 8 ))
        sns.set(font_scale=1.7)

        for i in range(len(distance_df_list)):  
            df = distance_df_list[i]
            df_ = pd.DataFrame(squareform(pdist(df.iloc[:, 1:] , metric="cosine") ), columns=df["sample"], index=df["sample"]).apply(lambda x : (x -1)*-1 )
            ax = fig.add_subplot(rows, columns, i+1)    
            heatmap = sns.heatmap(df_)
            heatmap.set(xlabel=None)
            heatmap.set(ylabel=None)

            plt.tight_layout()

            plt.title("Heatmap DBS "  + sample_name_df[i])
        
        plt.savefig(r_output_file_dir + "/Heatmap_DBS.svg", bbox_inches='tight')
        plt.savefig(r_output_file_dir + "/Heatmap_DBS.png", bbox_inches='tight')


    except Exception as e:
        print("No DBS sigs found", e)    
        pass

mutationalPattern_input = sys.argv[2] == "TRUE"
sigflow_input =  sys.argv[3] == "TRUE"
sigfit_input = sys.argv[4] == "TRUE"
deconstructSigs_input =  sys.argv[5] == "TRUE"



if os.path.exists(sys.argv[1] + "/output/SBS/MetaMutationalSigs.SBS96.all"):
    run_legacy(sigfit_input, sigflow_input, deconstructSigs_input , mutationalPattern_input )
    run_sbs(sigfit_input, sigflow_input, deconstructSigs_input , mutationalPattern_input)
if os.path.exists(sys.argv[1] + "/output/ID/MetaMutationalSigs.ID83.all"):
    run_id(sigfit_input, sigflow_input, deconstructSigs_input , mutationalPattern_input)
if os.path.exists(sys.argv[1] + "/output/DBS/MetaMutationalSigs.DBS78.all"):
    run_dbs(sigfit_input, sigflow_input, deconstructSigs_input , mutationalPattern_input)