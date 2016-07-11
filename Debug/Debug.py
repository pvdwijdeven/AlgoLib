debug = 1 + 2 + 4 + 8 + 16 + 32 + 64 + 128 + 256 + 512 + 1024

for x in xrange(10):
    if debug & 2 ** x:
        print "Debug level:", x + 1, "is active"

# example:
debug = 4

if debug & 2:
    print "Debug level 2 active"  # not active
if debug & 4:
    print "Debug level 3 active"  # only this one is active now
if debug & 8:
    print "Debug level 4 active"  # not active
if debug:
    print "Debug active"  # active if debug > 0
