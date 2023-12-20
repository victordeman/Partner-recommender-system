#Install packages
# pip install numpy
# pip install pandas
# pip install sklearn
# pip install igraph
# pip install networkx
# pip install leidenalg
#pip install mysql
#pip install sqlalchemy

#Referenced MLF for graph pruning from https://github.com/naviddianati/GraphPruning

#Import otherfiles from this project
import data_std_score
from graphPruning2.pruning import unimodal
from graphPruning2.pruning import utils

#Import packages
import networkx as nx
import igraph as ig

class graph_before_prune():

    G1 = nx.Graph()
    G1.add_weighted_edges_from([tuple(d) for d in data_std_score.diff_data_final[['source', 'target', 'Extro_Total']].values])
    extro_g = ig.Graph.from_networkx(G1)

    G2 = nx.Graph()
    G2.add_weighted_edges_from([tuple(d) for d in data_std_score.diff_data_final[['source', 'target', 'Optimist_Total']].values])
    optim_g = ig.Graph.from_networkx(G2)

    G3 = nx.Graph()
    G3.add_weighted_edges_from([tuple(d) for d in data_std_score.diff_data_final[['source', 'target', 'Tough_Total']].values])
    tough_g = ig.Graph.from_networkx(G3)

    G4 = nx.Graph()
    G4.add_weighted_edges_from([tuple(d) for d in data_std_score.diff_data_final[['source', 'target', 'Managing_People_Total']].values])
    manage_g = ig.Graph.from_networkx(G4)

    G5 = nx.Graph()
    G5.add_weighted_edges_from([tuple(d) for d in data_std_score.diff_data_final[['source', 'target', 'Communicating_Total']].values])
    comm_g = ig.Graph.from_networkx(G5)

    G6 = nx.Graph()
    G6.add_weighted_edges_from([tuple(d) for d in data_std_score.diff_data_final[['source', 'target', 'Success_Total']].values])
    success_g = ig.Graph.from_networkx(G6)

class graph_prune():

    def prune_graph(graph, field='significance', percent=25, num_remove=None):

        df = graph.get_edge_dataframe()
        mlf = unimodal.MLF(directed=False)
        G = mlf.fit_transform(graph)
        df_edgelist_1 = G.get_edge_dataframe()
        # New edge attribute "significance" is created
        #print(G.es.attributes())
        # Apply the transform to the edgelist
        # dataframe of the graph
        mlf = unimodal.MLF(directed=False)
        df_edgelist_2 = mlf.fit_transform(df)
        # Retain significant edges based on percent specified
        utils.prune(G, field, percent, num_remove)
        df = G.get_edge_dataframe()
        return df


def graphstats(graph):

    nodeCount = graph.vcount()
    edgeCount = graph.ecount()
    avgDegree = ig.mean(graph.degree())
    MaxDegree = (graph.maxdegree())
    Density = graph.density(loops=False)
    return nodeCount,edgeCount,avgDegree,MaxDegree,Density

print('Before Pruning Statistics')

extroBeforePruneStats = graphstats(graph_before_prune().extro_g)
print('Extro ',extroBeforePruneStats)
optimBeforePruneStats = graphstats(graph_before_prune().optim_g)
print('Optim ',optimBeforePruneStats)
ToughBeforePruneStats = graphstats(graph_before_prune().tough_g)
print('Tough ',ToughBeforePruneStats)
ManageBeforePruneStats = graphstats(graph_before_prune().manage_g)
print('Manage ',ManageBeforePruneStats)
CommBeforePruneStats = graphstats(graph_before_prune().comm_g)
print('Comm ',CommBeforePruneStats)
SuccessBeforePruneStats = graphstats(graph_before_prune().success_g)
print('Success ',SuccessBeforePruneStats)

