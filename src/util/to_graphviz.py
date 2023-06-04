def generate_node_and_edge(g):
    str0 = f"digraph "" { " \
           "edge [len=3, minlen=3];" \
           "node [fixedsize=true,shape=rectangle];	"
    node_str = ''
    for each_node in g.nodes:
        str1 = str(each_node) + " " + "[label=\"" + g.nodes[each_node]["label"] + "\"];"
        node_str += str1
    print(node_str)

    edge_str = ''
    for each_edge in g.edges:
        str2 = str(each_edge[0]) + "->" + str(each_edge[1]) + \
               "[label=\"" + str(g.edges[each_edge]["label"]) + "\""+ \
                                                                " color=\"" + str(g.edges[each_edge]["color"]) + "\"];"
        edge_str += str2
    print(edge_str)

    final_str = str0 + node_str + edge_str + "}"
    return final_str
