# from sklearn.cluster import AgglomerativeClustering
# import numpy as np
# data_matrix = np.ones((5,5))
# data_matrix[0][1] = 0.5
# data_matrix[1][0] = 0.5
#
# clustering = AgglomerativeClustering(affinity='precomputed',linkage='average').fit(data_matrix)
# print(clustering.labels_)
# print(data_matrix)
import grakel
import networkx as nx
from grakel import graph_from_networkx, Propagation,\
    RandomWalk, WeisfeilerLehmanOptimalAssignment, PyramidMatch, WeisfeilerLehman, RandomWalkLabeled
import src.algorithms.weisfeiler_lehman_kernel as wlkernel

# digraph1 = nx.DiGraph()
# digraph1.add_node(1, label="1")
# digraph1.add_node(2, label="2")
# digraph1.add_node(3, label="3")
# digraph1.add_node(4, label="3")
# digraph1.add_node(5, label="4")
# digraph1.add_edges_from([(1, 2), (2, 3), (3, 5), (2, 4), (4, 5)])
#
# digraph2 = nx.DiGraph()
# digraph2.add_node(1, label="1")
# digraph2.add_node(2, label="2")
# digraph2.add_node(3, label="2")
# digraph2.add_node(4, label="3")
# digraph2.add_node(5, label="3")
# digraph2.add_node(6, label="4")
# digraph2.add_node(7, label="4")
# digraph2.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 7)])
#
#
# grakel_graph1 = graph_from_networkx(digraph1,node_labels_tag='label',as_Graph=True)
# grakel_graph2 = graph_from_networkx(digraph2,node_labels_tag='label',as_Graph=True)
# print(type(grakel_graph1))
#
# rd = RandomWalk()
# parsed_grakel_graph1 = rd.parse_input(grakel_graph1)
# parsed_grakel_graph2 = rd.parse_input(grakel_graph2)
#
# print(rd.paipmise_operation(parsed_grakel_graph1,parsed_grakel_graph2))

G1 = nx.DiGraph()
G1.add_nodes_from([0,1,2,3])
G1.add_edges_from([(0,1),(1,2),(2,3)])
nx.set_node_attributes(G1, {0:'a', 1:'b', 2:'c',3:'d'}, 'label')

G2 = nx.DiGraph()
G2.add_nodes_from([0,1,2])
G2.add_edges_from([(0,1),(1,2)])
nx.set_node_attributes(G2, {0:'a', 1:'b', 2:'c'}, 'label')

G3 = nx.DiGraph()
G3.add_nodes_from([0,1,2,3])
G3.add_edges_from([(0,1)])
nx.set_node_attributes(G3, {0:'a', 1:'b', 2:'c',3:'d'}, 'label')


G4 = nx.DiGraph()
G4.add_nodes_from([0,1,2,3])
G4.add_edges_from([(3,2),(2,1),(1,0)])
nx.set_node_attributes(G4, {0:'a', 1:'b', 2:'c',3:'d'}, 'label')


G5 = nx.DiGraph()
G5.add_nodes_from([0,1,2,3])
G5.add_edges_from([(1,2)])
nx.set_node_attributes(G5, {0:'a', 1:'b', 2:'c',3:'d'}, 'label')

score = wlkernel.get_normalized_similarity_score(G1.copy(), G2.copy(), 4)
score1 = wlkernel.get_normalized_similarity_score(G1.copy(), G1.copy(), 4)
score2 = wlkernel.get_normalized_similarity_score(G2.copy(), G2.copy(), 4)
temp_score = max(score1, score2)
print(score / temp_score)
score = wlkernel.get_normalized_similarity_score(G1.copy(), G3.copy(), 4)
score1 = wlkernel.get_normalized_similarity_score(G1.copy(), G1.copy(), 4)
score2 = wlkernel.get_normalized_similarity_score(G3.copy(), G3.copy(), 4)
temp_score = max(score1, score2)
print(score / temp_score)
score = wlkernel.get_normalized_similarity_score(G1.copy(), G4.copy(), 4)
score1 = wlkernel.get_normalized_similarity_score(G1.copy(), G1.copy(), 4)
score2 = wlkernel.get_normalized_similarity_score(G4.copy(), G4.copy(), 4)
temp_score = max(score1, score2)
print(score / temp_score)
score = wlkernel.get_normalized_similarity_score(G1.copy(), G5.copy(), 4)
score1 = wlkernel.get_normalized_similarity_score(G1.copy(), G1.copy(), 4)
score2 = wlkernel.get_normalized_similarity_score(G5.copy(), G5.copy(), 4)
temp_score = max(score1, score2)
print(score / temp_score)


# Transforms list of NetworkX graphs into a list of GraKeL graphs
G11 = graph_from_networkx([G1], node_labels_tag='label')
G12 = graph_from_networkx([G2], node_labels_tag='label')
G13 = graph_from_networkx([G3], node_labels_tag='label')
G14 = graph_from_networkx([G4], node_labels_tag='label')
G15 = graph_from_networkx([G5], node_labels_tag='label')

# wlk = WeisfeilerLehman(normalize=True)
# G4 = wlk.parse_input(G12)

pm = PyramidMatch(normalize=True,with_labels=False,d=100)
v1 = pm.fit_transform(G11)
v2 = pm.transform(G12)
v3 = pm.transform(G13)
v4 = pm.transform(G14)
v5 = pm.transform(G15)
print(v1,v2,v3,v4,v5)

# pk = Propagation(normalize=True)
# v1 = pk.fit_transform(G11)
# v2 = pk.transform(G12)
# v3 = pk.transform(G13)
# v4 = pk.transform(G14)
# v5 = pk.transform(G15)
# print(v1,v2,v3,v4,v5)


# wl = WeisfeilerLehman(normalize=True,n_iter=2)
# v1 = wl.fit_transform(G11)
# v2 = wl.transform(G12)
# v3 = wl.transform(G13)
# v4 = wl.transform(G14)
# v5 = wl.transform(G15)
# print(v1,v2,v3,v4,v5)

# wlo = WeisfeilerLehmanOptimalAssignment(normalize=True,n_iter=2)
# v1 = wlo.fit_transform(G11)
# v2 = wlo.transform(G12)
# v3 = wlo.transform(G13)
# v4 = wlo.transform(G14)
# v5 = wlo.transform(G15)
# print(v1,v2,v3,v4,v5)

# rwl = RandomWalk(normalize=True,method_type='baseline',p=2)
# v1 = rwl.fit_transform(G11)
# v2 = rwl.transform(G12)
# v3 = rwl.transform(G13)
# v4 = rwl.transform(G14)
# v5 = rwl.transform(G15)
# print(v1,v2,v3,v4,v5)
