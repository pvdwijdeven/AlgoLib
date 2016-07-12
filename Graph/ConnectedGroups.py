debug = 1 + 4


def get_input():
    if debug & 2:
        rows_, columns_ = 4, 4
        grid_ = [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [1, 0, 0, 0]]
    else:
        rows_ = input()
        columns_ = input()
        grid_ = []
        for _ in xrange(rows_):
            grid_.append(map(int, raw_input().split()))
    return rows_, columns_, grid_


def node_name(row, column):
    return str(row) + str(column)


def get_loc(nodename):
    return int(nodename[:1]), int(nodename[1:])


def create_graph():
    # only look right and down
    nodes_ = []
    graph_ = []
    conns_ = {}
    for r in xrange(rows):
        for c in xrange(columns):
            if grid[r][c] == 1:
                curnode = node_name(r, c)
                nodes_.append(curnode)
                if curnode not in conns_:
                    conns_[curnode] = []
                if c + 1 < columns:
                    if grid[r][c + 1] == 1:
                        adjnode = node_name(r, c + 1)
                        graph_.append([curnode, adjnode])
                        conns_[curnode].append(adjnode)
                        if adjnode not in conns_:
                            conns_[adjnode] = []
                        conns_[adjnode].append(curnode)
                if r + 1 < rows:
                    if grid[r + 1][c] == 1:
                        adjnode = node_name(r + 1, c)
                        graph_.append([curnode, adjnode])
                        conns_[curnode].append(adjnode)
                        if adjnode not in conns_:
                            conns_[adjnode] = []
                        conns_[adjnode].append(curnode)
                if r + 1 < rows and c + 1 < columns:
                    if grid[r + 1][c + 1] == 1:
                        adjnode = node_name(r + 1, c + 1)
                        graph_.append([curnode, adjnode])
                        conns_[curnode].append(adjnode)
                        if adjnode not in conns_:
                            conns_[adjnode] = []
                        conns_[adjnode].append(curnode)
                if r + 1 < rows and c - 1 >= 0:
                    if grid[r + 1][c - 1] == 1:
                        adjnode = node_name(r + 1, c - 1)
                        graph_.append([curnode, adjnode])
                        conns_[curnode].append(adjnode)
                        if adjnode not in conns_:
                            conns_[adjnode] = []
                        conns_[adjnode].append(curnode)
    return nodes_, graph_, conns_


def mark_node(node, marked, group):
    for x in conns[node]:
        if x not in marked:
            marked[x] = group
            mark_node(x, marked, group)
    marked[node] = group
    return marked


def create_groups():
    todo = list(nodes)
    marked = {}
    group = 0
    while todo:
        marked = mark_node(todo[0], marked, group)
        for x in nodes:
            if x in marked:
                if x in todo:
                    todo.remove(x)
        if debug & 4:
            print marked
            print todo
        group += 1
    return marked


def get_biggest(group_):
    vallist = group_.values()
    mx = max(vallist)
    mxlist = [0] * (mx + 1)
    for x in vallist:
        mxlist[x - 1] += 1
    return max(mxlist)


rows, columns, grid = get_input()
nodes, graph, conns = create_graph()
groups = create_groups()
if debug & 4:
    print nodes
    print graph
    print conns
    print groups
print get_biggest(groups)
