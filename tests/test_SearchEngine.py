#  -*- coding: utf-8 -*-

from collections import namedtuple
import random

from utils import get_geohealpix_sample, build_test_case

import geohealpix
print "Imported geohealpix version : %s" % str(geohealpix.__version__)
print "---"

# Quick example showing how we can obtain a collection of point
# Which covers the earth 'optimally' for HEALPIX testing
G0 = geohealpix.GeoGrid(0)
HPX_BASES = [c for c in "ABCDEFGHIJKL"]


def make_test_bbox_for_point(pt):

    def test_bbox_for_point(self):

        MIN_DELTA = 0.1
        MAX_DELTA = 10
        LAT_STEPS = 10
        LON_STEPS = LAT_STEPS  # 20
        random.seed(pt)
        delta = random.uniform(MIN_DELTA, MAX_DELTA)

        Hp = geohealpix.GeoGrid
        search =geohealpix.SearchEngine(2, 10)

        Point = namedtuple('Point', 'lat lon')
        swCorner = Point(pt[0], pt[1])
        neCorner = Point(swCorner.lat+delta, swCorner.lon+delta)

        order = search.get_best_grid_for(
            swCorner.lat, swCorner.lon, neCorner.lat, neCorner.lon)

        diamonds = search.list_all_fcodes_for(
            swCorner.lat, swCorner.lon, neCorner.lat, neCorner.lon)

        for loni in xrange(LAT_STEPS+1):

            for lati in xrange(LON_STEPS+1):

                testPoint = Point(swCorner.lat + delta*lati/LAT_STEPS,
                                  swCorner.lon + delta*loni/LON_STEPS)
                testPointCode = Hp(order).get_fcode(testPoint.lat, testPoint.lon)

                self.assertIn(testPointCode, diamonds)

    return test_bbox_for_point

ppb = 4
seed = 1
sample = get_geohealpix_sample(seed, ppb)

TestBBoxForPoint = build_test_case(sample, 'TestBBoxForPoint',
                                       "test_bbox_for_point_%s",
                                       make_test_bbox_for_point)