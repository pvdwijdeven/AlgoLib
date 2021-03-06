import time

debug = 1 + 2 + 4 + 8 + 16 + 32 + 64 + 128 + 256 + 512 + 1024


class DColors:
    def __init__(self):
        pass

    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    NORMAL = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def dprint(level=0, color=DColors.NORMAL, *arg):
    if debug & level or level == -1:
        print color + ' '.join(map(str, arg)) + DColors.NORMAL  #


# ***** get_children when parent is know *****


def get_children(graph, root, parent):
    return [node for node in graph[root].keys()
            if (not node == parent)]


# ***** Depth first searches when path known *****
# DFS iterative is faster than recursive
# for recursive > 1000, try sys.setrecursionlimit
# if tree is very deep, BFS will be faster than DFS
# if tree is very wide, DFS will be faster than BFS
# binary tree -> BFS is faster


def dfs_iterative(graph, root):
    visited = [root]
    todo = [root]
    while todo:
        cur_node = todo.pop(0)
        for child in graph[cur_node]:
            if child not in visited:
                todo = [child] + todo
                visited.append(child)
    return visited


def dfs_recursive(graph, start, visited=None):
    if visited is None:
        visited = []
    visited.append(start)
    for child in graph[start]:
        if child not in visited:
            dfs_recursive(graph, child, visited)
    return visited


# ***** getting list of children and list of parents using DFS *****


def dfs_get_all_children(graph, root):
    visited = [root]
    children = {}
    todo = [root]
    while todo:
        cur_node = todo.pop(0)
        children[cur_node] = []
        for child in graph[cur_node]:
            if child not in visited:
                todo = [child] + todo
                children[cur_node].append(child)
                visited.append(child)
    return children


def dfs_get_all_parents(graph, root):
    visited = [root]
    parents = {}
    todo = [root]
    while todo:
        cur_node = todo.pop(0)
        for child in graph[cur_node]:
            if child not in visited:
                todo = [child] + todo
                parents[child] = cur_node
                visited.append(child)
    return parents


# ***** Breadth first searches when path known *****


def bfs_iterative(graph, root):
    visited = [root]
    todo = [root]
    while todo:
        cur_node = todo.pop(0)
        for child in graph[cur_node]:
            if child not in visited:
                todo.append(child)
                visited.append(child)
    return visited


# ***** getting list of children and list of parents using BFS *****


def bfs_get_all_children(graph, root):
    visited = [root]
    children = {}
    todo = [root]
    while todo:
        cur_node = todo.pop(0)
        children[cur_node] = []
        for child in graph[cur_node]:
            if child not in visited:
                todo.append(child)
                children[cur_node].append(child)
                visited.append(child)
    return children


def bfs_get_all_parents(graph, root):
    visited = [root]
    parents = {}
    todo = [root]
    while todo:
        cur_node = todo.pop(0)
        for child in graph[cur_node]:
            if child not in visited:
                todo.append(child)
                parents[child] = cur_node
                visited.append(child)
    return parents


# ***** test cases *****


def create_tree(depth=10):
    tree = {}
    todo = {}
    cur_depth = 0
    todo[0] = ["0"]
    #    tree["0"]=[]
    while cur_depth < depth:
        todo[cur_depth + 1] = []
        while todo[cur_depth]:
            cur_node = todo[cur_depth].pop(0)
            tree[cur_node] = []
            tree[cur_node].append(cur_node + str(0))
            tree[cur_node].append(cur_node + str(1))
            tree[cur_node + str(0)] = [cur_node]
            tree[cur_node + str(1)] = [cur_node]
            todo[cur_depth + 1].append(cur_node + str(0))
            todo[cur_depth + 1].append(cur_node + str(1))
        cur_depth += 1
    return tree


def test_searches():
    graph1 = {'a': {'c': 1, 'b': 1},
              'b': {'a': 1, 'd': 1},
              'c': {'a': 1},
              'd': {'b': 1, 'e': 1},
              'e': {'d': 1, 'g': 1, 'f': 1},
              'f': {'e': 1},
              'g': {'e': 1}
              }
    graph2 = {'A': {'B', 'C'},
              'B': {'A', 'D', 'E'},
              'C': {'A'},
              'D': {'B'},
              'E': {'B', 'F'},
              'F': {'E'}}
    graph3 = create_tree(14)
    if debug&1:
        print dfs_iterative(graph1, 'a')  # ['a', 'b', 'd', 'e', 'f', 'g', 'c']
        print dfs_recursive(graph1, 'a')
        print dfs_iterative(graph2, 'A')  # ['A', 'B', 'D', 'E', 'F', 'C']
        print dfs_recursive(graph2, 'A')
        print bfs_iterative(graph1, 'a')  # ['a', 'c', 'b', 'd', 'e', 'g', 'f']
        print bfs_iterative(graph2, 'A')  # ['A', 'C', 'B', 'E', 'D', 'F']
    print "start iterative DFS graph3"
    start_time = time.time()
    dfs_iterative(graph3, '0')
    print "end iterative DFS graph3", time.time() - start_time  # for tree(14): 11.6600000858(s)
    print "start recursive DFS graph3"
    start_time = time.time()
    dfs_recursive(graph3, '0')
    print "end recursive DFS graph3", time.time() - start_time  # for tree(14): 10.7320001125(s)
    print "start iterative BFS graph3"
    start_time = time.time()
    bfs_iterative(graph3, '0')
    print "end iterative BFS graph3", time.time() - start_time  # for tree(14): 4.50199985504(s)
    # print dfs_get_all_parents(graph1, 'a')
    # print dfs_get_all_parents(graph2, 'A')
    # print dfs_get_all_parents(graph3, '0')


test_searches()
