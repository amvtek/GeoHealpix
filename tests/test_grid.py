#  -*- coding: utf-8 -*-

from base import unittest, get_geohealpix_sample

import geohealpix
print "Imported geohealpix version : %s" % str(geohealpix.__version__)
print "---"

def build_TestCreateGrid():

    def make_test_create_grid(order):

        NPIX = 12*2**(2*order)

        def test_create_grid(self):

            nestGrid = geohealpix.GeoGrid(order)
            ringGrid = geohealpix.GeoGrid(order, 0)

            self.assertEquals(nestGrid.get_order(), order)
            self.assertEquals(nestGrid.get_scheme(), 'NEST')
            self.assertEquals(nestGrid.get_npix(), NPIX)

            self.assertEquals(ringGrid.get_order(), order)
            self.assertEquals(ringGrid.get_scheme(), 'RING')
            self.assertEquals(ringGrid.get_npix(), NPIX)

        return test_create_grid

    ctx = {}
    for o in xrange(30):

        fname = "test_create_grid_%02i" % o
        ctx[fname] = make_test_create_grid(o)

    return type('TestCreateGrid',(unittest.TestCase,),ctx)

TestCreateGrid = build_TestCreateGrid()


def build_TestCreateGridWithInvalidOrder():

    def make_test_grid_with_invalid_order(order):

        def test_grid_with_invalid_order(self):

            with self.assertRaises(ValueError):
                geohealpix.GeoGrid(order)

        return test_grid_with_invalid_order

    ctx = {}
    for name, order in [('minus_one',-1),('sixty',60),('string','string')]:

        fname = "test_create_fail_with_order_equals_%s" % name
        ctx[fname] = make_test_grid_with_invalid_order(order)

    return type('TestCreateGridWithInvalidOrder',(unittest.TestCase,),ctx)

TestCreateGridWithInvalidOrder = build_TestCreateGridWithInvalidOrder()

def build_TestCallCode(seed):

    Grid = geohealpix.GeoGrid # local alias

    # generate base points
    basePoints = get_geohealpix_sample(seed, 8)

    # pregenerates all grids
    grids = [ (o,Grid(o),Grid(o,0)) for o in xrange(30)]
    
    def make_test_call_code_for_point(pt):

        def test_call_code_for_point(self):

            for order, nestGrid, ringGrid in grids:

                npix = 12*2**(2*order)
                fcodelen = 1 + order

                # call get_code...
                self.assertTrue(0 <= nestGrid.get_code(*pt) <= npix)
                self.assertTrue(0 <= ringGrid.get_code(*pt) <= npix)

                # call get_fcode
                self.assertEquals(len(nestGrid.get_fcode(*pt)),fcodelen)
                self.assertEquals(len(ringGrid.get_fcode(*pt)),fcodelen)
        
        return test_call_code_for_point

    ctx = {}
    for name, point in basePoints.items():

        fname = "test_code_for_point_%s" % name
        ctx[fname] = make_test_call_code_for_point(point)

    return type('TestCallCode',(unittest.TestCase,),ctx)

TestCallCode = build_TestCallCode(1)

def build_TestFCodeAreNested(seed):

    Grid = geohealpix.GeoGrid # local alias

    # generate base points
    basePoints = get_geohealpix_sample(seed, 8)

    # pregenerates all grids
    grids = [ Grid(o) for o in xrange(30)]

    def make_test_call_fcode_for_nested_grid_and_point(pt):

        def test_call_fcode_for_nested_grid_and_point(self):

            for o in xrange(1,30,1):

                fc0 = grids[o - 1].get_fcode(*pt)
                fc1 = grids[o].get_fcode(*pt)
                
                # test that codes are nested
                self.assertTrue(fc1.startswith(fc0))

        return test_call_fcode_for_nested_grid_and_point

    ctx = {}
    for name, point in basePoints.items():

        fname = "test_fcode_are_nested_for_point_%s" % name
        ctx[fname] = make_test_call_fcode_for_nested_grid_and_point(point)

    return type('TestFCodeAreNested',(unittest.TestCase,),ctx)

TestFCodeAreNested = build_TestFCodeAreNested(1)
