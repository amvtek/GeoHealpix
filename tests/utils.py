#  -*- coding: utf-8 -*-

from base import unittest

import geohealpix

G0 = geohealpix.GeoGrid(0)
HPX_BASES = [c for c in "ABCDEFGHIJKL"]


def get_geohealpix_sample(seed, ppb=4):
    """
    >>> seed = 1
    >>> ppb = 4
    >>> sample = get_geohealpix_sample(seed, ppb)
    >>> len(sample)
    48
    >>> count = {}
    >>> for key in sample.keys():
    ...     if key[0] in HPX_BASES:
    ...         count[key[0]] = count.setdefault(key[0], 0) + 1
    >>> count.values().count(ppb) == len(count)
    True

    """

    # validate ppb (points per base...)
    ppb = int(ppb)
    if ppb <= 0:
        raise ValueError("Invalid ppb !")

    # seed random
    import random
    random.seed(seed)

    unf = random.uniform  # local alias
    get_latlon = lambda: (unf(-90, 90), unf(-180, 180))

    requirements = dict([(c, ppb) for c in HPX_BASES])
    sample = {}
    while requirements:

        # generate random point
        pt = get_latlon()

        k = G0.get_fcode(*pt)
        if k in requirements:

            c = requirements[k] - 1

            # add point to sample
            name = "%s%i" % (k, c)
            sample[name] = pt

            # update requirements
            if c:
                requirements[k] = c
            else:
                requirements.pop(k)

    return sample


def build_test_case(iter, testcaseName, testformat, f):

    ctx = {}

    for i in iter:

        testname = testformat % i
        ctx[testname] = f(iter[i])

    return type(testcaseName, (unittest.TestCase,), ctx)


if __name__ == "__main__":

    import doctest
    doctest.testmod()

