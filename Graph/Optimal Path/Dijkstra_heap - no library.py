#
# heap building and inserting
#


# Heap shortcuts
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


#
# version of dijkstra implemented using a heap
#
# returns a dictionary mapping a node to the distance
# to that node
def dijkstra_heap(graph, a):
    # Distance to the input node is zero
    first_entry = (0, a)
    heap = [first_entry]
    # location keeps track of items in the heap
    # so that we can update their value later
    location = {first_entry: 0}
    # dist_so_far is kind of our 'frontier'
    # it keeps track of the nodes that we've seen so far
    # but aren't sure if we've found the shortest distance
    dist_so_far = {a: first_entry}
    # final_dist keeps track of the nodes that we've seen
    # and know that is the shortest distance
    final_dist = {}
    while len(dist_so_far) > 0:
        # grab the minimum value from the heap
        dist, node = heappopmin(heap, location)
        # lock it down!
        final_dist[node] = dist
        del dist_so_far[node]

        # examine the neighbors
        for x in graph[node]:
            if x in final_dist:
                # skip the ones we already have shortest
                # distances for
                continue
            new_dist = graph[node][x] + final_dist[node]
            new_entry = (new_dist, x)
            if x not in dist_so_far:
                # add to the heap
                insert_heap(heap, new_entry, location)
                dist_so_far[x] = new_entry
            elif new_entry < dist_so_far[x]:
                # we found a better way to this node, update heap
                decrease_val(heap, location, dist_so_far[x], new_entry)
                dist_so_far[x] = new_entry
    return final_dist


def build_heap(local_list):
    local_heap = list(local_list)
    location = {}
    for i in xrange(len(local_heap) - 1, -1, -1):
        down_heapify(local_heap, i, location)
    return local_heap


############
#
# Test

def make_link(mygraph, node1, node2, w):
    if node1 not in mygraph:
        mygraph[node1] = {}
    if node2 not in mygraph[node1]:
        (mygraph[node1])[node2] = 0
    (mygraph[node1])[node2] += w
    if node2 not in mygraph:
        mygraph[node2] = {}
    if node1 not in mygraph[node2]:
        (mygraph[node2])[node1] = 0
    (mygraph[node2])[node1] += w
    return mygraph


def test():
    # shortcuts
    (a, b, c, d, e, f, g) = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
    triples = ((a, c, 3), (c, b, 10), (a, b, 15), (d, b, 9), (a, d, 4), (d, f, 7), (d, e, 3),
               (e, g, 1), (e, f, 5), (f, g, 2), (b, f, 1))
    graph = {}
    for (i, j, k) in triples:
        make_link(graph, i, j, k)

    print graph

    dist = dijkstra_heap(graph, a)
    print dist
    assert dist[g] == 8  # (a -> d -> e -> g)
    assert dist[b] == 11  # (a -> d -> e -> g -> f -> b)


test()
