/*
 * =====================================================================================
 *
 *       Filename:  earth.cc
 *
 *    Description:  Helper functions & classes to help working with GEO coordinates
 *
 *         Author:  AmvTek developers
 *          Email:  devel@amvtek.com
 *        Company:  sc AmvTek srl
 *
 * =====================================================================================
 */

#include "earth.h"

// convert degree to radian
#define d2r(x) ((x)*degr2rad)

// convert radian to degree
#define r2d(x) ((x)*rad2degr)

// square 'haversine' distance, arguments in radians
double inline hvsn2_dist_rad(numarg& lat0,numarg& lon0,numarg& lat1,numarg& lon1){
    
    return pow(sin((lat0-lat1)/2),2)+cos(lat0)*cos(lat1)*pow(sin((lon0-lon1)/2),2);
}

// square 'haversine' distance, arguments in degrees
double hvsn2_dist_deg(numarg& lat0,numarg& lon0,numarg& lat1,numarg& lon1){

    return hvsn2_dist_rad(d2r(lat0),d2r(lon0),d2r(lat1),d2r(lon1));
}

// convert square 'haversine' distance to earth distance
double hvsn2_to_earth(numarg& hdist){
    
    return 2*EARTH_RADIUS*atan2(sqrt(hdist),sqrt(1-hdist));
}

// earth 'metric' distance, arguments in radians
double earth_dist_rad(numarg& lat0, numarg& lon0, numarg& lat1, numarg& lon1){
    
    double a = hvsn2_dist_rad(lat0,lon0,lat1,lon1);
    return 2*EARTH_RADIUS*atan2(sqrt(a),sqrt(1-a));
}

// earth 'metric' distance, arguments in degrees
double earth_dist_deg(numarg& lat0, numarg& lon0, numarg& lat1, numarg& lon1){
    
    double a = hvsn2_dist_rad(d2r(lat0),d2r(lon0),d2r(lat1),d2r(lon1));
    return 2*EARTH_RADIUS*atan2(sqrt(a),sqrt(1-a));
}

// radians 'great circle' distance, arguments in radians
double gc_dist_rad(numarg& lat0, numarg& lon0, numarg& lat1, numarg& lon1){

    double a = hvsn2_dist_rad(lat0,lon0,lat1,lon1);
    return 2*atan2(sqrt(a),sqrt(1-a));
}

// radians 'great circle' distance, arguments in degrees
double gc_dist_deg(numarg& lat0, numarg& lon0, numarg& lat1, numarg& lon1){
    
    double a = hvsn2_dist_rad(d2r(lat0),d2r(lon0),d2r(lat1),d2r(lon1));
    return 2*atan2(sqrt(a),sqrt(1-a));
}

// bearing in degree from (lat0,lon0) to (lat1,lon1)
double bearing_deg(numarg& lat0, numarg& lon0, numarg& lat1, numarg& lon1){

    // convert args to radians
    double rlat0, rlon0, rlat1, rlon1;
    rlat0 = d2r(lat0); rlon0 = d2r(lon0);
    rlat1 = d2r(lat1); rlon1 = d2r(lon1);

    double deltaLon = rlon1 - rlon0;
    double y = sin(deltaLon)*cos(rlat1);
    double x = cos(rlat0)*sin(rlat1)-sin(rlat0)*cos(rlat1)*cos(deltaLon);

    return fmod(r2d(atan2(y,x))+360.0,360.0);
}

/*
 * return (ptlat,ptlon) of point at dist and bearing from ref
 * latitude,longitude are in degrees
 * bearing are in degree [0-360] clockwise North
 * distance in meters
 */
void point_at_dist_and_bearing_from_ref(
    numarg& reflat, numarg& reflon, numarg& dist, numarg& bearing,
    double* ptlat, double* ptlon){

    // results coordinates radians
    double lat,lon;

    // convert all args to radians
    double rlat,rlon,rdist,rbearing;
    rlat = d2r(reflat); rlon = d2r(reflon);
    rdist = dist/EARTH_RADIUS; rbearing = d2r(bearing);

    lat = asin(sin(rlat)*cos(rdist)+cos(rlat)*sin(rdist)*cos(rbearing));

    lon = rlon + atan2(sin(rbearing)*sin(rdist)*cos(rlat),cos(rdist)-sin(rlat)*sin(lat));

    // convert back to degree
    *ptlat = lat*rad2degr;

    *ptlon = lon*rad2degr;
}


GeoPointing::GeoPointing(numarg& deglat,numarg& deglon) {

    /* convert deglat,deglon to celestial coordinates */
    theta = (-deglat + 90.0)*degr2rad;
    phi = (deglon + 180.0)*degr2rad;
    this->normalize();
}

GeoPoint::GeoPoint(numarg& deglat, numarg& deglon) {

    /* convert deglat,deglon to radians */
    lat = deglat*degr2rad;
    lon = deglon*degr2rad;
}

double GeoPoint::dist_to(numarg& deglat, numarg& deglon) const {

    double lat1,lon1;
    lat1 = deglat*degr2rad;
    lon1 = deglon*degr2rad;

    return earth_dist_rad(lat,lon,lat1,lon1);

}

double GeoPoint::hvsn2_dist_to(numarg& deglat, numarg& deglon) const {
    
    double lat1,lon1;
    lat1 = deglat*degr2rad;
    lon1 = deglon*degr2rad;

    return hvsn2_dist_rad(lat,lon,lat1,lon1);

}
