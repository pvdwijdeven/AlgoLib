# first set debug level
# -1 = general debug when debug != 0
# 1 = create spanning tree
# 2 = post order
# 4 = number of descendants
# 8 = lowest post order
# 16 = highest post order
# 32 = bridge edges
# 64 = test cases
# 128 = main test case

debug = 1 + 2 + 4 + 8 + 16 + 32 + 128


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


# Now some utility functions
#


def make_link(graph, node1, node2, r_or_g):
    # modified make_link to apply
    # a color to the edge instead of just 1
    if node1 not in graph:
        graph[node1] = {}
    (graph[node1])[node2] = r_or_g
    if node2 not in graph:
        graph[node2] = {}
    (graph[node2])[node1] = r_or_g
    return graph


def get_children(spanning_tree, root, parent):
    """returns the children from following the
    green edges"""
    return [n for n, e in spanning_tree[root].items()
            if ((not n == parent) and
                (e == 'green'))]


def get_children_all(spanning_tree, root, parent):
    """returns the children from following
    green edges and the children from following
    red edges"""
    green = []
    red = []
    for n, e in spanning_tree[root].items():
        if n == parent:
            continue
        if e == 'green':
            green.append(n)
        if e == 'red':
            red.append(n)
    return green, red


#################

def create_rooted_spanning_tree(graph, root):
    # use DFS from the root to add edges and nodes
    # to the tree.  The first time we see a node
    # the edge is green, but after that its red
    dprint(1, DColors.BLUE, "start create_rooted_spanning_tree:")
    todo_list = [root]
    spanning_tree = {root: {}}
    while todo_list:
        node = todo_list.pop()
        dprint(1, DColors.NORMAL, "node:", node, "open_list:", todo_list)
        neighbors = graph[node]
        for n in neighbors:
            if n not in spanning_tree:
                # we haven't seen this node, so
                # need to use a green edge to connect
                # it
                make_link(spanning_tree, node, n, 'green')
                todo_list.append(n)
            else:
                # we have seen this node,
                # but, first make sure that
                # don't already have the edge
                # in spanning_tree
                if node not in spanning_tree[n]:
                    make_link(spanning_tree, node, n, 'red')
    dprint(1, DColors.BLUE, "done create_rooted_spanning_tree:\n", spanning_tree)
    return spanning_tree


##################

def _post_order(spanning_tree, root, parent, val, po):
    children = get_children(spanning_tree, root, parent)
    for c in children:
        val = _post_order(spanning_tree, c, root, val, po)
        dprint(2, DColors.NORMAL, "node:", root, "child:", c, "value:", val)
    po[root] = val
    return val + 1


def post_order(spanning_tree, root):
    dprint(2, DColors.BLUE, "start post_order:")
    po = {}
    _post_order(spanning_tree, root, None, 1, po)
    dprint(2, DColors.BLUE, "done post_order:\n", po)
    return po


##################

def _number_descendants(spanning_tree, root, parent, nd):
    # number of descendants is the
    # sum of the number of descendants of a nodes
    # children plus one
    children = get_children(spanning_tree, root, parent)
    nd_val = 1
    for c in children:
        # recursively calculate the number of descendants
        # for the children
        nd_val += _number_descendants(spanning_tree, c, root, nd)
    nd[root] = nd_val
    dprint(4, DColors.NORMAL, "node:", root, "value:", nd_val)
    return nd_val


def number_of_descendants(spanning_tree, root):
    dprint(4, DColors.BLUE, "start number_of_descendants:")
    nd = {}
    _number_descendants(spanning_tree, root, None, nd)
    dprint(4, DColors.BLUE, "end number_of_descendants:", nd)
    return nd


#
# Since highest and lowest post order will follow
# a similar method, I only wrote one method
# that can be used for both
#
def _general_post_order(spanning_tree, root, parent, po, gpo, comp):
    green, red = get_children_all(spanning_tree, root, parent)
    val = po[root]
    for c in green:
        # recursively find the low/high post order value of the children
        test = _general_post_order(spanning_tree, c, root, po, gpo, comp)
        # and save the low/highest one
        if comp(val, test):
            val = test
    for c in red:
        test = po[c]
        # and also look at the direct children
        # from following red edges
        # and save the low/highest one if needed
        if comp(val, test):
            val = test
    gpo[root] = val
    dprint(8 + 16, DColors.NORMAL, "root:", root, "value:", val)
    return val


def lowest_post_order(spanning_tree, root, po):
    dprint(8, DColors.BLUE, "start lowest_post_order:")
    lpo = {}
    _general_post_order(spanning_tree, root, None, po, lpo, lambda x, y: x > y)
    dprint(8, DColors.BLUE, "end lowest_post_order:\n", lpo)
    return lpo


def highest_post_order(spanning_tree, root, po):
    dprint(16, DColors.BLUE, "start highest_post_order:")
    hpo = {}
    _general_post_order(spanning_tree, root, None, po, hpo, lambda x, y: x < y)
    dprint(16, DColors.BLUE, "end highest_post_order:\n", hpo)
    return hpo


#
# Now put everything together
#

