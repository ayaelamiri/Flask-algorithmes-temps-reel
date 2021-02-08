import fractions
from functools import reduce


def _lcm(x, y):
    if x > y:
        greater = x
    else:
        greater = y

    while (True):
        if (greater % x == 0) and (greater % y == 0):
            lcm = greater
            break
        greater += 1

    return lcm

def lcm(a):
    return reduce(_lcm, a)