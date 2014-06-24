/*
 * =====================================================================================
 *
 *       Filename:  healpix.h
 *
 *    Description:  Provide GEO enabled HEALPIX grids
 *
 *         Author:  AmvTek developers
 *          Email:  devel@amvtek.com
 *        Company:  sc AmvTek srl
 *
 * =====================================================================================
 */

#ifndef  HEALPIX_H
#define  HEALPIX_H

#include <cstdio>

#include <vector>
#include <math.h>
#include <stdexcept>

#include "healpix/lsconstants.h"
#include "healpix/pointing.h"
#include "healpix/rangeset.h"
#include "healpix/healpix_base.h"

#include "earth.h"

using std::vector;


// ease mapping Healpix_Ordering_scheme enumeration from python/cython...
Healpix_Ordering_Scheme hpx_get_scheme(int s) {

    return (s == 0) ? RING : NEST;
}

template<typename I> class T_Healpix: public T_Healpix_Base<I> {
    
    public:

        static const int HPX_OK = 0;

        static const int HPX_ERROR = 1;
        
        T_Healpix(int order, int scheme): T_Healpix_Base<I>(order, hpx_get_scheme(scheme)){}
        
        I get_code(const double& lat, const double& lon) const {

            GeoPointing pt = GeoPointing(lat,lon);
            return this->ang2pix(pt);
        }

        void get_codes_in_disc(
                const double& lat, const double& lon, const double& radius, 
                vector<I>& results) const {

            // perform query_disc ...
            GeoPointing center = GeoPointing(lat,lon);
            rangeset<I> lc = rangeset<I>();
            this->query_disc_inclusive(center,radius,lc);
            lc.toVector(results);
        }

        void get_fcode(const double& lat,const double& lon,
                char *dest, int destlen) const {

            int err = hpx_encode(dest, destlen, get_code(lat, lon));
            if (err){
                throw std::invalid_argument("healpix encoding failed!!");
            }

        }
        
        void get_fcodes_in_disc(
                const double& lat, const double& lon, const double& radius, 
                vector<string>& results) const {

            // list codes as I...
            vector<I> icodes = vector<I>();
            get_codes_in_disc(lat, lon, radius, icodes);

            // initialize results vector...
            results.clear();
            results.reserve(icodes.size());
            
            int err = 0;
            char buffer[31];
            string scode;
            for (int i=0; i<icodes.size(); i++){
                
                // read and encode I code ...
                err = hpx_encode(buffer, 31, icodes.at(i));
                if (err){
                    throw std::invalid_argument("healpix encoding failed!!");
                }
                
                // add to results...
                scode = string(buffer);
                results.push_back(scode);
            }
            
        }

        /*
         * return maximum radian aperture ('radian diameter...')
         * that can be covered by a single grid pixel
        */
        double get_aperture() const {

            return sqrt(4*pi/this->Npix()); 
        }


        /*
         * encode I code to HEALPIX QuadTree representation
         * Results is stored in dest buffer
         * return 0 if conversion was successfull
         * return 1 if conversion failed
         *
         */
        int hpx_encode(char *dest, int destlen, I code) const {               

            static const int TWO_BITS = 3; // 11 binary

            static char QUADTREE_DIGITS[] = {'1','2','3','4'};
            static char DIAMOND_DIGITS[] = {'A','B','C','D','E','F','G','H','I','J','K','L'};

            int order = this->Order();

            if (dest == NULL || destlen < order + 2 || code < 0) {

                return HPX_ERROR;
            }

            for (int i=order; i>0; i--) {

                dest[i] = QUADTREE_DIGITS[code&TWO_BITS];
                code >>= 2;
            }

            if ( code > 11) {

                return HPX_ERROR;
            }

            dest[0] = DIAMOND_DIGITS[code];
            dest[order+1] = '\0';

            return HPX_OK;
        }       
 };


typedef T_Healpix<int> HealpixGrid;

typedef T_Healpix<int64> HealpixGridHR;

#endif   /* ----- #ifndef HEALPIX_H  ----- */
