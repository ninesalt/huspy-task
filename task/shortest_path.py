import networkx as nx


def get_shortest_path(edges, start, end):
    g = nx.Graph()
    g.add_edges_from(edges)

    try:
        return nx.shortest_path(g, start, end)
    except nx.exception.NetworkXNoPath:
        return None
