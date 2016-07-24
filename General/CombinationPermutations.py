import math

def nCr(n,r):
    f = math.factorial
    return f(n) / (f(r) * f(n-r))

def nPr(n,r):
    f = math.factorial
    return f(n) / f(n-r)