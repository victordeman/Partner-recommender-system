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

#Import packages
import networkx as nx
import igraph as ig
import numpy as np
import pandas as pd
import leidenalg as la

class finalgraph_after_prune():

    # Method for creating all individual final graphs after pruning
    def final_graph(dataframe):
        fg = nx.Graph()
        fg.add_weighted_edges_from([tuple(d) for d in dataframe[['source', 'target', 'weight']].values])
        final_g = ig.Graph.from_networkx(fg)
        return final_g
    #Method for creating leiden partitions for all individual graphs
    def leiden_mpartition(graph):
        leiden_partition = la.find_partition(
            graph,\
            la.ModularityVertexPartition, seed=2, n_iterations=-2, max_comm_size=4)
        return leiden_partition

    # Method for creating leiden membership combined for graphs
    def leiden_membership(*graphs):
        leiden_communities = la.find_partition_multiplex(
            graphs,\
            la.ModularityVertexPartition, seed=2, n_iterations=-2, max_comm_size=4)
        return leiden_communities

    #Method for getting indexes and converting to user ids
    def index_user(dataframe, result5_df):
        tdff = dataframe
        tdff.reset_index(inplace=True)
        trial_df = tdff.rename(columns={'index': 'id'})
        guser1 = nx.Graph()
        guser1.add_weighted_edges_from([tuple(d) for d in trial_df[['source', 'target', 'weight']].values])
        guser = ig.Graph.from_networkx(guser1)
        guser.vs['id'] = trial_df['id']
        guser_edgelist1 = guser.get_vertex_dataframe()
        guser_edgelist1 = guser_edgelist1.astype('int64')
        user_names = result5_df['UserID']
        guser_edgelist = guser_edgelist1
        guser_edgelist = guser_edgelist.rename(columns={'_nx_name': 'UserID'})
        prefinal_result = pd.merge(user_names, guser_edgelist, how="inner", on="UserID")
        return prefinal_result

#Technique 1 Creating final graphs
# extro_final_g = finalgraph_after_prune.final_graph(graph_prune_data.extro_pruned_graph)
# optim_final_g = finalgraph_after_prune.final_graph(graph_prune_data.optim_pruned_graph)
# tough_final_g = finalgraph_after_prune.final_graph(graph_prune_data.tough_pruned_graph)
# manage_final_g = finalgraph_after_prune.final_graph(graph_prune_data.manage_pruned_graph)
# comm_final_g = finalgraph_after_prune.final_graph(graph_prune_data.comm_pruned_graph)
# success_final_g = finalgraph_after_prune.final_graph(graph_prune_data.success_pruned_graph)

#Technique 2 Creating final graphs copying auto updated graphs after pruning
extro_final_g = graph_prune_data.extro_graphFinal
optim_final_g = graph_prune_data.optim_graphFinal
tough_final_g = graph_prune_data.tough_graphFinal
manage_final_g = graph_prune_data.manage_graphFinal
comm_final_g = graph_prune_data.comm_graphFinal
success_final_g = graph_prune_data.success_graphFinal

#Finding leiden partitions for all graphs individually
leiden_partition_extro = finalgraph_after_prune.leiden_mpartition(extro_final_g)
#print(leiden_partition_extro)
#print(leiden_partition_extro.modularity)

leiden_partition_optim = finalgraph_after_prune.leiden_mpartition(optim_final_g)
#print(leiden_partition_optim)
#print(leiden_partition_optim.modularity)

leiden_partition_tough = finalgraph_after_prune.leiden_mpartition(tough_final_g)
#print(leiden_partition_tough)
#print(leiden_partition_tough.modularity)

leiden_partition_manage = finalgraph_after_prune.leiden_mpartition(manage_final_g)
#print(leiden_partition_manage)
#print(leiden_partition_manage.modularity)

leiden_partition_comm = finalgraph_after_prune.leiden_mpartition(comm_final_g)
#print(leiden_partition_comm)
#print(leiden_partition_comm.modularity)

leiden_partition_success = finalgraph_after_prune.leiden_mpartition(success_final_g)
#print(leiden_partition_success)
#print(leiden_partition_success.modularity)

#Replacing ids with userids for leiden partitions for all graphs individually
#Extro partition
user_extro_result = finalgraph_after_prune.index_user(data_std_score.std_score.resultdf_extro, data_process.main_dataset_final)
userids_dict_extro = dict(zip(user_extro_result.id, user_extro_result.UserID))
partlextro = list(leiden_partition_extro)
partition_extro_final = [[userids_dict_extro[u] for u in i] for i in partlextro]

#Optim partition
user_optim_result = finalgraph_after_prune.index_user(data_std_score.std_score.resultdf_optim, data_process.main_dataset_final)
userids_dict_optim = dict(zip(user_optim_result.id, user_optim_result.UserID))
partloptim = list(leiden_partition_optim)
partition_optim_final = [[userids_dict_optim[u] for u in i] for i in partloptim]

#Tough partition
user_tough_result = finalgraph_after_prune.index_user(data_std_score.std_score.resultdf_tough, data_process.main_dataset_final)
userids_dict_tough = dict(zip(user_tough_result.id, user_tough_result.UserID))
partltough = list(leiden_partition_tough)
partition_tough_final = [[userids_dict_tough[u] for u in i] for i in partltough]

#Manage partition
user_manage_result = finalgraph_after_prune.index_user(data_std_score.std_score.resultdf_manage, data_process.main_dataset_final)
userids_dict_manage = dict(zip(user_manage_result.id, user_manage_result.UserID))
partlmanage = list(leiden_partition_manage)
partition_manage_final = [[userids_dict_manage[u] for u in i] for i in partlmanage]

#Comm partition
user_comm_result = finalgraph_after_prune.index_user(data_std_score.std_score.resultdf_comm, data_process.main_dataset_final)
userids_dict_comm = dict(zip(user_comm_result.id, user_comm_result.UserID))
partlcomm = list(leiden_partition_comm)
partition_comm_final = [[userids_dict_comm[u] for u in i] for i in partlcomm]

#Success partition
user_success_result = finalgraph_after_prune.index_user(data_std_score.std_score.resultdf_success, data_process.main_dataset_final)
userids_dict_success = dict(zip(user_success_result.id, user_success_result.UserID))
partlsuccess = list(leiden_partition_success)
partition_success_final = [[userids_dict_success[u] for u in i] for i in partlsuccess]


#Finding leiden membership for all graphs combined
leiden_multiplex_community = finalgraph_after_prune.leiden_membership(extro_final_g,optim_final_g,tough_final_g,manage_final_g,comm_final_g,success_final_g)
#print(leiden_multiplex_community)

#Grouping by communities and replacing ids with userids for leiden membership
user_comm_prefinal_result = finalgraph_after_prune.index_user(data_std_score.std_score.resultdf_extro, data_process.main_dataset_final)
userids_dict = dict(zip(user_comm_prefinal_result.id, user_comm_prefinal_result.UserID))
leiden_mem = leiden_multiplex_community[0]
index_mem = pd.Series(range(len(leiden_mem))).groupby(leiden_mem, sort=False).apply(list).tolist()
members_final_ll = [[userids_dict[u] for u in i] for i in index_mem]
#print(members_final_ll)