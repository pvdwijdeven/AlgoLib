def first_test(ar_a):
    # although same principle, a bit slower due to (extra) for-loops!!
    ar_b = []
    ar_a.sort()
    for x in ar_a:
        ar_b.append(x - K)
    total = 0
    start = 0
    max_b = ar_b[N - 1]
    for i, x in enumerate(ar_a):
        if x > max_b:
            break
        for j in xrange(start, N):
            if x == ar_b[j]:
                start = j + 1
                total += 1
                break
            elif x < ar_b[j]:
                start = j
                break
    print total


def second_test(ar_a):
    ar_a.sort()
    total = 0
    i = 0
    j = 1
    while j < N:
        if ar_a[i] > ar_a[j] - K:
            j += 1
        elif ar_a[i] < ar_a[j] - K:
            i += 1
        else:
            total += 1
            i += 1
            j += 1
    print total


N, K = map(int, raw_input().split())
A = map(int, raw_input().split())
