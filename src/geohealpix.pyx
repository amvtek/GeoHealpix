#  -*- coding: utf-8 -*-
from libc.stdio cimport snprintf
from libc.stdint cimport uint32_t, int64_t

from libc.string cimport strncpy, strcpy

from cpython.bytes cimport PyBytes_FromStringAndSize, PyBytes_AsStringAndSize
from cpython.float cimport PyFloat_FromDouble
from cpython.int cimport PyInt_FromLong
from cpython.long cimport PyLong_FromUnsignedLong

from libcpp.vector cimport vector
from libcpp.list cimport list
from libcpp.string cimport string

from cython.operator cimport preincrement as inc, dereference as deref

from math import pi, log, ceil, sqrt, floor
from bisect import bisect

__version__ = (1,1,3)

EARTH_RADIUS = 6371 # km
EARTH_PERIMETER = 2*pi*EARTH_RADIUS  # km unit
EARTH_AREA_SURFACE = 510072000  # squared km

cdef extern from "earth.h":
    
    double earth_dist_deg(double&,double&,double&,double&)
    double gc_dist_deg(double&,double&,double&,double&)
    double bearing_deg(double& lat0, double& lon0, double& lat1, double& lon1)
    void point_at_dist_and_bearing_from_ref(double&,double&,double&,double&,double*,double*)

cdef extern from "msession.h":

    ctypedef unsigned long ulong

    cdef cppclass MSession:
        MSession()
        int update(double&,double&)
        double& lat()
        double& lon()
        double& distance()
        long duration()

cdef extern from "healpix.h":

    cdef cppclass HealpixGridHR:
        HealpixGridHR(int, int) except +
        int64_t  get_code(double&, double&) except +
        void get_fcode(double&, double&, char*, int) except +
        void get_codes_in_disc(double&, double&, double&, vector[int64_t]&) except +
        void get_fcodes_in_disc(double&, double&, double&, vector[string]&) except +
        int64_t Npix()
        double get_aperture()

def earth_dist(lat0, lon0, lat1, lon1):
    "return distance in meters in between (lat0,lon0) and (lat1,lon1)"

    return earth_dist_deg(lat0, lon0, lat1, lon1)

def bearing(lat0, lon0, lat1, lon1):
    "return bearing in degree from (lat0,lon0) to (lat1,lon1)"

    return bearing_deg(lat0, lon0, lat1, lon1)

def point_at_dist(lat0, lon0, dist, bearing):
    "return (lat,lon) of point at dist and bearing from (lat0,lon0)"

    cdef double ptlat, ptlon
    point_at_dist_and_bearing_from_ref(lat0,lon0,dist,bearing,&ptlat,&ptlon)

    return (PyFloat_FromDouble(ptlat), PyFloat_FromDouble(ptlon))

cdef class TrackingSession(object):

    cdef MSession *session
    cdef object unitId

    def __cinit__(self, *args, **kwargs):

        # *args,**kwargs are to simplify python inheritance
        # If in need to define an inheriting python class this __cinit__ class
        # will always be called, except if you redefine __new__

        # instanciate new MSession
        self.session = new MSession()

    def __init__(self, unitId):

        self.unitId = unitId

    def update(self, double lat, double lon):

        # update underlaying MSession storing in it lat,lon 
        # and adjusting odometer...
        cdef int hasError = self.session.update(lat,lon)

        if hasError:
            raise ValueError("Invalid latitude or longitude")

    # ========================================================================
    # accessor for session variables

    def get_lat(self):
        return PyFloat_FromDouble(self.session.lat())
    lat = property(get_lat)
    
    def get_lon(self):
        return PyFloat_FromDouble(self.session.lon())
    lon = property(get_lon)

    def get_distance(self):
        return PyFloat_FromDouble(self.session.distance())
    distance = property(get_distance)

    def get_duration(self):
        return PyInt_FromLong(self.session.duration())
    duration = property(get_duration)

    def __dealloc__(self):

        del self.session

class Healpix:
    "Enumerate Healpix grid schemes"

    RING = 0
    
    NEST = 1
    
    fmt = "<Healpix Grid scheme=%(scheme)s order=%(order)i>"

