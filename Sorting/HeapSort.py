#
# Implement remove_min
#


def remove_min(mylist):
    # your code here
    mylist.pop(0)
    down_heapify(mylist,0)
    return mylist


def parent(node):
    return (node - 1) / 2


def left_child(node):
    return 2 * node + 1


def right_child(node):
    return 2 * node + 2


def is_leaf(mylist, node):
    return (left_child(node) >= len(mylist)) and (right_child(node) >= len(mylist))


def one_child(mylist, node):
    return (left_child(node) < len(mylist)) and (right_child(node) >= len(mylist))


# Call this routine if the heap rooted at i satisfies the heap property
# *except* perhaps i to its immediate children
def down_heapify(mylist, node):
    # If node is a leaf, heap property holds
    if is_leaf(mylist, node):
        return
    # If node has one child...
    if one_child(mylist, node):
        # check heap property
        if mylist[node] > mylist[left_child(node)]:
            # If it fails, swap, fixing node and its child (a leaf)
            (mylist[node], mylist[left_child(node)]) = (mylist[left_child(node)], mylist[node])
        return
    # If node has two children...
    # check heap property
    if min(mylist[left_child(node)], mylist[right_child(node)]) >= mylist[node]:
        return
    # If it fails, see which child is the smaller
    # and swap node's value into that child
    # Afterwards, recurse into that child, which might violate
    if mylist[left_child(node)] < mylist[right_child(node)]:
        # Swap into left child
        (mylist[node], mylist[left_child(node)]) = (mylist[left_child(node)], mylist[node])
        down_heapify(mylist, left_child(node))
        return
    else:
        (mylist[node], mylist[right_child(node)]) = (mylist[right_child(node)], mylist[node])
        down_heapify(mylist, right_child(node))
        return


#########
# Testing Code
#

# build_heap
def build_heap(mylist):
    for node in range(len(mylist) - 1, -1, -1):
        down_heapify(mylist, node)
    return mylist


def test():
    mylist = range(10)
    build_heap(mylist)
    print mylist
    remove_min(mylist)
    print mylist
    # now, the new minimum should be 1
    assert mylist[0] == 1

test()