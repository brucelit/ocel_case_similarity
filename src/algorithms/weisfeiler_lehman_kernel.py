import networkx as nx


def update_hash_label_vec(digraph1, 
                          digraph2,
                          label_dict_for_digraph1,
                          label_dict_for_digraph2):
    '''
    Return an updated vector of the hash label

    Parameters
    ----------
    G: graph
        The graph to be hashed.
        Can have node and/or edge attributes. Can also have no attributes.
    edge_attr: string, default=None
        The key in edge attribute dictionary to be used for hashing.
        If None, edge labels are ignored.
    node_attr: string, default=None
        The key in node attribute dictionary to be used for hashing.
        If None, and no edge_attr given, use the degrees of the nodes as labels.
    iterations: int, default=3
        Number of neighbor aggregations to perform.
        Should be larger for larger graphs.
    digest_size: int, default=16
        Size (in bits) of blake2b hash digest to use for hashing node labels.
        The default size is 16 bits

    Returns
    -------
    new dictionary : dict
        A dictionary with each key given by a node in G, and each value given
        by the hashes in order of depth from the key node.
    '''

    # iterate each node in digraph1, check whether the new label is in dict
    for each_node in digraph1.nodes:
        if digraph1.nodes[each_node]['label'] not in label_dict_for_digraph1:
            label_dict_for_digraph1[digraph1.nodes[each_node]['label']] = 1
        else:
            label_dict_for_digraph1[digraph1.nodes[each_node]['label']] += 1

    # iterate each node in digraph1, check whether the new label is in dict
    for each_node in digraph2.nodes:
        if digraph2.nodes[each_node]['label'] not in label_dict_for_digraph2:
            label_dict_for_digraph2[digraph2.nodes[each_node]['label']] = 1
        else:
            label_dict_for_digraph2[digraph2.nodes[each_node]['label']] += 1

    return label_dict_for_digraph1, label_dict_for_digraph2

def get_similarity_score(label_dict_for_digraph1, label_dict_for_digraph2):
    '''
    Return the similarity score of two different graph

    Parameters
    ----------
    G: graph
        The graph to be hashed.
        Can have node and/or edge attributes. Can also have no attributes.
    edge_attr: string, default=None
        The key in edge attribute dictionary to be used for hashing.
        If None, edge labels are ignored.
    node_attr: string, default=None
        The key in node attribute dictionary to be used for hashing.
        If None, and no edge_attr given, use the degrees of the nodes as labels.
    iterations: int, default=3
        Number of neighbor aggregations to perform.
        Should be larger for larger graphs.
    digest_size: int, default=16
        Size (in bits) of blake2b hash digest to use for hashing node labels.
        The default size is 16 bits

    Returns
    -------
    new dictionary : dict
        A dictionary with each key given by a node in G, and each value given
        by the hashes in order of depth from the key node.
    '''
    # change the dict to two vector
    score = sum(label_dict_for_digraph1[k] * label_dict_for_digraph2[k]
                for k in label_dict_for_digraph1.keys()&label_dict_for_digraph2.keys())
    return score


def get_normalized_similarity_score(digraph1, digraph2, int_id, iteration=1):
    '''
    Return the normzalized similarity score of two different graph

    '''
    label_dict_for_digraph1, label_dict_for_digraph2, possible_label_dict = {}, {}, {}
    update_hash_label_vec(digraph1, digraph2, label_dict_for_digraph1,label_dict_for_digraph2)

    for idx in range(0, iteration):
        #   relabel the label of the digraph
        #  get all the predecessors and successors of digraph1

        to_change_digraph1 = {}
        to_change_digraph2 = {}

        for each_node in digraph1.nodes:
            pre_lst = []
            for each_pre in digraph1.predecessors(each_node):
                pre_lst.append(digraph1.nodes[each_pre]['label'])
            suc_lst = []
            for each_suc in digraph1.successors(each_node):
                suc_lst.append(digraph1.nodes[each_suc]['label'])
            pre_suc_lst = (digraph1.nodes[each_node]['label'], tuple(pre_lst), tuple(suc_lst))
            if pre_suc_lst not in possible_label_dict:
                int_id += 1
                possible_label_dict[pre_suc_lst] = int_id
                to_change_digraph1[each_node] = int_id
            else:
                # print(each_node, pre_suc_lst, "new label:", possible_label_dict[pre_suc_lst])
                to_change_digraph1[each_node] = possible_label_dict[pre_suc_lst]

        # print("  ----------   ")
        for each_node in digraph2.nodes:
            pre_lst = []
            for each_pre in digraph2.predecessors(each_node):
                pre_lst.append(digraph2.nodes[each_pre]['label'])
            suc_lst = []
            for each_suc in digraph2.successors(each_node):
                suc_lst.append(digraph2.nodes[each_suc]['label'])
            pre_suc_lst = (digraph2.nodes[each_node]['label'], tuple(pre_lst), tuple(suc_lst))
            if pre_suc_lst not in possible_label_dict:
                int_id += 1
                possible_label_dict[pre_suc_lst] = int_id
                to_change_digraph2[each_node] = int_id
                # print(each_node, pre_suc_lst, "new label:", int_id)
            else:
                # print(each_node, pre_suc_lst, "new label:", possible_label_dict[pre_suc_lst])
                to_change_digraph2[each_node] = possible_label_dict[pre_suc_lst]

        for k, v in to_change_digraph1.items():
            digraph1.nodes[k]['label'] = v

        for k, v in to_change_digraph2.items():
            digraph2.nodes[k]['label'] = v

        # for node in digraph1.nodes:
        #     print(node, digraph1.nodes[node])

        # print("-----------")
        # for node in digraph2.nodes:
        #     print(node, digraph2.nodes[node])
        # update the label dictionary for both graph
        update_hash_label_vec(digraph1, digraph2, label_dict_for_digraph1, label_dict_for_digraph2)
    score = get_similarity_score(label_dict_for_digraph1, label_dict_for_digraph2)
    return score


