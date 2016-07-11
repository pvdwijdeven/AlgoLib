n = input()
ar = []
xlist = [''] * 100
for i in xrange(n):
    x, y = raw_input().split()
    if i < n / 2:
        y = '-'
    xlist[int(x)] += ' ' + y
for x in xlist:
    print x.strip(),
    
