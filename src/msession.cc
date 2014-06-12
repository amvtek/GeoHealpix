/*
 * ===========================================================================
 *
 *       Filename:  msession.cc
 *
 *    Description:  MSession class which help maintaining tracking session
 *
 *         Author:  AmvTek developers
 *          Email:  devel@amvtek.com
 *        Company:  sc AmvTek srl
 *
 * ===========================================================================
 */

#include "msession.h"

MSession::MSession(){

    // initializes session measurement
    odometer = 0.0;
    t0 = time(NULL); 
    t1 = time(NULL);
    nUpdates = 0;
}

int MSession::update(const double& lat1, const double& lon1){

    static const int OK = 0;
    static const int ERROR = 1;

    // validate new coordinates are valid geocoordinates
    if (lat1<-90 || lat1>90 || lon1<-180 || lon1>180) {

        return ERROR;
    }

    t1 = time(NULL);

    if(nUpdates++ > 0) {

        // update odometer
        odometer += earth_dist_deg(lat0,lon0,lat1,lon1);
    }
    lat0 = lat1;
    lon0 = lon1;

    return OK;
}

const double& MSession::lat() const{

    return lat0;
}

const double& MSession::lon() const{

    return lon0;
}

const double& MSession::distance() const{

    return odometer;
}

long MSession::duration() const{

    long delta = t1 - t0;
    return delta;
}
