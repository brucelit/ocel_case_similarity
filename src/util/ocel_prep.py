import numpy
import pandas as pd
import src.util.extrace_case as ec
import src.util.to_graphviz as tg
import io

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import src.algorithms.edit_distance as ged
import src.algorithms.weisfeiler_lehman_kernel as wlk
import src.algorithms.similarity as sm
import matplotlib.pyplot as plt
import networkx as nx
import sys,time
import numpy as np
import func_timeout
import numpy as np
import pygraphviz as pgv
import os

from networkx.drawing.nx_agraph import graphviz_layout, to_agraph
from tqdm import tqdm
from pm4py.objects.ocel.importer.xmlocel import importer
from pm4py.objects.ocel.util import *
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from sklearn.cluster import AgglomerativeClustering


def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack(
        [model.children_, model.distances_, counts]
    ).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)

def node_ins_del_cost(n):
    return 1


def node_subs_cost(n1, n2):
    if n1['label'] == n2['label']:
        return 0
    else:
        return 2


def edge_ins_del_cost(e):
    return 1


def node_match(n1, n2):
    if n1['label'] == n2['label']:
        return True
    return False


def edge_subst_cost(e1, e2, d1, d2):
    if d1.nodes[e1[0]]['label'] == d2.nodes[e2[0]]['label'] and d1.nodes[e1[1]]['label'] == d2.nodes[e2[1]]['label']:
        return 0
    return 1


def get_ged(digraph1, digraph2):
    path, best_cost = sm.optimal_edit_paths(digraph1,
                          digraph2,
                          node_match=lambda a,b: a['label'] == b['label'],
                          node_del_cost=node_ins_del_cost,
                          node_subst_cost=node_subs_cost,
                          node_ins_cost=node_ins_del_cost,
                          edge_del_cost=edge_ins_del_cost,
                          edge_ins_cost=edge_ins_del_cost,
                          edge_subst_cost=edge_subst_cost)
    return path, best_cost

#定义一个进度条
def process_bar(num, total):
    rate = float(num)/total
    ratenum = int(100*rate)
    r = '\r[{}{}]{}%'.format('*'*ratenum,' '*(100-ratenum), ratenum)
    sys.stdout.write(r)
    sys.stdout.flush()

def plot_network(G):
  ag = nx.nx_agraph.to_agraph(G)
  ag.layout(prog="dot")
  tempname = "temp.svg"
  ag.draw(tempname)
  img = mpimg.imread(tempname)

  plt.figure(dpi=2000)
  plt.axis('off')
  plt.imshow(img)

  plt.show()
  os.remove(tempname)


if __name__ == "__main__":
    ocel = importer.apply("..\..\data\\running-example.xmlocel")
    # print(related_objects.related_objects_dct_per_type(ocel)["applications"])
    # print(ocel.get_summary())
    # print(pm4py.ocel_get_attribute_names(ocel))
    # print(ocel.events)
    # print(ocel.objects)
    # l1 = ocel.objects['ocel:type'].unique()

    # df = flattening.flatten(ocel, "applications")
    # print(df)
    # df1 = df[df['case:concept:name'] == 'Application[770001]']
    # print()
    # print(df[df['case:concept:name'] == 'Application[770001]']['concept:name'].tolist())
    # print(list(ocel.columns.values)
    restrictions = {"1":("coexist","items","place order")}
    case_dict, case_idx_dict = ec.extract_case_with_leading_type(ocel, "orders", ['items','packages'],
                                                                 restrictions=restrictions)

    print("finish extraction",case_idx_dict)

    similarity_matrix = np.ones((len(case_dict),len(case_dict)))
    for k1 in case_dict.keys():
        # ax = plt.gca()
        # pos = nx.nx_agraph.graphviz_layout(case_dict[k1])
        # nx.draw_networkx_nodes(case_dict[k1], pos, node_color='r', node_size=100, alpha=1)
        #
        # for e in case_dict[k1].edges:
        #     ax.annotate("",
        #                 xy=pos[e[0]], xycoords='data',
        #                 xytext=pos[e[1]], textcoords='data',
        #                 arrowprops=dict(arrowstyle="->", color="0.5",
        #                                 shrinkA=5, shrinkB=5,
        #                                 patchA=None, patchB=None,
        #                                 connectionstyle="arc3,rad=rrr".replace('rrr', str(0.3 * e[2])
        #                                                                        ),
        #                                 ),
        #                 )
        # plt.axis('off')
        # plt.show()
        # nx.draw(case_dict[k1], with_labels=True)

        # plt.show()
        # for each_eadge in case_dict[k1].edges:
        #     print(each_eadge)

        # case_dict[k1].graph['node'] = {'shape': 'circle', 'fixedsize': 'true'}
        # case_dict[k1].graph['edges'] = {'arrowsize': '4.0'}
        #
        # set defaults
        G=case_dict[k1]
        G.graph['graph'] = {'rankdir': 'TD'}
        G.graph['node'] = {'shape': 'rectangle','fixedsize': 'true'}
        G.graph['edges'] = {'arrowsize': '4.0'}

        plot_network(G)
        # for k2 in case_dict.keys():
        #     dg_trans1, dg_trans2, label_num = wlk.translate_evt_to_int_id(case_dict[k1].copy(),
        #                                                                   case_dict[k2].copy())
        #     score = wlk.get_normalized_similarity_score(dg_trans1.copy(), dg_trans2.copy(), label_num)
        #     kernel_score = score
        #     idx1 = case_idx_dict[k1]
        #     idx2 = case_idx_dict[k2]
        #     similarity_matrix[idx1][idx2] = kernel_score




    # print(similarity_matrix)
    # for i in range(0, len(case_dict.keys())):
    #     for j in range(0, len(case_dict.keys())):
    #         for k in range(0, len(case_dict.keys())):
    #             if similarity_matrix[i][j] < min(similarity_matrix[i][k],similarity_matrix[k][j]):
    #                 print("不行",i,j,k)

    # clustering = AgglomerativeClustering(affinity='precomputed', linkage='complete').fit(similarity_matrix)
    # print(clustering.labels_)
    # print(case_dict.keys())
    # model = AgglomerativeClustering(distance_threshold=0, n_clusters=None,affinity='precomputed', linkage='complete')
    # model = model.fit(similarity_matrix)
    # plt.title("Hierarchical Clustering Dendrogram")
    # # plot the top three levels of the dendrogram
    # plot_dendrogram(model, truncate_mode="level", p=4)
    # plt.xlabel("Number of points in node (or index of point if no parenthesis).")
    # plt.show()
    # print(similarity_matrix)
    # plt.scatter(x, y)
    # plt.show()
                # for e1 in v1.edges:
                #     for e2 in v2.edges:
                #         edge_subst_cost(e1, e2, v1, v2)

    # 对于每个obj类型，获取对应的event数目
    #
    # # 每个activity的mean max min median
    # print(events_per_type_per_activity.apply(ocel))


    # 获取每个obj对应的event
    # dict1 = related_events.related_events_dct(ocel)
    # for k,v in dict1.items():
    #     for k1, v1 in v.items():
    #         print(k1, " ", v1)

    #
    # dict2 = related_objects.related_objects_dct_per_type(ocel)
    # for k, v in dict2.items():
    #     if k == "vacancies":
    #         for k1, v1 in v.items():
    #             print(k1,v1)

    # for all events, get the related objects
    # dict3 = related_objects.related_objects_dct_overall(ocel)
    # for k, v in dict3.items():
    #     print(k, v)
