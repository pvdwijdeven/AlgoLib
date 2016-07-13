# See also https://classroom.udacity.com/courses/cs215/lessons/48739297/concepts/487491120923
# retrieve top K of list size n:

# Selection/Insertion: use when K=logn,loglogn or 100
# sort:				 use when K=n/2,sqrt(n) or logn

# retrieve unsorted top K of list size n:

# partitioning (theta(n)):
import random


# given absolute is minimized when x = median of L (?)
def minimize_absolute(mylist):
    return max(top_k(mylist, 1 + len(mylist) / 2, False))


def partition(mylist, v):
    smaller = []
    bigger = []
    same = []
    for val in mylist:
        if val < v:
            smaller.append(val)
        if val == v:
            same.append(val)
        if val > v:
            bigger.append(val)
    return smaller, same, [v], bigger


def top_k(mylist, k, top):
    v = mylist[random.randrange(len(mylist))]
    if top:
        (right, m_duplicates, middle, left) = partition(mylist, v)
    else:
        (left, m_duplicates, middle, right) = partition(mylist, v)
    if len(left) == k:
        return left
    if (len(left) < k) and (len(left) + len(m_duplicates) > k):  # can fill list up with duplicates
        some_list = left + [v] * (k - len(left))
        return some_list
    if len(left) > k:
        return top_k(left, k, top)
    if len(left) + len(m_duplicates) == k:
        return left + m_duplicates
    return left + m_duplicates + top_k(right, k - len(left) - len(m_duplicates), top)


# L = [1,2,3,4,5,6,5,2]
# print minimize_absolute(L)


def test_top_k():
    test_list = [random.randint(0, 100) for _ in xrange(100)]
    print top_k(test_list, 50, True)
    print top_k(test_list, 50, False)

    print minimize_absolute(test_list)
    test_list.sort()
    print test_list[len(test_list) / 2]


test_top_k()
