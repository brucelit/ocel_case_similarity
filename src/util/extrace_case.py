from pm4py.objects.ocel.util import *
import networkx as nx
import time

color_lst = ["#800000","#BDB76B","#808000","#DC143C","#BC8F8F",
             "#FF0000","#32CD32","#FF7F50","#20B2AA","#CD5C5C",
             "#FF8C00","#2F4F4F","#FFD700","#00CED1","#00BFFF",
             "#4682B4","#000080","#FF00FF","#F5DEB3","#8B4513"]

def related_event_id_dict(ocel, object_types):
    dct = {}
    for ot in object_types:
        dct.update(ocel.relations[ocel.relations[ocel.object_type_column] == ot].groupby(ocel.object_id_column)[
                       ocel.event_id_column].apply(
            list).to_dict())
    return dct


def related_event_activity_dict(ocel, object_types):
    dct = {}
    for ot in object_types:
        dct.update(ocel.relations[ocel.relations[ocel.object_type_column] == ot].groupby(ocel.object_id_column)[
                       ocel.event_activity].apply(
            list).to_dict())
    return dct


def extract_case_with_leading_type(ocel, lead_obj_type, rev_object_types=None, restrictions=None):
    '''
       Return the dictionary of (case) event-graph

       Parameters
       ----------
       ocel: ocel
           The ocel to be extracted.
       lead_obj_type: string
           The leading object type to use.
       sec_object_types: string
           The leading object type to use.

       Returns
       -------
       new dictionary : dict
           A dictionary with each key given by a leading event type, and each value to be the corresponding case.
       '''

    # get all objects of leading obj type
    lead_obj_lst = ocel.objects[ocel.objects[ocel.object_type_column] ==
                                lead_obj_type]["ocel:oid"].values.flatten().tolist()

    # for all events, get the related objs
    evt_related_obj_dict = related_objects.related_objects_dct_overall(ocel)

    # flatten all event of leading obj type
    df = flattening.flatten(ocel, lead_obj_type)

    # keep all cases with case_dict
    case_dict = {}
    case_idx_dict = {}  # save obj string to similar matrix

    # set obj to eid dictionary
    sec_obj_to_eid_dict = related_event_id_dict(ocel, rev_object_types)
    sec_obj_to_act_dict = related_event_activity_dict(ocel, rev_object_types)

    all_obj_dict, all_obj_to_type_dict = get_secondary_objects(ocel)

    # iterate every object of leading type
    color_idx = 0

    start_time = time.time()
    for lead_obj in lead_obj_lst:

        evt_digraph = nx.MultiDiGraph()

        # get the list of events related to lead_obj
        lead_obj_to_act_lst = df[df['case:concept:name'] == lead_obj]['concept:name'].tolist()
        lead_obj_to_eid_lst = df[df['case:concept:name'] == lead_obj]['ocel:eid'].tolist()

        # add the event id as node id
        for i in range(0, len(lead_obj_to_eid_lst)):
            evt_digraph.add_node(lead_obj_to_eid_lst[i], label=lead_obj_to_act_lst[i])

        # add the edge
        for j in range(0, len(lead_obj_to_eid_lst) - 1):
            evt_digraph.add_edge(lead_obj_to_eid_lst[j], lead_obj_to_eid_lst[j + 1],
                                 label=lead_obj,
                                 color = color_lst[color_idx%20])
        color_idx += 1

        # keep all secondary objects using temp_sec_obj_dict, key: obj type. val: obj
        temp_sec_obj_dict = {}
        for each_obj_type in rev_object_types:
            temp_sec_obj_dict[each_obj_type] = set()

        for each_eid in lead_obj_to_eid_lst:
            # for each objs in this event
            for each_obj in evt_related_obj_dict[each_eid]:
                if all_obj_to_type_dict[each_obj] in rev_object_types:
                    temp_sec_obj_dict[all_obj_to_type_dict[each_obj]].add(each_obj)

        if restrictions:
            temp_sec_obj_dict = update_obj_to_keep(restrictions,
                                                   lead_obj_to_eid_lst,
                                                   lead_obj_to_act_lst,
                                                   evt_related_obj_dict,
                                                   all_obj_to_type_dict,
                                                   temp_sec_obj_dict
                                                   )
        # ------------ add events related to sec obj type ------------
        for sec_obj_type_key, sec_obj_set in temp_sec_obj_dict.items():
            for each_obj in sec_obj_set:
                # get the list of events related to this secondary objects
                sec_obj_to_eid_lst = sec_obj_to_eid_dict[each_obj]
                sec_obj_to_act_lst = sec_obj_to_act_dict[each_obj]
                # add the event in
                for i in range(0, len(sec_obj_to_eid_lst)):
                    # if the event is already in
                    if sec_obj_to_eid_lst[i] in evt_digraph.nodes:
                        # do not add the evt again
                        pass
                    else:
                        evt_digraph.add_node(sec_obj_to_eid_lst[i], label=sec_obj_to_act_lst[i])

                # add the edge
                for j in range(0, len(sec_obj_to_eid_lst) - 1):
                    evt_digraph.add_edge(sec_obj_to_eid_lst[j],
                                         sec_obj_to_eid_lst[j + 1],
                                         label=each_obj,
                                         color=color_lst[color_idx%20])
                color_idx += 1

        # ------------ add events related to sec obj type ------------
        case_dict[lead_obj] = evt_digraph
        case_idx_dict[lead_obj] = len(case_dict) - 1
        if len(case_dict) == 10:
            print(len(case_dict), time.time() - start_time)
        elif len(case_dict) == 100:
            print(len(case_dict), time.time() - start_time)
        elif len(case_dict) == 1000:
            print(len(case_dict), time.time() - start_time)
    return case_dict, case_idx_dict


