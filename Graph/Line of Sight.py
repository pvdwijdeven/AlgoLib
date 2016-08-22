from math import sqrt
from heapq import *


def line_of_sight(node1, node2, matrix, obstacles):
    """
    # returns line of sight length between 2 nodes, 0 if no sight
    :param node1: first node
    :param node2: second node
    :param matrix: dict with (x,y) as nodes and val as value
    :param obstacles: list of obstacles (values in matrix)
    :return: length of LoS (0 if none)
    """
    # line formula: y=ax+b
    y1, x1 = node1
    y2, x2 = node2
    x_start = min(x1, x2)
    x_end = max(x1, x2)
    y_start = min(y1, y2)
    y_end = max(y1, y2)
    x1 += 0.5
    x2 += 0.5
    y1 += 0.5
    y2 += 0.5
    if x1 != x2:
        a = (y1 - y2) / float(x1 - x2)
        b = y1 - a * x1

    for x in xrange(x_start, x_end + 1):
        for y in xrange(y_start, y_end + 1):
            node = (y, x)
            if matrix[node] in obstacles:
                if x1 == x2:
                    return 0
                else:
                    if y <= a * x + b <= y + 1 or y <= a * (x + 1) + b <= y + 1:
                        return 0
                    if x <= (y - b) / float(a) <= x + 1 or x <= (y + 1 - b) / float(a) <= x + 1:
                        return 0
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def dijkstra_min(g, f, t):
    """
    # return shortest path
    :param g: graph
    :param f: start point
    :param t: target point
    :return: (cost,shortest path)
    """
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


def checkio(bunker):
    matrix = {}
    bats = []
    los_dict = {}
    start=(0,0)
    # get bats
    for row, line in enumerate(bunker):
        for col, element in enumerate(line):
            matrix[(row, col)] = element
            if element == 'B' or element == 'A':
                bats.append((row, col))
                los_dict[(row, col)] = []
            if element == 'A':
                target = (row, col)
    # make bats-map, neighbors should be in line of sight
    for b1 in xrange(len(bats)):
        for b2 in xrange(b1 + 1, len(bats)):
            los = line_of_sight(bats[b1], bats[b2], matrix, ['W'])
            if los > 0:
                los_dict[bats[b1]].append((los, bats[b2]))
                los_dict[bats[b2]].append((los, bats[b1]))
    return dijkstra_min(los_dict, start, target)[0]


# These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    def almost_equal(checked, correct, significant_digits=2):
        precision = 0.1 ** significant_digits
        return correct - precision < checked < correct + precision


    assert almost_equal(checkio([
        "B--",
        "---",
        "--A"]), 2.83), "1st example"
    assert almost_equal(checkio([
        "B-B",
        "BW-",
        "-BA"]), 4), "2nd example"
    assert almost_equal(checkio([
        "BWB--B",
        "-W-WW-",
        "B-BWAB"]), 12), "3rd example"
    assert almost_equal(checkio([
        "B---B-",
        "-WWW-B",
        "-WA--B",
        "-W-B--",
        "-WWW-B",
        "B-BWB-"]), 9.24), "4th example"
    assert almost_equal(checkio([
        "B-B--B-",
        "-W-W-W-",
        "--B---B",
        "BW-W-W-",
        "----A--",
        "BW-W-W-",
        "-B--B-B"]), 16), "5th"
