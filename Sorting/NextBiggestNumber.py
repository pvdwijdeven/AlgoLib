T = input()

for t in xrange(T):
    w = raw_input()
    w = list(w)
    pivot = -1
    for i in xrange(len(w) - 1, 0, -1):
        if ord(w[i]) > ord(w[i - 1]):
            pivot = i - 1
            break
    if pivot == -1:
        print "no answer"
    else:
        minc = 'z'
        for j in xrange(pivot + 1, len(w)):
            if minc >= w[j] > w[pivot]:
                minc = w[j]
                minp = j
        w[pivot], w[minp] = w[minp], w[pivot]
        x = len(w)
        halfway = (x - pivot - 1) / 2

        for i in xrange(0, halfway):
            w[i + pivot + 1], w[x - i - 1] = w[x - i - 1], w[i + pivot + 1]
        print ''.join(w)
