def find_matrix_neighbors(matrix, rows, cols=-1,obstacles=None):
    """
    Finds direct neighbors of all nodes, regardless of contents
    :param matrix: dictionary with node name (x,y) as key and value as value
    :param rows: number of rows
    :param cols: number of columns, if omitted, same as rows
    :param obstacles: when matrix value in obstacle, object is not counted as node or neighbour
    :return: unweighted graph with nodes (x,y) as key and neighbours as values
    """
    if obstacles==None:
        obstacles=[]
    if cols == -1:
        cols = rows
    graph = {}
    for vertex in matrix:
        if matrix[vertex] in obstacles:
            continue
        i, j = vertex[0], vertex[1]
        output = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]  # all neighbors
        remove = []
        for v in output:
            if v[0] < 0 or v[0] > rows - 1 or v[1] < 0 or v[1] > cols - 1:
                remove.append(v)
        final = [x for x in output if x not in remove and matrix[x] not in obstacles]
        graph[vertex] = final
    return graph


def read_matrix(rows, filename=""):
    """
    Read matrix from file, or if filename omitted from console
    :param rows: number of rows
    :param filename: filename
    :return: dictionary containing elements (x,y) of matrix with value
    """
    matrix = {}
    el = 0
    if filename != "":
        f = open(filename)
    else:
        f = None
    for row in xrange(rows):
        if filename == "":
            line = map(int, raw_input().split())
        else:
            line = map(int, f.readline().split())
        for el, element in enumerate(line):
            matrix[(row, el)] = element
    if filename != "":
        f.close()
    return matrix, el


def test():
    n = input()
    matrix, cols = read_matrix(n)
    graph = find_matrix_neighbors(matrix, n,obstacles=[2])
    print graph


test()
