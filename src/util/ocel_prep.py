from pm4py.objects.ocel.importer.xmlocel import importer
from pm4py.objects.ocel.util import *
import pandas as pd
import src.util.extrace_case as ec
import src.algorithms.edit_distance as ged
import src.algorithms.weisfeiler_lehman_kernel as wlk
import src.algorithms.similarity as sm
import matplotlib.pyplot as plt
import networkx as nx
import sys,time
import numpy as np
import func_timeout

from tqdm import tqdm

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

    case_dict = ec.extract_case_with_leading_type(ocel, "orders", ['items'])

    x = np.array([])
    y = np.array([])
    #

    i = 0

    for k1, v1 in case_dict.items():
        print(k1, len(v1.nodes), len(v1.edges))
        # nx.draw_networkx(v1, with_labels=True, font_weight='bold')
        # plt.show()

        print("\n event id: ", k1)
        for k2, v2 in case_dict.items():
            if k1 != k2 and i >1:
                try:
                    path, best_cost = sm.optimal_edit_paths(v1.copy(), v2.copy(),
                                                            node_match=lambda a, b: a['label'] == b['label'],
                                                            node_subst_cost=node_subs_cost,
                                                            node_del_cost=node_ins_del_cost,
                                                            node_ins_cost=node_ins_del_cost,
                                                            edge_del_cost=edge_ins_del_cost,
                                                            edge_ins_cost=edge_ins_del_cost,
                                                            edge_subst_cost=edge_subst_cost)
                    print("edit dist:", best_cost)
                    # 若调用函数超时自动走异常(可在异常中写超时逻辑处理)
                except func_timeout.exceptions.FunctionTimedOut:
                    print('执行函数超时')




                # x = np.append(x, best_cost)
                dg_trans1, dg_trans2, label_num = wlk.translate_evt_to_int_id(v1.copy(), v2.copy())
                score = wlk.get_normalized_similarity_score(dg_trans1.copy(), dg_trans2.copy(), label_num)
                score1 = wlk.get_normalized_similarity_score(dg_trans1.copy(), dg_trans1.copy(), label_num)
                score2 = wlk.get_normalized_similarity_score(dg_trans2.copy(), dg_trans2.copy(), label_num)
                temp_score = max(score1, score2)
                print("kernel score:", score/temp_score)
                y = np.append(y,score/temp_score)

        i += 1

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
