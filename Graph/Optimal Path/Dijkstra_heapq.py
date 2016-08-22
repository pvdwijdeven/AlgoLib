from heapq import *


def findNeighbors(vertex,n,grid):
    rows,cols=n,n
    i, j = vertex[0], vertex[1]
    output = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]  # all neighbors
    remove = []
    for v in output:
        if v[0] < 0 or v[0] > rows - 1 or v[1] < 0 or v[1] > cols - 1:
            remove.append(v)
    final = [(grid[x], x) for x in output if not x in remove]
    return final


def dijkstra_min(g, f, t):
    q, seen = [(0, f, ())], set()
    while q:
        (cost, v1, path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == t: return (cost, path)

            for c, v2 in g.get(v1, ()):
                if v2 not in seen:
                    heappush(q, (cost + c, v2, path))

    return float("inf")


def test():
    n = input()
    grid = {}
    counter = 0
    for line in xrange(n):
        temp = map(int, raw_input().split())
        for a in range(len(temp)):
            grid[(counter, a)] = int(temp[a])
        counter += 1
    neigh = {}
    for x in grid:
        neigh[x] = findNeighbors(x,n,grid)
    print dijkstra(neigh, (0, 0), (n - 1, n - 1))[0] + grid[(0, 0)]


test()