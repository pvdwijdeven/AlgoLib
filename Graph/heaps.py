#
# heap building and inserting
#


def up_heapify(local_heap, node):
    cur_parent = parent(node)
    if local_heap[cur_parent] > local_heap[node]:
        local_heap[cur_parent], local_heap[node] = local_heap[node], local_heap[cur_parent]
        if cur_parent != 0:
            up_heapify(local_heap, cur_parent)
    return


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


# Call this routine if the heap rooted at i satisfies the heap property
# *except* perhaps i to its immediate children
def down_heapify(local_heap, i):
    # If i is a leaf, heap property holds
    if leaf(local_heap, i):
        return
    # If i has one child...
    if one_child(local_heap, i):
        # check heap property
        if local_heap[i] > local_heap[left(i)]:
            # if it fail, swap, fixing i and its child (a leaf)
            (local_heap[i], local_heap[left(i)]) = (local_heap[left(i)], local_heap[i])
        return
    # if i has two children...
    # check heap property
    if min(local_heap[left(i)], local_heap[right(i)]) >= local_heap[i]:
        return
    # If it fails, see which child is the smaller
    # and swap i's value into that child
    # Afterwards, recurse into that child, which might violate
    if local_heap[left(i)] < local_heap[right(i)]:
        # Swap into left child
        (local_heap[i], local_heap[left(i)]) = (local_heap[left(i)], local_heap[i])
        down_heapify(local_heap, left(i))
        return
    (local_heap[i], local_heap[right(i)]) = (local_heap[right(i)], local_heap[i])
    down_heapify(local_heap, right(i))
    return


def build_heap(local_list):
    local_heap = list(local_list)
    for i in range(len(local_heap) - 1, -1, -1):
        down_heapify(local_heap, i)
    return local_heap


def test():
    my_list = [16, 77, 72, 53, 62, 87, 17, 37, 32, 45]
    print my_list
    my_heap = build_heap(my_list)  # [16, 32, 17, 37, 45, 87, 72, 77, 53, 62]
    print my_heap
    my_heap.append(31)
    up_heapify(my_heap, len(my_heap) - 1)
    print my_heap  # [16, 31, 17, 37, 32, 87, 72, 77, 53, 62, 45]


test()
