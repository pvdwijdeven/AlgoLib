class Graph(object):
    """
    Author: Pascal van de Wijdeven
    Date:  18-08-2016
    Ver:   0.1

    includes:
    - create graph from edges
    - create graph from matrix
    - shortest path (BFS)
    - get directions from path
    """

    def __init__(self, graph=None, bidirectional=True):
        self.bidirectional = bidirectional
        self.nodes = set()
        self._parent__graph = {}
        self.graph = graph
        self.diagonals = False

    @property
    def graph(self):
        return self._parent__graph

    @graph.setter
    def graph(self, graph):
        if graph is not None:
            self._parent__graph = graph
        else:
            self._parent__graph = {}
        if self._parent__graph != {}:
            for x in self._parent__graph:
                self.nodes.add(x)
                for y in self._parent__graph[x]:
                    self.nodes.add(y)


class WeightedGraph(Graph):
    def __init__(self, graph=None, bidirectional=True):
        Graph.__init__(self, graph, bidirectional)

    def add_nodes(self, node1, node2, weight):
        self.nodes.add(node1)
        self.nodes.add(node2)
        if node1 not in self._parent__graph:
            self._parent__graph[node1] = {}
        if node2 not in self._parent__graph[node1]:
            self._parent__graph[node1][node2]=weight

    def create_graph_from_matrix(self, matrix, road, obstacles, diagonals=False):
        # todo: create weighted graph from node distance in matrix
        """

        Create a graph from a matrix structure
        :param matrix: matrix as nested list: [[0,0,0],[1,1,0],[0,1,0]]
        :param obstacles: list of obstacles to be ignored: [1]
        :param diagonals: use diagonals as edge or not?, default False
        :return: Nothing
        """
        self._parent__graph = {}
        self.nodes = set()
        self.diagonals = diagonals
        rows = len(matrix)
        cols = len(matrix[0])
        self.nodes = set()
        self._parent__graph = {}
        for r in xrange(rows):
            for c in xrange(cols):
                if matrix[r][c] in obstacles:
                    continue
                else:
                    node = (matrix[r][c], r, c)
                    if r > 0:
                        node2val = matrix[r - 1][c]
                        node2name = (node2val, r - 1, c)
                        if node2val not in obstacles:
                            self.add_nodes(node, node2name)
                        if diagonals:
                            if c > 0:
                                node2val = matrix[r - 1][c - 1]
                                node2name = (node2val, r - 1, c - 1)
                                if node2val not in obstacles:
                                    self.add_nodes(node, node2name)
                            if c < cols - 1:
                                node2val = matrix[r - 1][c + 1]
                                node2name = (node2val, r - 1, c + 1)
                                if node2val not in obstacles:
                                    self.add_nodes(node, node2name)
                    if c > 0:
                        node2val = matrix[r][c - 1]
                        node2name = (node2val, r, c - 1)
                        if node2val not in obstacles:
                            self.add_nodes(node, node2name)
                    if c < cols - 1:
                        node2val = matrix[r][c + 1]
                        node2name = (node2val, r, c + 1)
                        if node2val not in obstacles:
                            self.add_nodes(node, node2name)
                    if r < rows - 1:
                        node2val = matrix[r + 1][c]
                        node2name = (node2val, r + 1, c)
                        if node2val not in obstacles:
                            self.add_nodes(node, node2name)
                        if diagonals:
                            if c > 1:
                                node2val = matrix[r + 1][c - 1]
                                node2name = (node2val, r + 1, c - 1)
                                if node2val not in obstacles:
                                    self.add_nodes(node, node2name)
                            if c < cols - 1:
                                node2val = matrix[r + 1][c + 1]
                                node2name = (node2val, r + 1, c + 1)
                                if node2val not in obstacles:
                                    self.add_nodes(node, node2name)

    def create_graph_from_edges(self, edges):
        """
        Create a graph from a list of edges
        :param edges: list of edges: [[1,2,weight],[2,3,weight],[1,3,weight]]
        :return: Nothing
        """
        self._parent__graph={}
        self.nodes=set()
        for edge in edges:
            node1 = edge[0]
            node2 = edge[1]
            weight = edge[2]
            self.add_nodes(node1,node2,weight)
            if self.bidirectional:
                self.add_nodes(node2, node1, weight)

    def get_neighbours(self, node):
        """
        Show neighbours of node
        :param node: node to be examined
        :return: list of neighbours
        """
        if node not in self._parent__graph:
            return []
        else:
            return self._parent__graph[node]

    def shortest_path(self, start_node, end_node):
        """
        Returns shortest path from start to end node
        :param start_node: node, should be in self.graph/nodes
        :param end_node: node, should be in self.graph/nodes
        :return: ordered list of nodes showing shortest path
        """
        if start_node not in self._parent__graph or end_node not in self._parent__graph:
            return []
        visited = {start_node: None}
        queue = [start_node]
        while queue:
            node = queue.pop(0)
            if node == end_node:
                path = []
                while node is not None:
                    path.append(node)
                    node = visited[node]
                return path[::-1]
            for neighbour in self._parent__graph[node]:
                if neighbour not in visited:
                    visited[neighbour] = node
                    queue.append(neighbour)
        return []

    def get_directions(self, path, north="N", south="S", east="E", west="W", northeast="NE", northwest="NW",
                       southeast="SE", southwest="SW"):
        """
        Creates directions from path (obtained from shortest path)
        :param path: list of nodes showing path
        :param north: characters to be added when going north
        :param south: characters to be added when going south
        :param east: characters to be added when going east
        :param west: characters to be added when going west
        :param northeast: characters to be added when going northeast (when diagonals=True)
        :param northwest: characters to be added when going northwest (when diagonals=True)
        :param southeast: characters to be added when going southeast (when diagonals=True)
        :param southwest: characters to be added when going southwest (when diagonals=True)
        :return: string of directions
        """
        directions = ""
        for i in xrange(1, len(path)):
            if path[i][1] > path[i - 1][1]:
                if self.diagonals:
                    if path[i][2] == path[i - 1][2]:
                        directions += south
                    elif path[i][2] > path[i - 1][2]:
                        directions += southeast
                    elif path[i][2] < path[i - 1][2]:
                        directions += southwest
                else:
                    directions += south
            elif path[i][1] < path[i - 1][1]:
                if self.diagonals:
                    if path[i][2] == path[i - 1][2]:
                        directions += north
                    elif path[i][2] > path[i - 1][2]:
                        directions += northeast
                    elif path[i][2] < path[i - 1][2]:
                        directions += northwest
                else:
                    directions += north
            elif path[i][2] > path[i - 1][2]:
                directions += east
            elif path[i][2] < path[i - 1][2]:
                directions += west
        return directions


# example:
def test():
    test_graph = WeightedGraph({1: {2:1, 3:2}, 2: {4:2, 5:1}})
    print test_graph.nodes
    print test_graph.graph
    print
    test_graph.bidirectional=False
    test_graph.create_graph_from_edges([[1, 2,1], [2, 3,1], [1, 4,1]])
    print test_graph.nodes
    print test_graph.graph
    print
    #test_graph.create_graph_from_matrix([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                         # [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                                         # [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                                         # [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                                         # [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
                                         # [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                                         # [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1],
                                         # [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1],
                                         # [1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1],
                                         # [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1],
                                         # [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
                                         # [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]], [1], False)
    #print test_graph.nodes
    #print test_graph.graph
    #print test_graph.get_directions(test_graph.shortest_path((0, 1, 1), (0, 10, 10)))


test()
