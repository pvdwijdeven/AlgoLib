#
# Shortest path via Dijkstra (use for sparse graphs - small edge/node ratio, else use Floyd-Warshall
#


def shortest_dist_node(dist):
    best_node = 'undefined'
    best_value = 10**18  # make sure this is bigger than any max edge value
    for v in dist:
        if dist[v] < best_value:
            (best_node, best_value) = (v, dist[v])
    return best_node


def linear_dijkstra(my_graph, v):
    dist_so_far = {v: 0}
    final_dist = {}
    while len(final_dist) < len(my_graph):
        w = shortest_dist_node(dist_so_far)
        # lock it down!
        final_dist[w] = dist_so_far[w]
        del dist_so_far[w]
        for x in my_graph[w]:
            if x not in final_dist:
                if x not in dist_so_far:
                    dist_so_far[x] = final_dist[w] + my_graph[w][x]
                elif final_dist[w] + my_graph[w][x] < dist_so_far[x]:
                    dist_so_far[x] = final_dist[w] + my_graph[w][x]
    return final_dist


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

    dist = linear_dijkstra(graph, a)

    assert dist[g] == 8  # (a -> d -> e -> g)
    assert dist[b] == 11  # (a -> d -> e -> g -> f -> b)


test()