#Plot graphs before pruning and save as png image files
ig.plot(graph_before_prune().extro_g, target='extro_graph_beforeprune.png')
ig.plot(graph_before_prune().optim_g, target='optim_graph_beforeprune.png')
ig.plot(graph_before_prune().tough_g, target='tough_graph_beforeprune.png')
ig.plot(graph_before_prune().manage_g, target='manage_graph_beforeprune.png')
ig.plot(graph_before_prune().comm_g, target='comm_graph_beforeprune.png')
ig.plot(graph_before_prune().success_g, target='success_graph_beforeprune.png')

#Save graphs before pruning
# graph_before_prune().extro_g.save("extro_graph_beforeprune.gml")
# graph_before_prune().optim_g.save("optim_graph_beforeprune.gml")
# graph_before_prune().tough_g.save("tough_graph_beforeprune.gml")
# graph_before_prune().manage_g.save("manage_graph_beforeprune.gml")
# graph_before_prune().comm_g.save("comm_graph_beforeprune.gml")
# graph_before_prune().success_g.save("success_graph_beforeprune.gml")


##########################################################
extro_pruned_graph = graph_prune.prune_graph(graph=graph_before_prune().extro_g, field='significance', percent=15, num_remove=None)
optim_pruned_graph = graph_prune.prune_graph(graph=graph_before_prune().optim_g, field='significance', percent=15, num_remove=None)
tough_pruned_graph = graph_prune.prune_graph(graph=graph_before_prune().tough_g, field='significance', percent=15, num_remove=None)
manage_pruned_graph = graph_prune.prune_graph(graph=graph_before_prune().manage_g, field='significance', percent=15, num_remove=None)
comm_pruned_graph = graph_prune.prune_graph(graph=graph_before_prune().comm_g, field='significance', percent=15, num_remove=None)
success_pruned_graph = graph_prune.prune_graph(graph=graph_before_prune().success_g, field='significance', percent=15, num_remove=None)


#After applying pruning the existing graphs are updated so no need to create new graph object again
#For directly using updated graphs after pruning
extro_graphFinal = graph_before_prune().extro_g
optim_graphFinal = graph_before_prune().optim_g
tough_graphFinal = graph_before_prune().tough_g
manage_graphFinal = graph_before_prune().manage_g
comm_graphFinal = graph_before_prune().comm_g
success_graphFinal = graph_before_prune().success_g

#Plot graphs after pruning and save as png image files
ig.plot(extro_graphFinal, target='extro_graph_afterprune.png')
ig.plot(optim_graphFinal, target='optim_graph_afterprune.png')
ig.plot(tough_graphFinal, target='tough_graph_afterprune.png')
ig.plot(manage_graphFinal, target='manage_graph_afterprune.png')
ig.plot(comm_graphFinal, target='comm_graph_afterprune.png')
ig.plot(success_graphFinal, target='success_graph_afterprune.png')

print('***************')
print('After Pruning Statistics')
extroAfterPruneStats = graphstats(graph_before_prune().extro_g)
print('ExtroGP ',extroAfterPruneStats)
optimAfterPruneStats = graphstats(graph_before_prune().optim_g)
print('OptimGP ',optimAfterPruneStats)
ToughAfterPruneStats = graphstats(graph_before_prune().tough_g)
print('ToughGP ',ToughAfterPruneStats)
ManageAfterPruneStats = graphstats(graph_before_prune().manage_g)
print('ManageGP ',ManageAfterPruneStats)
CommAfterPruneStats = graphstats(graph_before_prune().comm_g)
print('CommGP ',CommAfterPruneStats)
SuccessAfterPruneStats = graphstats(graph_before_prune().success_g)
print('SuccessGP ',SuccessAfterPruneStats)

#Save graphs after pruning
# graph_before_prune().extro_g.save("extro_graph_afterprune.gml")
# graph_before_prune().optim_g.save("optim_graph_afterprune.gml")
# graph_before_prune().tough_g.save("tough_graph_afterprune.gml")
# graph_before_prune().manage_g.save("manage_graph_afterprune.gml")
# graph_before_prune().comm_g.save("comm_graph_afterprune.gml")
# graph_before_prune().success_g.save("success_graph_afterprune.gml")