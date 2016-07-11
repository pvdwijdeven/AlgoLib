def find_eulerian_tour(graph):
    tour = []
    find_tour(1, graph, tour)
    return tour


def find_tour(current_node, eulerian_graph, tour):
    for (node1, node2) in eulerian_graph:
        if node1 == current_node:
            eulerian_graph.remove((node1, node2))
            find_tour(node2, eulerian_graph, tour)
        elif node2 == current_node:
            eulerian_graph.remove((node1, node2))
            find_tour(node1, eulerian_graph, tour)
    tour.append(current_node)