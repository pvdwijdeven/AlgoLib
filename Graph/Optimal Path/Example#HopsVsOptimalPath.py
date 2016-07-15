#############
# first, construct the weighted graph
#

# a version of make_link that increments that
# value of the link if we make multiple nodes
#
# For the marvel graph, this will be used to count
# how many times character1 is in the same comic
# as character2


import csv
from collections import deque


def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    if node2 not in G[node1]:
        (G[node1])[node2] = 0
    (G[node1])[node2] += 1
    if node2 not in G:
        G[node2] = {}
    if node1 not in G[node2]:
        (G[node2])[node1] = 0
    (G[node2])[node1] += 1
    return G


# Reads the graph in CSV format.  Each line is in edge
# Keeps a list of characters
tsv = csv.reader(open("marvel.tsv"), delimiter='\t')

# loop through the raw data creating a bipartite graph
marvelG = {}
characters = set()
for (char, comic) in tsv:
    if char not in characters:
        characters.add(char)
    make_link(marvelG, char, comic)

# now, loop through the bipartite graph
# creating a graph of connected characters
# making a link (which increments the weight)
# everytime we see two characters in the same
# comic together
charG = {}
for char1 in characters:
    for book in marvelG[char1]:
        for char2 in marvelG[book]:
            # don't want to double count
            # so make this check
            if char1 < char2:
                make_link(charG, char1, char2)

# loop through charG and change the weights
# in charG to be inverse
for char1 in charG:
    char1 = charG[char1]
    for char2 in char1:
        char1[char2] = 1.0 / char1[char2]

################
# now find shortest paths
#

# here is an implementation of breadth first search
# which will be used to find the shortest path by hops


def bfs(G, node):
    final_dist = {node: (0, node, None)}
    # breadth first is a queue (fifo)
    # and so using deque is more efficient
    # then a list
    open_list = deque([node])
    while len(open_list) > 0:
        node = open_list.popleft()
        dist, _, _ = final_dist[node]
        for neighbor in G[node]:
            if neighbor in final_dist:
                continue
            final_dist[neighbor] = (dist + 1, neighbor, node)
            open_list.append(neighbor)
    return final_dist


# this is a standard implementation of dijkstras
# with one exception - the distance at each node
# is the sum of the edge weights along with the number
# of hops taken to get there.  This means
# that if two paths have the same distance, the one
# with the least number of hops will be selected
def left(i):
    return i * 2 + 1


def right(i):
    return i * 2 + 2


def parent(i):
    return (i - 1) / 2


def root(i):
    return i == 0


def leaf(local_heap, i):
    return right(i) >= len(local_heap) and left(i) >= len(local_heap)


def one_child(local_heap, i):
    return right(i) == len(local_heap)


def swap(heap, old, new, location):
    location[heap[old]] = new
    location[heap[new]] = old
    (heap[old], heap[new]) = (heap[new], heap[old])


# Call this routine if the heap rooted at i satisfies the heap property
# *except* perhaps i to its children immediate children
#
# location is a dictionary mapping an object to its location
# in the heap
def down_heapify(heap, i, location):
    # If i is a leaf, heap property holds
    while True:
        l = left(i)
        r = right(i)

        # see if we don't have any children
        if l >= len(heap):
            break

        v = heap[i][0]
        lv = heap[l][0]

        # If i has one child...
        if r == len(heap):
            # check heap property
            if v > lv:
                # If it fails, swap, fixing i and its child (a leaf)
                swap(heap, i, l, location)
            break

        rv = heap[r][0]
        # If i has two children...
        # check heap property
        if min(lv, rv) >= v:
            break
        # If it fails, see which child is the smaller
        # and swap i's value into that child
        # Afterwards, recurse into that child, which might violate
        if lv < rv:
            # Swap into left child
            swap(heap, i, l, location)
            i = l
        else:
            # swap into right child
            swap(heap, i, r, location)
            i = r


# Call this routine if whole heap satisfies the heap property
# *except* perhaps i to its parent
def up_heapify(heap, i, location):
    # If i is root, all is well
    while i > 0:
        # check heap property
        p = (i - 1) / 2
        if heap[i][0] < heap[p][0]:
            swap(heap, i, p, location)
            i = p
        else:
            break


