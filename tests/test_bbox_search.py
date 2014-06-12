#  -*- coding: utf-8 -*-

from math import sqrt, pi, pow
import random

import geohealpix

EARTH_RADIUS = 6371
EARTH_PERIMETER = 2*pi*EARTH_RADIUS  # km unit
EARTH_AREA_SURFACE = 510072000  # squared km

# depending upon python version use stdlib unittest or external unittest2...
import sys
if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest


class Location(object):

    def __init__(self, lat, lon):

        self.lat = lat
        self.lon = lon


def test_list_all_fcodes_for(lat0, lon0, lat1, lon1,
                             latSteps=1000, lonSteps=500,
                             minOrder=None, maxOrder=None,
                             expectedOrder = -1):
    """
    tests if the codes given by list_all_fcodes_for(bbox)

    Inputs:
    lat0, lon0 for SW
    lat1, lon1 for NE

    Return true if the codes completly cover the bbox
    """

    print "Running new test for coords:"
    print "SW.lat: {}. SW.lon:{}".format(lat0, lon0)
    print "NE.lat: {}. NE.lon:{}".format(lat1, lon1)

    Hp = geohealpix.GeoGrid
    search =geohealpix.SearchEngine(minOrder, maxOrder)

    order = search.get_best_grid_for(lat0, lon0, lat1, lon1)
    print "Best grid order: %d" % order
    if order != expectedOrder > -1:

        print "Calculated order doesn't match expected order"
        print "Calculated order: %d" % order
        print "Expected order: %d" % expectedOrder
        return False

    diamonds = search.list_all_fcodes_for(lat0, lon0, lat1, lon1)

    SW = Location(lat0, lon0)
    NE = Location(lat1, lon1)
    SE = Location(lat0, lon1)
    NW = Location(lat1, lon0)

    deltaLat = SE.lat - SW.lat
    deltaLon = NW.lon - SW.lon

    for loni in xrange(lonSteps+1):

        for lati in xrange(latSteps+1):

            testPoint = Location(SW.lat + deltaLat * lati/latSteps,
                         SW.lon + deltaLon * loni/lonSteps)
            testPointCode = Hp(order).get_fcode(testPoint.lat, testPoint.lon)

            if testPointCode not in diamonds:

                print "\n**************************"
                print 'testPoint does not matchbDiamonds list for (lati,loni): {}, {}'.format(lati, loni)
                print "SW: {}".format(SW)
                print "NW: {}".format(NW)
                print "SE: {}".format(SE)
                print "testPoint: {}".format(testPoint)
                print "testPoint Code: {}".format(testPointCode)
                print "covering diamonds: {}".format(diamonds)
                return False

    print "Test ran perfectly fine. This test is done\n\n"
    return True


class TestDefinedMaps(unittest.TestCase):

    def test_maps(self):
        """test user defined maps"""

        maps = []
        maps.append([45.701383, 21.134948, 45.801041, 21.334075])
        maps.append([0, 0, 0.2, 0.1])
        maps.append([45.0, 21.0, 45.2, 21.1])
        maps.append([-45.901383, -21.534948, -45.801041, -21.334075])
        maps.append([-0.1, -0.2, 0.2, 0.1])
        maps.append([45.0, -22.0, 45.2, 21.1])

        for map in maps:

            result = test_list_all_fcodes_for(*map)
            self.assertTrue(result)