cdef class GeoGrid(object):
    """
    Provides access to Healpix global grid which tesselates spherical Earth
    sphere using equiaera <diamond> shaped cells (called pixels in Healpix)
    The main purpose of this class is to let us index location of moving
    objects without the need to apply local latitude corrections to evaluate
    distances...
    """

    cdef HealpixGridHR *_grid
    cdef int _order, _scheme
    
    def __cinit__(self, order, nested=True, *args, **kwargs):

        # extra arguments are to simplify python inheritance...

        # validate order
        order = int(order)
        if (order < 0) or (order > 29):
            raise ValueError("Invalid grid order, value not in range [0,29]!")
        self._order = order

        # choose grid scheme
        if nested : # we use NEST scheme
            self._scheme = Healpix.NEST
        else:
            self._scheme = Healpix.RING
        
        # instantiate grid
        self._grid = new HealpixGridHR(self._order, self._scheme)
        
    def get_code(self,lat,lon):
        """
        return numerical pixel code for (lat,lon) location
        
        @lat : location latitude in decimal degree
        @lon : location longitude in decimal degree
        """
        
        return self._grid.get_code(lat,lon)

    def get_fcode(self, lat, lon):
        """
        return formatted pixel code for (lat,lon) location
        
        @lat : location latitude in decimal degree
        @lon : location longitude in decimal degree
        """

        cdef char[31] scode # max size for rawcode is 29 + 1 + 1...
        self._grid.get_fcode(lat, lon, scode, 31)
        return scode

    def list_codes_in_disc(self,lat,lon,radius):
        """
        return list of numerical pixels code for diamonds
        at distance less than radius of (lat,lon) center

        @lat : center latitude in decimal degree
        @lon : center longitude in decimal degree
        @radius : distance in 'earth' radians
        """

        cdef vector[int64_t] rv = vector[int64_t]()
        self._grid.get_codes_in_disc(lat,lon,radius,rv)

        return rv

    def list_fcodes_in_disc(self,lat,lon,radius):
        """
        return list of formatted pixels code for diamonds 
        at distance less than radius of (lat,lon) center

        @lat : center latitude in decimal degree
        @lon : center longitude in decimal degree
        @radius : distance in 'earth' radians
        """
  
        cdef vector[string] rv = vector[string]()
        self._grid.get_fcodes_in_disc(lat, lon, radius, rv)

        return rv

    def get_scheme(self):
        "return code scheme as 'RING' or 'NEST'"

        if self._scheme:
            return 'NEST'
        return 'RING'
    scheme = property(get_scheme)

    def get_order(self):
        "return order"

        return self._order
    order = property(get_order)

    def get_npix(self):
        "return Npix()"

        return self._grid.Npix()
    npix = property(get_npix)

    def get_aperture(self):
        "return pixel grid aperture"

        return self._grid.get_aperture()
    aperture = property(get_aperture)
        
    def __hash__(self):

        return hash((self._scheme, self._order))

    def __repr__(self):

        scheme = self.get_scheme()
        order  = self.get_order()

        return Healpix.fmt % locals()

    def __dealloc__(self):

        del self._grid

class SearchEngine(object):

    def __init__(self, *grids):

        if not grids:
            raise ValueError("SearchEngine requires at least 1 GeoGrid !!")

        # sort grid by aperture size
        grids = sorted(grids, key=lambda g:g.aperture)

        # construct inner _hpxGridIdx as sorted list of (g.aperture/2.0,g)
        self._hpxGridIdx = [(g.aperture/2.0,g) for g in grids]

    def _get_disk_covering_bbox(self, lat0, lon0, lat1, lon1):

        lat = (lat0 + lat1)/2.0
        lon = (lon0 + lon1)/2.0
        cdef double radius = gc_dist_deg(lat0, lon0, lat1, lon1)/2.0

        return (lat, lon, radius)

    def list_fcode_tiling_bbox(self, lat0, lon0, lat1, lon1):

        # minimal search disk to cover rectangular bbox 
        lat, lon, radius = self._get_disk_covering_bbox(lat0, lon0, lat1, lon1)

        # select best grid to process search disk
        gridIdx = bisect(self._hpxGridIdx, (radius,))
        if gridIdx == len(self._hpxGridIdx):
            gridIdx = -1
        maxradius, bestGrid = self._hpxGridIdx[gridIdx]

        return bestGrid.list_fcodes_in_disc(lat, lon, min(radius,maxradius))
