#include <cstdio>

#include "../src/earth.h"


int main(){

    printf("---\nExercising distance functions in earth.h : \n");

    double lat0, lon0, lat1, lon1, d;
    lat0 = 45.0; lon0 = 23.0;
    printf("Departure : lat = %.06f | lon = %.06f \n",lat0,lon0);
    lat1 = 45.001; lon1 = 23.567;
    printf("Arrival : lat = %.06f | lon = %.06f \n",lat1,lon1);
    d = earth_dist_deg(lat0, lon0, lat1, lon1);
    printf("Distance : %.02f meters \n",d);
    d = hvsn2_dist_deg(lat0, lon0, lat1, lon1);
    printf("Square haversine : %.09f rad^2 \n",d);
}
