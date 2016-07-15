def bfs(graph, start, end):
    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    queue.append([start])
    while queue:
        # get the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        # path found
        if node == end:
            return path
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        for adjacent in graph.get(node, []):
            new_path = list(path)
            new_path.append(adjacent)
            queue.append(new_path)


############
#
# Test

def make_link(mygraph, node1, node2, w):
    if node1 not in mygraph:
        mygraph[node1] = {}
    if node2 not in mygraph[node1]:
        (mygraph[node1])[node2] = 0
    (mygraph[node1])[node2] += w
    if node2 not in mygraph:
        mygraph[node2] = {}
    if node1 not in mygraph[node2]:
        (mygraph[node2])[node1] = 0
    (mygraph[node2])[node1] += w
    return mygraph


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


test()