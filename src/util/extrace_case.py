from pm4py.objects.ocel.util import *
import networkx as nx


def extract_case_with_leading_type(ocel, lead_obj_type, rev_object_types=None):
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
    lead_obj_lst = ocel.objects[ocel.objects[ocel.object_type_column] == lead_obj_type][
        "ocel:oid"].values.flatten().tolist()
    # flatten all event of leading obj type
    df = flattening.flatten(ocel, lead_obj_type)

    # get all events related to sec obj types
    sec_obj_evt_lst = []
    for each_sec_obj_type in rev_object_types:
        sec_obj_evt_lst.append(related_objects.related_objects_dct_per_type(ocel)[each_sec_obj_type])

    # keep all cases
    case_dict = {}

    # iterate every object of leading type
    for lead_obj in lead_obj_lst:
        evt_digraph = nx.DiGraph()

        # get the list of events related to lead_obj
        lead_obj_to_act_lst = df[df['case:concept:name'] == lead_obj]['concept:name'].tolist()
        lead_obj_to_eid_lst = df[df['case:concept:name'] == lead_obj]['ocel:eid'].tolist()

        # add the event id as node id
        for i in range(0, len(lead_obj_to_eid_lst)):
            evt_digraph.add_node(lead_obj_to_eid_lst[i], label=lead_obj_to_act_lst[i])

        # add the edge
        for j in range(0, len(lead_obj_to_eid_lst) - 2):
            evt_digraph.add_edge(lead_obj_to_eid_lst[j], lead_obj_to_eid_lst[j + 1])

        # keep all sec objs
        sec_obj_lst=[]
        for i in lead_obj_to_eid_lst:
            for each_dict in sec_obj_evt_lst:
                if i in each_dict:
                    print("有的：",i, each_dict[i])

        # ------------ add events related to sec obj type ------------
        for each_obj in sec_obj_lst:
            # get the list of events related to this sec_obj
            sec_obj_to_act_lst = df[df['case:concept:name'] == each_obj]['concept:name'].tolist()
            sec_obj_to_eid_lst = df[df['case:concept:name'] == each_obj]['ocel:eid'].tolist()

            # add the event in
            for i in range(0, len(sec_obj_to_eid_lst)):
                # if the event is already in
                if sec_obj_to_eid_lst[i] in evt_digraph.nodes:
                    # do not add the evt again
                    pass
                else:
                    evt_digraph.add_node(sec_obj_to_eid_lst[i], label=sec_obj_to_act_lst[i])

            # add the edge
            for j in range(0, len(lead_obj_to_eid_lst) - 2):
                evt_digraph.add_edge(sec_obj_to_eid_lst[j], sec_obj_to_eid_lst[j + 1])
        # ------------ add events related to sec obj type ------------
        case_dict[lead_obj] = evt_digraph

        if len(case_dict) > 5:
            break

    return case_dict
