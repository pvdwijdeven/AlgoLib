def bfs(graph_, start_node, end_node):
    if start_node not in graph_ or end_node not in graph_:
        return []
    visited = {start_node: None}
    queue = [start_node]
    while queue:
        node = queue.pop(0)
        if node == end_node:
            path = []
            while node is not None:
                path.append(node)
                node = visited[node]
            return path[::-1]
        for neighbour in graph_[node]:
            if neighbour not in visited:
                visited[neighbour] = node
                queue.append(neighbour)
    return []


def make_link(graph_, node1, node2, w):
    if node1 not in graph_:
        graph_[node1] = {}
    if node2 not in graph_[node1]:
        (graph_[node1])[node2] = 0
    (graph_[node1])[node2] += w
    if node2 not in graph_:
        graph_[node2] = {}
    if node1 not in graph_[node2]:
        (graph_[node2])[node1] = 0
    (graph_[node2])[node1] += w
    return graph_


def edge_to_graph(graph_, edge_):
    node1 = edge_[0]
    node2 = edge_[1]
    if node1 not in graph_:
        graph_[node1] = []
    if node2 not in graph_:
        graph_[node2] = []
    if node2 not in graph_[node1]:
        graph_[node1].append(node2)
    if node1 not in graph_[node2]:
        graph_[node2].append(node1)


############
#
# Test


def test():
    # shortcuts
    (a, b, c, d, e, f, g) = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
    triples = ((a, c, 3), (c, b, 10), (a, b, 15), (d, b, 9), (a, d, 4), (d, f, 7), (d, e, 3),
               (e, g, 1), (e, f, 5), (f, g, 2), (b, f, 1))
    graph = {}
    for (i, j, k) in triples:
        make_link(graph, i, j, k)

    print graph

    dist = bfs(graph, a, g)
    print dist

    graph2 = {}
    edges = [[1, 2], [1, 3], [2, 4], [4, 5], [3, 5]]
    for x in edges:
        edge_to_graph(graph2, x)

    print graph2

    dist = bfs(graph2, 1, 5)
    print dist


test()
