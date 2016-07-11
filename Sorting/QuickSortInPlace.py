def quicksort(ar_, lo, hi):
    if lo < hi:
        p = partition(ar_, lo, hi)
        quicksort(ar_, lo, p - 1)
        quicksort(ar_, p + 1, hi)


def partition(ar_, lo, hi):
    pivot = ar_[hi]
    i = lo
    for j in xrange(lo, hi):
        if ar_[j] <= pivot:
            ar_[i], ar_[j] = ar_[j], ar_[i]
            i += 1
    ar_[i], ar_[hi] = ar_[hi], ar_[i]
    for x in ar_:
        print x,
    print
    return i


m = input()
ar = map(int, raw_input().split())
quicksort(ar, 0, len(ar) - 1)
