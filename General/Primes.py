def get_list_of_10000_primes():
    limit = 104729  # this is the 10000th prime
    if limit % 2 != 0:
        limit += 1
    primes_ = [True] * limit
    primes_[0], primes_[1] = [None] * 2
    for ind, val in enumerate(primes_):
        if val is True:
            # sieve out non-primes by multiples of known primes
            primes_[ind * 2::ind] = [False] * (((limit - 1) // ind) - 1)
    return primes_


def get_all_primes_to_limit(limit):
    primes_ = []
    sieve_list = get_list_of_10000_primes()
    for i in xrange(limit+1):
        if sieve_list[i]:
            primes_.append(i)
    return primes_


def primes(n):
    """ Returns  a list of primes < n """
    sieve = [True] * n
    for i in xrange(3,int(n**0.5)+1,2):
        if sieve[i]:
            sieve[i*i::2*i]=[False]*((n-i*i-1)/(2*i)+1)
    return [2] + [i for i in xrange(3,n,2) if sieve[i]]
	
# for big prime numbers:
def _try_composite(a, d, n, s):
    if pow(a, d, n) == 1:
        return False
    for i in range(s):
        if pow(a, 2 ** i * d, n) == n - 1:
            return False
    return True  # n  is definitely composite


def is_prime(n, _precision_for_huge_n=16):
    if n in _known_primes or n in (0, 1):
        return True
    if any((n % p) == 0 for p in _known_primes):
        return False
    d, s = n - 1, 0
    while not d % 2:
        d, s = d >> 1, s + 1
    # Returns exact according to http://primes.utm.edu/prove/prove2_3.html
    if n < 1373653:
        return not any(_try_composite(a, d, n, s) for a in (2, 3))
    if n < 25326001:
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5))
    if n < 118670087467:
        if n == 3215031751:
            return False
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7))
    if n < 2152302898747:
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11))
    if n < 3474749660383:
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13))
    if n < 341550071728321:
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13, 17))
    # otherwise
    return not any(_try_composite(a, d, n, s)
                   for a in _known_primes[:_precision_for_huge_n])


_known_primes = [2, 3]
_known_primes += [x for x in range(5, 1000, 2) if is_prime(x)]




def main():
    primes = get_all_primes_to_limit(10000)
    print primes


if __name__ == "__main__":
    main()
