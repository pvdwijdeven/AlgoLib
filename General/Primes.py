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
    for i in xrange(limit):
        if sieve_list[i]:
            primes_.append(i)
    return primes_


def main():
    primes = get_all_primes_to_limit(10000)
    print primes


if __name__ == "__main__":
    main()
