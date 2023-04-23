import networkx as nx


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
    path, best_cost = nx.optimal_edit_paths(digraph1,
                          digraph2,
                          node_match=lambda a,b: a['label'] == b['label'],
                          node_del_cost=node_ins_del_cost,
                          node_subst_cost=node_subs_cost,
                          node_ins_cost=node_ins_del_cost,
                          edge_del_cost=edge_ins_del_cost,
                          edge_ins_cost=edge_ins_del_cost,
                          edge_subst_cost=edge_subst_cost)
    return path, best_cost

if __name__ == '__main__':
    digraph1 = nx.DiGraph()
    digraph1.add_node(1, label="1")
    digraph1.add_node(2, label="2")
    digraph1.add_node(3, label="3")
    digraph1.add_node(4, label="3")
    digraph1.add_node(5, label="4")
    digraph1.add_node(6, label="5")

    digraph1.add_edges_from([(1, 2), (2, 3), (3, 5), (2, 4), (4, 5), (5, 6)])

    digraph2 = nx.DiGraph()
    digraph2.add_node(1, label="1")
    digraph2.add_node(2, label="2")
    digraph2.add_node(3, label="2")
    digraph2.add_node(4, label="3")
    digraph2.add_node(5, label="3")
    digraph2.add_node(6, label="4")
    digraph2.add_node(7, label="4")
    digraph2.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 7)])

    # for edge in digraph1.edges:
    #     print(digraph1.nodes[edge[0]]['label'])

    path, best_cost = nx.optimal_edit_paths(digraph1,
                          digraph2,
                          node_match=lambda a,b: a['label'] == b['label'],
                          node_del_cost=node_ins_del_cost,
                          node_subst_cost=node_subs_cost,
                          node_ins_cost=node_ins_del_cost,
                          edge_del_cost=edge_ins_del_cost,
                          edge_ins_cost=edge_ins_del_cost,
                          edge_subst_cost=edge_subst_cost)

