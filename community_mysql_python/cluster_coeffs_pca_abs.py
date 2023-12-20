#Install packages
# pip install numpy
# pip install pandas
# pip install sklearn
# pip install igraph
# pip install networkx
# pip install leidenalg
#pip install mysql
#pip install sqlalchemy

#Import otherfiles from this project
import data_process
import data_std_score
import graph_prune_data
from graph_prune_data import graph_prune
from leiden_communities import finalgraph_after_prune

#Import packages
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import NMF
import networkx as nx
import igraph as ig

#Import in-built python modules
import itertools
import warnings
warnings.filterwarnings("ignore")

std_main_df = data_process.main_dataset_final

class nmf_std_score():
    #Apply normalization on survey scores

    def normalization_data(std_data):

        std_data[['Extro_Total','Tough_Total',\
        'Managing_People_Total','Optimist_Total','Communicating_Total','Success_Total']]\
        = MinMaxScaler().fit_transform(std_data[['Extro_Total','Tough_Total',\
        'Managing_People_Total','Optimist_Total','Communicating_Total','Success_Total']])

        return std_data

    # Using NMF method instead of PCA for dimensionality reduction as per literature
    def nmf_one(input_nmf):
        nmf_input = input_nmf.drop('UserID', axis=1)
        # Instantiate NMF
        nmf = NMF(n_components=1, init='nndsvd')
        # Fit NMF to features
        nmf1 = nmf.fit_transform(nmf_input)
        user_df = std_main_df['UserID']
        nmf1df = pd.DataFrame(nmf1)
        nmf_df = pd.concat([user_df, nmf1df], axis=1)
        return nmf_df

    # Transpose main dataframe before calculating difference
    def transpose_nmfdata(transp_nmfdata):
        # Transpose main dataframe before calculating difference
        dff = transp_nmfdata.set_index('UserID').T
        return dff

    # Calculation of distances(differences) between User scores for all surveys
    # For all combinations, calculate differences in scores
    def abs_difference(df):
        comb = list(itertools.combinations(df.columns, 2))

        new_df = pd.DataFrame()

        for a, b in comb:
            new_df[f"{a},{b}"] = abs(1 / (df[a] - df[b]))
            new_df = new_df.replace([np.inf, -np.inf], 50)

            new_df = new_df.astype('int64')
        new_df = new_df.transpose()

        new_df = new_df.reset_index(level=0)
        new_df = new_df.rename(columns={"index": "UserID"}, errors="raise")
        return new_df

    # print(result_df)
    def graph_nmf(dataframe):
        GNMF = nx.Graph()
        GNMF.add_weighted_edges_from(
            [tuple(d) for d in dataframe[['source', 'target', 'absolute_distance']].values])
        nmf_graph = ig.Graph.from_networkx(GNMF)
        return nmf_graph

    # Creating final nmf based graph
    def final_graph_cluster(dataframe):
        fg = nx.Graph()
        fg.add_weighted_edges_from([tuple(d) for d in dataframe[['source', 'target', 'weight']].values])
        final_g_cluster = fg
        return final_g_cluster

    #Mapping ids to User ids
    def user_names(dataframe, result5_df):
        tdff = dataframe
        tdff = tdff.reset_index()
        trial_df = tdff.rename(columns={'index': 'id'})
        guser1 = nx.Graph()
        guser1.add_weighted_edges_from([tuple(d) for d in trial_df[['source', 'target', 'absolute_distance']].values])
        guser = ig.Graph.from_networkx(guser1)
        guser.vs['id'] = trial_df['id']
        guser_edgelist1 = guser.get_vertex_dataframe()
        user_names = result5_df['UserID']
        guser_edgelist = guser_edgelist1
        guser_edgelist = guser_edgelist.rename(columns={'_nx_name': 'UserID'})
        prefinal_result = pd.merge(user_names, guser_edgelist, how="inner", on="UserID")
        return prefinal_result


    # Clustering using absolute difference
    def cluster_coeffs(graph_to_cluster):
        gcc = nx.average_clustering(graph_to_cluster)
        #print('Average Clustering :', cc)
        clust = nx.clustering(graph_to_cluster)
        #print('Local Clustering :')
        res = {key: round(clust[key], 1) for key in clust}
        #print(str(res))
        clust_df = pd.DataFrame(res.items(), columns=['id', 'Clustering Coefficient'])
        clust_df = clust_df.sort_values('id')
        return clust_df
    #------------------------------------------------------------------------------

#Calling the methods
norm_data_final = nmf_std_score.normalization_data(std_main_df)
nmf_applied_data = nmf_std_score.nmf_one(norm_data_final)
#print(nmf_applied_data)
transpose_nmfdata_final = nmf_std_score.transpose_nmfdata(nmf_applied_data)
nmf_result_df = nmf_std_score.abs_difference(transpose_nmfdata_final)

nmf_result_df[['source', 'target']] = nmf_result_df['UserID'].str.split(',', expand=True)
nmf_result_df = nmf_result_df.rename(columns={0: "absolute_distance"}, errors="raise")
nmf_result_df = nmf_result_df.drop(['UserID'], axis=1)
nmf_result_df = nmf_result_df.astype('int64')

# nmf_diff_data_final = nmf_std_score.nmf_result_df

# print(nmf_diff_data_final)

nmf_graph = nmf_std_score.graph_nmf(nmf_result_df)

# Graph Pruning on nmf data
nmf_pruned_graph = graph_prune.prune_graph(graph=nmf_graph, field='significance', percent=15,
                                           num_remove=None)

nmf_final_g = nmf_std_score.final_graph_cluster(nmf_pruned_graph)

user_prefinal_result = nmf_std_score.user_names(nmf_result_df, data_process.main_dataset_final)

cluster_coefficients = nmf_std_score.cluster_coeffs(nmf_final_g)

final_clust_result = pd.merge(user_prefinal_result, cluster_coefficients, how="inner", on="id")

final_clusters = final_clust_result.drop('id',axis=1)
final_clusters_df = final_clusters.rename(columns={"UserID": "student_id","Clustering Coefficient":"clustering_coefficient"}, errors="raise")
#print(final_clusters_df)