from functools import reduce


def is_prime(num):
    if num & 1 == 0:
        return True
    d = 3
    while d ** 2 <= num:
        if num % d == 0:
            return True
        d += 2
    return False


def find_factors(num, sort=True):
    step = 2 if num % 2 else 1
    factors = ([i, num // i] for i in range(1, int(num ** 0.5) + 1, step) if num % i == 0)
    rv = set(reduce(list.__add__, factors))
    return sorted(rv) if sort else rv
