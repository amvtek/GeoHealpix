#  -*- coding: utf-8 -*-

from utils import get_geohealpix_sample, build_test_case

import geohealpix
print "Imported geohealpix version : %s" % str(geohealpix.__version__)
print "---"

# Quick example showing how we can obtain a collection of point
# Which covers the earth 'optimally' for HEALPIX testing
G0 = geohealpix.GeoGrid(0)
HPX_BASES = [c for c in "ABCDEFGHIJKL"]


def make_test_create_grid(order):

    def test_create_grid(self):

        nestGrid = geohealpix.GeoGrid(order)
        ringGrid = geohealpix.GeoGrid(order, 0)

        self.assertEquals(nestGrid.get_order(), order)
        self.assertEquals(nestGrid.get_scheme(), 'NEST')
        self.assertEquals(ringGrid.get_order(), order)
        self.assertEquals(ringGrid.get_scheme(), 'RING')

    return test_create_grid


def make_test_grid_with_invalid_order(order):

    def test_grid_with_invalid_order(self):

        with self.assertRaises(ValueError):
            geohealpix.GeoGrid(order)

    return test_grid_with_invalid_order


def make_test_call_code_for_point(pt):

    def test_call_code_for_point(self):

        nestGrid = geohealpix.GeoGrid(0)
        ringGrid = geohealpix.GeoGrid(0, 0)

        self.assertTrue('A' <= nestGrid.get_fcode(pt[0], pt[1]) <= 'L')
        self.assertTrue('A' <= ringGrid.get_fcode(pt[0], pt[1]) <= 'L')
        self.assertTrue(0 <= nestGrid.get_code(pt[0], pt[1]) <= 11)
        self.assertTrue(0 <= ringGrid.get_code(pt[0], pt[1]) <= 11)

    return test_call_code_for_point


def make_test_call_fcode_for_nested_grid_and_point(pt):

    def test_call_fcode_for_nested_grid_and_point(self):

        nest0 = geohealpix.GeoGrid(0)
        fcode0 = nest0.get_fcode(pt[0], pt[1])
        nest1 = geohealpix.GeoGrid(1)
        fcode1 = nest1.get_fcode(pt[0], pt[1])

        self.assertTrue(fcode1.startswith(fcode0))

    return test_call_fcode_for_nested_grid_and_point


# Creating the TestCases

TestCreateGrid = build_test_case(dict(zip(xrange(30), xrange(30))),
                                 'TestCreateGrid',
                                 "test_create_grid_%s",
                                 make_test_create_grid)

TestGridWithInvalidOrder = build_test_case(
    dict(zip([-1, 30, 60], [-1, 30, 60])),
    'TestGridWithInvalidOrder',
    "test_grid_with_invalid_order_%s",
    make_test_grid_with_invalid_order)

ppb = 4
seed = 1
sample = get_geohealpix_sample(seed, ppb)

TestCallCodeForPoint = build_test_case(sample, 'TestCallCodeForPoint',
                                       "test_call_code_for_point_%s",
                                       make_test_call_code_for_point)

TestCallFcodeForNestedGridAndPoint = build_test_case(
    sample, 'TestCallFcodeForNestedGridAndPoint',
    "test_call_fcode_for_nested_grid_and_point_%s",
    make_test_call_fcode_for_nested_grid_and_point
)




