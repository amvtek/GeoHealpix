/*
 * =====================================================================================
 *
 *       Filename:  earth.h
 *
 *    Description:  Helper functions & classes to help working with GEO coordinates
 *
 *         Author:  AmvTek developers
 *          Email:  devel@amvtek.com
 *        Company:  sc AmvTek srl
 *
 * =====================================================================================
 */

#ifndef  EARTH_H
#define  EARTH_H

#include <cmath>

#include "healpix/lsconstants.h"
#include "healpix/pointing.h"

static const double EARTH_RADIUS = 6371009; // meters
static const double EARTH_PERIMETER = 2*pi*EARTH_RADIUS;
static const double EARTH_SURFACE = 4*pi*pow(EARTH_RADIUS,2);

typedef const double numarg;


double hvsn2_dist_rad(numarg& lat0, numarg& lon0, numarg& lat1, numarg& lon1);

double hvsn2_dist_deg(numarg& lat0, numarg& lon0, numarg& lat1, numarg& lon1);

double hvsn2_to_earth(numarg& hdist);

double earth_dist_rad(numarg& lat0, numarg& lon0, numarg& lat1, numarg& lon1);

double earth_dist_deg(numarg& lat0, numarg& lon0, numarg& lat1, numarg& lon1);

double gc_dist_rad(numarg& lat0, numarg& lon0, numarg& lat1, numarg& lon1);

double gc_dist_deg(numarg& lat0, numarg& lon0, numarg& lat1, numarg& lon1);

double bearing_deg(numarg& lat0, numarg& lon0, numarg& lat1, numarg& lon1);

void point_at_dist_and_bearing_from_ref(
    numarg& reflat, numarg& reflon, numarg& dist, numarg& bearing,
    double* ptlat, double* ptlon); 


class GeoPointing : public pointing {

    public:

        GeoPointing(const double& deglat,const double& deglon);

};

class GeoPoint {

    public:

        GeoPoint(numarg& deglat, numarg& deglon);

        double dist_to(numarg& deglat, numarg& deglon) const;

        double hvsn2_dist_to(numarg& deglat, numarg& deglon) const;

    protected:

        double lat, lon;
};

#endif   /* ----- #ifndef EARTH_H  ----- */