def update_hash_label():
    '''
    update the label label of two diff graph
    :return:
    '''
    return 1
    # return digraph1, dg


def translate_evt_to_int_id(digraph1, digraph2):
    # translate the event to label
    evt_label_dict ={}
    int_id = 0
    for each_node in digraph1.nodes:
        if digraph1.nodes[each_node]['label'] not in evt_label_dict:
            evt_label_dict[digraph1.nodes[each_node]['label']] = int_id
            int_id += 1
    for each_node in digraph2.nodes:
        if digraph2.nodes[each_node]['label'] not in evt_label_dict:
            evt_label_dict[digraph2.nodes[each_node]['label']] = int_id
            int_id += 1

    for each_node in digraph1.nodes:
        digraph1.nodes[each_node]['label'] = evt_label_dict[digraph1.nodes[each_node]['label']]

    for each_node2 in digraph2.nodes:
        digraph2.nodes[each_node2]['label'] = evt_label_dict[digraph2.nodes[each_node2]['label']]
    return digraph1, digraph2, len(evt_label_dict)


if __name__ == '__main__':
    digraph1 = nx.DiGraph()
    digraph1.add_node(1, label="1")
    digraph1.add_node(2, label="2")
    digraph1.add_node(3, label="3")
    digraph1.add_node(4, label="3")
    digraph1.add_node(5, label="4")
    digraph1.add_edges_from([(1, 2), (2, 3), (3, 5), (2, 4), (4, 5)])

    digraph2 = nx.DiGraph()
    digraph2.add_node(1, label="1")
    digraph2.add_node(2, label="2")
    digraph2.add_node(3, label="2")
    digraph2.add_node(4, label="3")
    digraph2.add_node(5, label="3")
    digraph2.add_node(6, label="4")
    digraph2.add_node(7, label="4")
    digraph2.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 7)])

    dg3 = nx.DiGraph()
    dg3.add_node(1, label="evt1")
    dg3.add_node(2, label="evt2")
    dg3.add_node(3, label="evt3")
    dg3.add_node(4, label="evt3")
    dg3.add_node(5, label="evt4")
    dg3.add_edges_from([(1, 2), (2, 3), (3, 5), (2, 4), (4, 5)])

    dg4 = nx.DiGraph()
    dg4.add_node(1, label="evt4")
    dg4.add_node(2, label="evt6")
    dg4.add_node(3, label="evt6")
    dg4.add_node(4, label="evt6")
    dg4.add_node(5, label="evt5")
    dg4.add_edges_from([(1, 2), (2, 3), (3, 5), (2, 4), (4, 5)])

    dg_trans1, dg_trans2, label_num = translate_evt_to_int_id(dg3, dg4)
    score = get_normalized_similarity_score(dg_trans1, dg_trans2, label_num)

    dg_trans3, dg_trans4, label_num = translate_evt_to_int_id(dg3, dg4)
    score1 = get_normalized_similarity_score(dg_trans3, dg_trans3, label_num)
    score2 = get_normalized_similarity_score(dg_trans4, dg_trans4, label_num)
    temp_score = max(score1, score2)

    print(score,score1,score2,score/temp_score)
