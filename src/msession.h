/*
 * ===========================================================================
 *
 *       Filename:  msession.h
 *
 *    Description:  MSession class which help maintaining tracking session
 *
 *         Author:  AmvTek developers
 *          Email:  devel@amvtek.com
 *        Company:  sc AmvTek srl
 *
 * ===========================================================================
 */

#ifndef  MSESSION_H
#define  MSESSION_H

#include <ctime>

#include "earth.h"

using namespace std;

typedef unsigned long ulong;

class MSession {

    public: 

        MSession();

        int update(const double& lat1, const double& lon1);

        const double& lat() const;

        const double& lon() const;

        const double& distance() const;

        long duration() const;

    protected:
        
        double lat0, lon0, odometer;

        time_t t0, t1;

        unsigned long nUpdates;

};

#endif   /* ----- #ifndef MSESSION_H  ----- */
