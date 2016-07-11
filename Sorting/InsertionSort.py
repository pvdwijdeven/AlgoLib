#!/bin/python
def printarray(ar1_, ar2_):
    for x in ar1_:
        print x,
    for x in ar2_:
        print x,
    print


def sortarray(ar_):
    for x in xrange(len(ar_) - 1, 0, -1):
        if ar_[x] < ar_[x - 1]:
            ar_[x], ar_[x - 1] = ar_[x - 1], ar_[x]
        else:
            break


def insertion_sort(ar1_, ar2_):
    e = ar2_[0]
    ar2_.pop(0)
    ar1_.append(e)
    sortarray(ar1_)
    printarray(ar1_, ar2_)
    return ar1_, ar2_


m = input()
ar2 = [int(i) for i in raw_input().strip().split()]
ar1 = [ar2[0]]
ar2.pop(0)
while ar2: 
    ar1, ar2 = insertion_sort(ar1, ar2)
