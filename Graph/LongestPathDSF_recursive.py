#
# Write centrality_max to return the maximum distance
# from a node to all the other nodes it can reach
#


def mark_node(graph, v, marked, level):
    marked[v] = level
    for x in graph[v]:
        if x not in marked:
            marked[x] = level
            mark_node(graph, x, marked, level + 1)
    return marked


def centrality_max(graph, v):
    # use DFS
    marked = mark_node(graph, v, {}, 0)
    return max(marked.values())


#################
# Testing code
#
def make_link(graph, node1, node2):
    if node1 not in graph:
        graph[node1] = {}
    (graph[node1])[node2] = 1
    if node2 not in graph:
        graph[node2] = {}
    (graph[node2])[node1] = 1
    return graph


def test():
    chain = ((1, 2), (2, 3), (3, 4), (4, 5), (5, 6))
    graph = {}
    for n1, n2 in chain:
        make_link(graph, n1, n2)
    assert centrality_max(graph, 1) == 5
    assert centrality_max(graph, 3) == 3
    tree = ((1, 2), (1, 3),
            (2, 4), (2, 5),
            (3, 6), (3, 7),
            (4, 8), (4, 9),
            (6, 10), (6, 11))
    graph = {}
    for n1, n2 in tree:
        make_link(graph, n1, n2)
    assert centrality_max(graph, 1) == 3
    assert centrality_max(graph, 11) == 6


test()
