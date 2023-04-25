from pm4py.objects.ocel.importer.xmlocel import importer
from pm4py.objects.ocel.util import *
import pandas as pd
import src.util.extrace_case as ec
import src.algorithms.edit_distance as ged
import src.algorithms.weisfeiler_lehman_kernel as wlk
import src.algorithms.similarity as sm
import matplotlib.pyplot as plt

import sys,time
import numpy as np

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

def get_related_objects_of_selected_type(ocel, rev_object_types):
    dct = {}
    for ot in rev_object_types:
        df = ocel.relations[ocel.relations[ocel.object_type_column] == ot]
        dct[ot] = df['ocel:oid'].unique().tolist()
    return dct


def related_events_dct(ocel):
    object_types = ocel.relations[ocel.object_type_column].unique()
    dct = {}
    for ot in object_types:
        dct[ot] = ocel.relations[ocel.relations[ocel.object_type_column] == ot].groupby(ocel.object_id_column)[ocel.event_activity].apply(
            list).to_dict()
    return dct



if __name__ == "__main__":
    ocel = importer.apply("..\..\data\\recruiting.xmlocel")

    rev_object_types = ['vacancies', "applications"]



    # 对于每个object都有对应的event
    # df = ocel.relations
    # df1 = df[df['ocel:type'] == 'vacancies']
    # print(df1['ocel:oid'].tolist())

    # 对于每个obj类型，获取对应的event数目
    # print(events_per_object_type.apply(ocel))

    # 获取每个obj对应的event
    dict1 = related_events_dct(ocel)
    for k,v in dict1.items():
        for k1, v1 in v.items():
            print(k1, " ", v1)

    # dict2 = related_objects.related_objects_dct_per_type(ocel)
    # for k, v in dict2.items():
    #     if k == "vacancies":
    #         for k1, v1 in v.items():
    #             print(k1,v1)

    # for all events, get the related objects
    # dict3 = related_objects.related_objects_dct_overall(ocel)
    # for k, v in dict3.items():
    #     print(k, v)
