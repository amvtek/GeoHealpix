#  -*- coding: utf-8 -*-

# depending upon python version use stdlib unittest or external unittest2...
import os
import sys
if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

# patch sys.path to ease running tests during development
# developer may set the environment variable HEALPIX_BUILD_PATH
# so that newly built extension module can be imported

buildPath = os.environ.get('HEALPIX_BUILD_PATH')
print "---"
if buildPath is not None:
    print "Found HEALPIX_BUILD_PATH : %s" % buildPath
    sys.path.insert(0, buildPath)

# generates a seed controled random set of point with ppb points
# in each HEALPIX base diamonds
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

    from geohealpix import GeoGrid

    G0 = GeoGrid(0)
    HPX_BASES = "ABCDEFGHIJKL"
    
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