def get_secondary_objects(ocel):
    # key is the object type, value is the set of correponding objects of this type
    all_obj_dict = {}

    # obj to obj type
    all_obj_to_type_dict = {}

    # get all the object types
    object_types = ocel.relations[ocel.object_type_column].unique().tolist()

    # classify all the obj to corresponding
    for ot in object_types:
        obj_ot_lst = ocel.relations[ocel.relations[ocel.object_type_column] == ot]['ocel:oid'].unique().tolist()
        all_obj_dict[ot] = obj_ot_lst
        # all obj to corresponding obj type
        for each_obj in obj_ot_lst:
            all_obj_to_type_dict[each_obj] = ot
    return all_obj_dict, all_obj_to_type_dict


def update_obj_to_keep(restrictions,
                       evt_lst,
                       act_lst,
                       evt_related_obj_dict,
                       obj_to_type_dict,
                       temp_sec_obj_dict):
    obj_to_keep_dict = {}
    obj_to_remove_dict = {}

    for each_restrictions_key, each_restrictions_val in restrictions.items():
        if each_restrictions_val[0] == 'coexist':
            obj_to_keep = set()
            # iterate each act in act list
            for i in range(0, len(act_lst)):
                # if the activity matches the target activity
                if act_lst[i] == each_restrictions_val[2]:
                    # get the related objects
                    for each_obj in evt_related_obj_dict[evt_lst[i]]:
                        if obj_to_type_dict[each_obj] == each_restrictions_val[1]:
                            obj_to_keep.add(each_obj)
            obj_to_keep_dict[each_restrictions_val[1]] = obj_to_keep

        else:
            obj_to_remove = set()
            # iterate each act in act list
            for i in range(0, len(act_lst)):
                # if the activity matches the target activity
                if act_lst[i] == each_restrictions_val[1]:
                    # get the related objects
                    for each_obj in evt_related_obj_dict[evt_lst[i]]:
                        if obj_to_type_dict[each_obj] == each_restrictions_val[2]:
                            obj_to_remove.add(each_obj)
            obj_to_remove_dict[each_restrictions_val[1]] = obj_to_remove
    # only keep the objects
    for k1, v1 in obj_to_keep_dict.items():
        temp_sec_obj_dict[k1] = set()
        temp_sec_obj_dict[k1] = v1
    # remove the objects

    # for k2,v2 in obj_to_remove_dict.items():
    #     temp_sec_obj_dict[k2] = temp_sec_obj_dict[k2] - v2
    return temp_sec_obj_dict