# remove the minimum value:
def heappopmin(heap, location):
    val = heap[0]
    new_top = heap.pop()
    location[val] = None
    if len(heap) == 0:
        return val
    location[new_top] = 0
    heap[0] = new_top
    down_heapify(heap, 0, location)
    return val


# put a pair in the heap
def insert_heap(heap, v, location):
    heap.append(v)
    location[v] = len(heap) - 1
    up_heapify(heap, len(heap) - 1, location)


# decrease a value
def decrease_val(heap, location, old_val, new_val):
    i = location[old_val]
    heap[i] = new_val
    location[old_val] = None
    location[new_val] = i
    up_heapify(heap, i, location)


# increase a value
def increase_val(heap, location, old_val, new_val):
    i = location[old_val]
    heap[i] = new_val
    location[old_val] = None
    location[new_val] = i
    down_heapify(heap, i, location)


# when following an edge to a new node, need to
# add the distance and increment the hop-count
# this function accomplishes that
def add_dist(dista, tupleb):
    # adds dista to the distance of tupleb
    # and increments the hop-count of tupleb
    return (dista + tupleb[0], 1 + tupleb[1])


def dijkstra(graph, node):
    # (0, 0) is the initial weight - the value is zero and the hops are zero
    first_entry = ((0, 0), node, None)  # distance, node, parent/previous
    heap = [first_entry]
    # location is a dictionary that tracks the location of each entry
    location = {first_entry: 0}
    # dist_so_far is the frontier. A mapping of nodes we've explored
    # and the shortest paths we've seen so far to get there
    dist_so_far = {node: first_entry}
    # this is nodes we've fully explored
    final_dist = {}
    while len(dist_so_far) > 0:
        # find the closest un-explored node
        w = heappopmin(heap, location)
        # a stupid little optimization
        node = w[1]
        dist = w[0]

        # lock it down!
        del dist_so_far[node]
        # final_dist[node] = (dist, node, w.parent)
        final_dist[node] = w
        # look at its neighbors
        for x in graph[node]:
            # but only those that haven't been locked down
            if x not in final_dist:
                # for the marvel graph, dist is tuple
                # and graph[node][x] is just a number
                new_dist = add_dist(graph[node][x], dist)
                new_entry = (new_dist, x, node)
                if x not in dist_so_far:
                    # we haven't see this yet
                    # so add to the heap and the dictionary
                    dist_so_far[x] = new_entry
                    insert_heap(heap, new_entry, location)
                # this comparision uses the fact that
                # tuples are comparable
                elif new_entry < dist_so_far[x]:
                    # the new distance is less then the
                    # best known
                    # and then add a new entry
                    # for this node
                    decrease_val(heap, location, dist_so_far[x], new_entry)
                    dist_so_far[x] = new_entry
    return final_dist


# given a `dist` object (a mapping of a node to the shortest distance
# to that node and its parent) and a `target` node, return the path
# needed to get to the target
def get_parent(pair): return pair[2]


def find_path(dist, target):
    node = target
    path = [target]
    while True:
        prev = get_parent(dist[node])
        if prev is None:
            # We've rached our target, so return
            # the path
            return path
        path.append(prev)
        node = prev


# a list to store my answers in
answers = []  # store a tuple ((char1, char2), (char_path, hop_dist))

# the characters that the problem asks us to look at
chars = ['SPIDER-MAN/PETER PAR',
         'GREEN GOBLIN/NORMAN ',
         'WOLVERINE/LOGAN ',
         'PROFESSOR X/CHARLES ',
         'CAPTAIN AMERICA']

for char1 in chars:
    # calculate the distance to each other character
    char_dist = dijkstra(charG, char1)
    # and calculate the hops required
    hop_dist = bfs(charG, char1)

    for char2 in char_dist:
        if char1 == char2:
            continue
        char_path = find_path(char_dist, char2)
        hop_path = find_path(hop_dist, char2)
        # if the weighted path is longer then the hop path, we need
        # to save it
        if len(char_path) > len(hop_path):
            answers.append(((char1, char2), (char_path, hop_path)))

# and now we print out the answer
print len(answers)
