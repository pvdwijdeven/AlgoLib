from math import sqrt


def factors(n):
    step = 2 if n % 2 else 1
    return sorted(list(set(reduce(list.__add__,
                                  ([i, n // i] for i in range(1, int(sqrt(n)) + 1, step) if n % i == 0)))))


def prime_factors(n):
    i = 2
    prime_factor_list = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            prime_factor_list.append(i)
    if n > 1:
        prime_factor_list.append(n)
    return prime_factor_list


print factors(10**9)
print prime_factors(10**9)
