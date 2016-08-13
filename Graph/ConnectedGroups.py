def node_name(row, column):
    return str(row) + str(column)


def get_loc(nodename):
    return int(nodename[:1]), int(nodename[1:])


def create_graph():
    nodes = {}
    graph = {}
    conns = {}
    for cat in xrange(1, 6):
        # only look right and down
        nodes[cat] = []
        graph[cat] = []
        conns[cat] = {}
        for r in xrange(rows):
            for c in xrange(columns):
                if grid[r][c] == cat:
                    curnode = node_name(r, c)
                    nodes[cat].append(curnode)
                    if curnode not in conns[cat]:
                        conns[cat][curnode] = []
                    if c + 1 < columns:
                        if grid[r][c + 1] == cat:
                            adjnode = node_name(r, c + 1)
                            graph[cat].append([curnode, adjnode])
                            conns[cat][curnode].append(adjnode)
                            if adjnode not in conns[cat]:
                                conns[cat][adjnode] = []
                            conns[cat][adjnode].append(curnode)
                    if r + 1 < rows:
                        if grid[r + 1][c] == cat:
                            adjnode = node_name(r + 1, c)
                            graph[cat].append([curnode, adjnode])
                            conns[cat][curnode].append(adjnode)
                            if adjnode not in conns[cat]:
                                conns[cat][adjnode] = []
                            conns[cat][adjnode].append(curnode)
    return nodes, graph, conns


def mark_node(node, marked, group, cat):
    for x in conns[cat][node]:
        if x not in marked[cat]:
            marked[cat][x] = group
            mark_node(x, marked, group, cat)
    marked[cat][node] = group
    return marked


def create_groups():
    marked = {}
    for cat in xrange(1, 6):
        todo = list(nodes[cat])
        marked[cat] = {}
        group = 0
        while todo:
            mark_node(todo[0], marked, group, cat)
            for x in nodes[cat]:
                if x in marked[cat]:
                    if x in todo:
                        todo.remove(x)
                        # if debug & 4:
                        # print marked
                        # print todo
            group += 1
    return marked


def get_biggest(group_):
    mlist=[]

    for cat in xrange(1,6):
        vallist = group_[cat].values()
        try:
            mx = max(vallist)
            mxlist = [0] * (mx + 1)
            for x in vallist:
                mxlist[x - 1] += 1
        except ValueError:
            mxlist=[0]
        mlist.append([max(mxlist),cat])
    print max(mlist, key=lambda x: x[0])
    return max(mlist, key=lambda x: x[0])



def checkio(matrix):
    global grid
    grid=matrix
    global rows,columns
    rows=len(matrix)
    columns=len(matrix[0])
    global nodes,graph,conns
    nodes, graph, conns = create_graph()
    groups = create_groups()
    return get_biggest(groups)



# These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert checkio([
        [1, 2, 3, 4, 5],
        [1, 1, 1, 2, 3],
        [1, 1, 1, 2, 2],
        [1, 2, 2, 2, 1],
        [1, 1, 1, 1, 1]
    ]) == [14, 1], "14 of 1"

    assert checkio([
        [2, 1, 2, 2, 2, 4],
        [2, 5, 2, 2, 2, 2],
        [2, 5, 4, 2, 2, 2],
        [2, 5, 2, 2, 4, 2],
        [2, 4, 2, 2, 2, 2],
        [2, 2, 4, 4, 2, 2]])
    
    
#fast way:
from collections import defaultdict
from itertools import chain, product
​
def checkio(matrix):
    numgroups = defaultdict(list)
    for y, x in product(*map(range, map(len, (matrix, matrix[0])))):
        groups = numgroups[matrix[y][x]]
        links = [g for g in groups if g & {(y - 1, x), (y, x - 1)}]
        for g in links: groups.remove(g)
        groups += [{(y, x)} | set(chain(*links))]
​
    return max([max(map(len, numgroups[n])), n] for n in numgroups if n)
