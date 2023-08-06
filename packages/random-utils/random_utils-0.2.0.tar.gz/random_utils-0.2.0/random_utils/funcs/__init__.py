import ctypes
import numpy as np


def flatten(list_to_flatten) -> iter:
    for item in list_to_flatten:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


def crash():
    ctypes.pointer(ctypes.c_char.from_address(5))[0]


def diff(l1, l2):
    return np.array(l1) - np.array(l2)


def map_range(x, from_range, to_range, to_int=True):
    val = np.interp(x, from_range, to_range)
    return int(val) if to_int else val


def useless_func(*args):
    if len(args) == 1:
        return args[0]
    else:
        return args