def bridge_edges(graph, root):
    dprint(32, DColors.BLUE, "start bridge_edges:")
    spanning_tree = create_rooted_spanning_tree(graph, root)
    po = post_order(spanning_tree, root)
    nd = number_of_descendants(spanning_tree, root)
    lpo = lowest_post_order(spanning_tree, root, po)
    hpo = highest_post_order(spanning_tree, root, po)
    bridges = []
    open_list = [(root, None)]
    # walk down the tree and see which edges are
    # tree edges
    while len(open_list) > 0:
        node, parent = open_list.pop()
        for child in get_children(spanning_tree, node, parent):
            # all of these edges are automatically green (get_children only
            # follows green edges)
            # so only need to check the other two conditions
            dprint(32, DColors.NORMAL, "child:", child, "po:", po[child], "hpo", hpo[child], "lpo:", lpo[child], "nd:",
                   nd[child], "bridge:",
                   hpo[child] <= po[child] and lpo[child] > (po[child] - nd[child]))
            if hpo[child] <= po[child] and lpo[child] > (po[child] - nd[child]):
                bridges.append((node, child))
            open_list.append((child, node))
    dprint(32, DColors.BLUE, "end bridge_edges:\n", bridges)
    return bridges


# ***** test functions *****

def test_create_rooted_spanning_tree():
    graph = {'a': {'c': 1, 'b': 1},
             'b': {'a': 1, 'd': 1},
             'c': {'a': 1, 'd': 1},
             'd': {'c': 1, 'b': 1, 'e': 1},
             'e': {'d': 1, 'g': 1, 'f': 1},
             'f': {'e': 1, 'g': 1},
             'g': {'e': 1, 'f': 1}
             }
    spanning_tree = create_rooted_spanning_tree(graph, "a")
    assert spanning_tree == {'a': {'c': 'green', 'b': 'green'},
                             'b': {'a': 'green', 'd': 'green'},
                             'c': {'a': 'green', 'd': 'red'},
                             'd': {'c': 'red', 'b': 'green', 'e': 'green'},
                             'e': {'d': 'green', 'g': 'green', 'f': 'green'},
                             'f': {'e': 'green', 'g': 'red'},
                             'g': {'e': 'green', 'f': 'red'}
                             }


def test_post_order():
    spanning_tree = {'a': {'c': 'green', 'b': 'green'},
                     'b': {'a': 'green', 'd': 'red'},
                     'c': {'a': 'green', 'd': 'green'},
                     'd': {'c': 'green', 'b': 'red', 'e': 'green'},
                     'e': {'d': 'green', 'g': 'green', 'f': 'green'},
                     'f': {'e': 'green', 'g': 'red'},
                     'g': {'e': 'green', 'f': 'red'}
                     }
    po = post_order(spanning_tree, 'a')
    assert po == {'a': 7, 'c': 5, 'b': 6, 'e': 3, 'd': 4, 'g': 1, 'f': 2}


def test_number_of_descendants():
    spanning_tree = {'a': {'c': 'green', 'b': 'green'},
                     'b': {'a': 'green', 'd': 'red'},
                     'c': {'a': 'green', 'd': 'green'},
                     'd': {'c': 'green', 'b': 'red', 'e': 'green'},
                     'e': {'d': 'green', 'g': 'green', 'f': 'green'},
                     'f': {'e': 'green', 'g': 'red'},
                     'g': {'e': 'green', 'f': 'red'}
                     }
    nd = number_of_descendants(spanning_tree, 'a')
    assert nd == {'a': 7, 'b': 1, 'c': 5, 'd': 4, 'e': 3, 'f': 1, 'g': 1}


def test_lowest_post_order():
    spanning_tree = {'a': {'c': 'green', 'b': 'green'},
                     'b': {'a': 'green', 'd': 'red'},
                     'c': {'a': 'green', 'd': 'green'},
                     'd': {'c': 'green', 'b': 'red', 'e': 'green'},
                     'e': {'d': 'green', 'g': 'green', 'f': 'green'},
                     'f': {'e': 'green', 'g': 'red'},
                     'g': {'e': 'green', 'f': 'red'}
                     }
    po = post_order(spanning_tree, 'a')
    l = lowest_post_order(spanning_tree, 'a', po)
    assert l == {'a': 1, 'c': 1, 'b': 4, 'e': 1, 'd': 1, 'g': 1, 'f': 1}


def test_highest_post_order():
    spanning_tree = {'a': {'c': 'green', 'b': 'green'},
                     'b': {'a': 'green', 'd': 'red'},
                     'c': {'a': 'green', 'd': 'green'},
                     'd': {'c': 'green', 'b': 'red', 'e': 'green'},
                     'e': {'d': 'green', 'g': 'green', 'f': 'green'},
                     'f': {'e': 'green', 'g': 'red'},
                     'g': {'e': 'green', 'f': 'red'}
                     }
    po = post_order(spanning_tree, 'a')
    h = highest_post_order(spanning_tree, 'a', po)
    assert h == {'a': 7, 'c': 6, 'b': 6, 'e': 3, 'd': 6, 'g': 2, 'f': 2}


def test_bridge_edges():
    graph = {'a': {'c': 1, 'b': 1},
             'b': {'a': 1, 'd': 1},
             'c': {'a': 1, 'd': 1},
             'd': {'c': 1, 'b': 1, 'e': 1},
             'e': {'d': 1, 'g': 1, 'f': 1},
             'f': {'e': 1, 'g': 1},
             'g': {'e': 1, 'f': 1}
             }
    bridges = bridge_edges(graph, 'a')
    assert bridges == [('d', 'e')]


if debug & 64:
    dprint(64, DColors.GREEN, "\n***** testing create rooted spanning tree *****")
    test_create_rooted_spanning_tree()
    dprint(64, DColors.GREEN, "\n***** testing post order *****")
    test_post_order()
    dprint(64, DColors.GREEN, "\n***** testing number of descendants *****")
    test_number_of_descendants()
    dprint(64, DColors.GREEN, "\n***** testing lowest post order *****")
    test_lowest_post_order()
    dprint(64, DColors.GREEN, "\n***** testing highest post order *****")
    test_highest_post_order()
if debug & 128:
    dprint(128, DColors.GREEN, "\n***** testing bridge edges *****")
    test_bridge_edges()
