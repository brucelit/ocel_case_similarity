from pm4py.objects.ocel.util import *
import networkx as nx


def related_event_id_dict(ocel, object_types):
    dct = {}
    for ot in object_types:
        dct.update(ocel.relations[ocel.relations[ocel.object_type_column] == ot].groupby(ocel.object_id_column)[ocel.event_id_column].apply(
            list).to_dict())
    return dct


def related_event_activity_dict(ocel, object_types):
    dct = {}
    for ot in object_types:
        dct.update(ocel.relations[ocel.relations[ocel.object_type_column] == ot].groupby(ocel.object_id_column)[ocel.event_activity].apply(
            list).to_dict())
    return dct


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

    # for all events, get the related objs
    evt_related_obj_dict = related_objects.related_objects_dct_overall(ocel)

    # flatten all event of leading obj type
    df = flattening.flatten(ocel, lead_obj_type)

    # get the list of sec objects
    obj_dict = {}
    obj_evt_dict = {}
    sec_obj_lst = []
    for ot in rev_object_types:
        obj_dict[ot] = ocel.relations[ocel.relations[ocel.object_type_column] == ot]['ocel:oid'].unique().tolist()
        sec_obj_lst.extend(obj_dict[ot])

        # key: obj, value: list of related evts
        obj_evt_dict[ot] = ocel.relations[ocel.relations[ocel.object_type_column] == ot].groupby(ocel.object_id_column)[
            ocel.event_id_column].apply(
            list).to_dict()

    # keep all cases
    case_dict = {}

    # set obj to eid dictionary
    sec_obj_to_eid_dict = related_event_id_dict(ocel, rev_object_types)
    sec_obj_to_act_dict = related_event_activity_dict(ocel, rev_object_types)

    # iterate every object of leading type
    for lead_obj in lead_obj_lst:
        evt_digraph = nx.DiGraph()

        # get the list of events related to lead_obj
        lead_obj_to_act_lst = df[df['case:concept:name'] == lead_obj]['concept:name'].tolist()
        lead_obj_to_eid_lst = df[df['case:concept:name'] == lead_obj]['ocel:eid'].tolist()

        print(lead_obj_to_act_lst)
        # add the event id as node id
        for i in range(0, len(lead_obj_to_eid_lst)):
            evt_digraph.add_node(lead_obj_to_eid_lst[i], label=lead_obj_to_act_lst[i])

        # add the edge
        for j in range(0, len(lead_obj_to_eid_lst) - 2):
            evt_digraph.add_edge(lead_obj_to_eid_lst[j], lead_obj_to_eid_lst[j + 1])

        # # keep all sec objs with sec_obj_lst
        sec_obj_set = set()
        print("\n")
        for each_eid in lead_obj_to_eid_lst:
            for each_obj in evt_related_obj_dict[each_eid]:
                if each_obj in sec_obj_lst:
                    sec_obj_set.add(each_obj)
        print("len:", lead_obj, len(lead_obj_to_act_lst), len(sec_obj_set))

        # ------------ add events related to sec obj type ------------
        for each_obj in sec_obj_set:
            # get the list of events related to this sec_obj
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
            for j in range(0, len(sec_obj_to_eid_lst) - 2):
                evt_digraph.add_edge(sec_obj_to_eid_lst[j], sec_obj_to_eid_lst[j + 1])

        # ------------ add events related to sec obj type ------------
        case_dict[lead_obj] = evt_digraph

        if len(case_dict) > 10:
            break
    return case_dict
