debug = 1 + 2 + 4 + 8 + 16 + 32 + 64 + 128 + 256 + 512 + 1024


class DColors:
    def __init__(self):
        pass

    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    NORMAL = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def dprint(level=0, color=DColors.NORMAL, *arg):
    if debug & level or level == -1:
        print color + ' '.join(map(str, arg)) + DColors.NORMAL  #


def main():
    for x in xrange(10):
        if debug & 2 ** x:
            print "Debug level:", x + 1, "is active"
        dprint(2 ** x, DColors.BLUE, "Debug printing level:", x + 1, "is active")

    # example:
    global debug
    debug = 4

    if debug & 2:
        print "Debug level 2 active"  # not active
        dprint(2, DColors.GREEN, "Debug level 2 printing is active")
        if debug & 4:
            print "Debug level 3 active"  # only this one is active now
        dprint(4, DColors.GREEN, "Debug level 3 printing is active")
        if debug & 8:
            print "Debug level 4 active"  # not active
        dprint(8, DColors.GREEN, "Debug level 4 printing is active")
        if debug:
            print "Debug active"  # active if debug != 0
        dprint(-1, DColors.GREEN, "Debug printing is active")


if __name__ == "__main__":
    main()
