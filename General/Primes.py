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
	

def main():
    primes = get_all_primes_to_limit(10000)
    print primes


if __name__ == "__main__":
    main()
