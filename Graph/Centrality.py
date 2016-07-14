#
# Write centrality_max to return the maximum distance
# from a node to all the other nodes it can reach
#
import random
import csv


def mark_node(graph_, v, marked, level):
    marked[v] = level
    for x in graph_[v]:
        if x not in marked:
            marked[x] = level
            mark_node(graph_, x, marked, level + 1)
    return marked


def bfs_iterative_levels(graph_, root):
    visited = {root: 0}
    todo = [root]
    while todo:
        cur_node = todo.pop(0)
        for child in graph_[cur_node]:
            if child not in visited:
                todo.append(child)
                visited[child] = visited[cur_node] + 1
    return visited


def centrality_max(graph_, v):
    # use DFS
    marked = bfs_iterative_levels(graph_, v)
    return max(marked.values())


def centrality_min(graph_, v):
    # use DFS
    marked = bfs_iterative_levels(graph_, v)
    return min(marked.values())


def centrality_avg(graph_, v):
    # use DFS
    marked = bfs_iterative_levels(graph_, v)
    return sum(marked.values()) / float(len(marked.values()) - 1)


def make_link(graph_, node1, node2):
    if node1 not in graph_:
        graph_[node1] = {}
    (graph_[node1])[node2] = 1
    if node2 not in graph_:
        graph_[node2] = {}
    (graph_[node2])[node1] = 1
    return graph_


def rank(my_list, v):
    r = 0
    for l in my_list:
        if l < v:
            r += 1
    return r


def find_rank(my_list, i):
    lt = {}
    eq = {}
    gt = {}
    v = random.choice(my_list.keys())
    for l in my_list.keys():
        if my_list[l] < my_list[v]:
            lt[l] = my_list[l]
        elif my_list[l] == my_list[v]:
            eq[l] = my_list[l]
        elif my_list[l] > my_list[v]:
            gt[l] = my_list[l]
    if len(lt) >= i:
        return find_rank(lt, i)
    elif len(lt) + len(eq) >= i:
        return v
    else:
        return find_rank(gt, i - len(lt) - len(eq))


def read_graph(filename):
    tsv = csv.reader(open(filename), delimiter='\t')
    graph_ = {}
    actors_ = {}
    movies_ = {}
    for (actor_, movie_name, year) in tsv:
        movie = str(movie_name) + ", " + str(year)
        actors_[actor_] = 1
        movies_[movie] = 1
        make_link(graph_, actor_, movie)
    return graph_, actors_, movies_


graph, actors, movies = read_graph("actors.tsv")
cen_dict = {}
for actor in actors:
    cen_dict[actor] = centrality_avg(graph, actor)
actor_index = find_rank(cen_dict, 20)
print actor_index
print cen_dict[actor_index]
