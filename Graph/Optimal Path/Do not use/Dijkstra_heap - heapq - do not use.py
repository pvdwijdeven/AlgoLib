#
# Shortest path via Dijkstra (use for sparse graphs - small edge/node ratio, else use Floyd-Warshall
#


import heapq


def val(pair):
    return pair[0]


def id_(pair):
    return pair[1]


def dijkstra(graph, v):
    heap = [[0, v]]
    dist_so_far = {v: [0, v]}
    final_dist = {}
    while len(final_dist) < len(graph):
        # find the closest un-explored node
        while True:
            w = heapq.heappop(heap)
            # grab the relevant parts of w
            node = id_(w)
            dist = val(w)
            if node != 'REMOVED':
                del dist_so_far[node]
                break

        # lock it down!
        final_dist[node] = dist
        # look at its neighbors
        for x in graph[node]:
            # but only those that haven't been locked down
            if x not in final_dist:
                new_dist = dist + graph[node][x]
                new_entry = [new_dist, x]
                if x not in dist_so_far:
                    # we haven't see this yet
                    # so add to the heap and the dictionary
                    dist_so_far[x] = new_entry
                    heapq.heappush(heap, new_entry)
                elif new_dist < val(dist_so_far[x]):
                    # the new distance is less then the
                    # best known
                    # Instead of removing it from the heap
                    # which could be expensive, mark it
                    dist_so_far[x][1] = "REMOVED"
                    # and then add a new entry
                    # for this node
                    dist_so_far[x] = new_entry
                    heapq.heappush(heap, new_entry)
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

    dist = dijkstra(graph, a)

    assert dist[g] == 8  # (a -> d -> e -> g)
    assert dist[b] == 11  # (a -> d -> e -> g -> f -> b)


test()
