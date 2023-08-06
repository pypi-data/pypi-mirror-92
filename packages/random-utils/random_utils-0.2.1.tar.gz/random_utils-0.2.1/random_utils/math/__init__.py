from functools import reduce
from .vector import Vector


def is_prime(num):
    if num == 2 or num == 3: return True
    if num < 2 or num % 2 == 0: return False
    if num < 9: return True
    if num % 3 == 0: return False
    r = int(num**0.5)
    f = 5
    while f <= r:
        if num % f == 0: return False
        if num % (f+2) == 0: return False
        f += 6
    return True


def find_factors(num, sort=True):
    step = 2 if num % 2 else 1
    factors = ([i, num // i] for i in range(1, int(num ** 0.5) + 1, step) if num % i == 0)
    rv = set(reduce(list.__add__, factors))
    return sorted(rv) if sort else list(rv)
