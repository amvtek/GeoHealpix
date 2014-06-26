# -*- coding: utf-8 -*-

from base import unittest, get_geohealpix_sample

import math, random

import geohealpix
print "Imported geohealpix version : %s" % str(geohealpix.__version__)
print "---"

GeoGrid = geohealpix.GeoGrid
SearchEngine = geohealpix.SearchEngine

def build_TestSearchBbox(seed, ppb=8, latlon_delta=(0.1,10.0), tpb=128):

    mGrid = GeoGrid(12)
    searchEngine = SearchEngine(*[GeoGrid(o) for o in xrange(1,13,1)])

    basePoints = get_geohealpix_sample(seed, ppb)

    def make_bbox_search_test(pt):

        def test_bbox_search(self):

            # use pt to produce ptseed
            # floats are converted to integer to control rounding errors
            mlat, mlon = pt
            mlat = int(mlat*1000000)
            mlon = int(mlon*1000000)
            ptseed = (seed,mlat,mlon)

            rnd = random.Random(ptseed)
            unf = random.uniform

            # generate random rectangular bbox
            lat,lon = pt
            dlat = unf(*latlon_delta)
            dlon = unf(*latlon_delta)
            lat0, lon0 = lat-dlat, lon-dlon
            lat1, lon1 = lat+dlat, lon+dlon
            bbox = (lat0, lon0, lat1, lon1)

            # point in bonding box random generator
            gen_pt_in_bbox = lambda :(unf(lat0,lat1),unf(lon0,lon1))

            bboxPixTiles = searchEngine.list_fcode_tiling_bbox(*bbox)

            # bbox shall be tiled by at most 4 healpix pixels
            # healpix library does not provide guarantee for this
            # failmsg = "bbox is tiled by %i pixels !!" % len(bboxPixTiles)
            # self.assertTrue(len(bboxPixTiles)<=6,failmsg)

            # generate tpb random point inside bbox
            # and make sure they are in one of the pixel in bboxPixTiles...
            for i in xrange(tpb):

                # generate random point
                bp = gen_pt_in_bbox()
                bpfcode = mGrid.get_fcode(*bp)

                # check to what pixel bpfcode belongs...
                bppix = None
                for pix in bboxPixTiles:

                    if bpfcode.startswith(pix):
                        bppix = pix
                        break

                # make sure a pixel was found
                failmsg = "point %i not covered by bbox tiling pixels!!" % i
                self.assertIsNotNone(bppix,failmsg)

        return  test_bbox_search

    ctx = {}
    for name, point in basePoints.items():

        fname = "test_bbox_search_at_point_%s" % name
        ctx[fname] = make_bbox_search_test(point)

    return type('TestSearchBbox', (unittest.TestCase,), ctx)

TestSearchBbox = build_TestSearchBbox("Search Engine tests 1",ppb=32)


