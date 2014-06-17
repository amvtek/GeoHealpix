# -*- coding: utf-8 -*-

from .base import unittest

import geohealpix
print "Imported geohealpix version : %s" % str(geohealpix.__version__)
print "---"

# Quick example showing how we can obtain a collection of point
# Which covers the earth 'optimally' for HEALPIX testing
G0 = geohealpix.GeoGrid(0)
HPX_BASES = [c for c in "ABCDEFGHIJKL"]


def get_geohealpix_sample(seed, ppb=4):

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

sample = get_geohealpix_sample("QUICK TEST", 8)
print sample
print "len(sample) = ", len(sample)


# Quick example showing how TestCase can be dynamically generated
def build_test_case(num):

    def make_test_func(i):

        def test_func(self):
            print "\n---"
            print "In test !!"
            self.assertEquals(i, i)

        return test_func

    ctx = {}

    for i in xrange(num):

        testname = "test_%02i" % i
        ctx[testname] = make_test_func(i)

    return type('TestAuto', (unittest.TestCase,), ctx)

TestAuto = build_test_case(4)


