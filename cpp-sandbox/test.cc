#include <iostream>
#include <vector>
using namespace std;

#include "../src/healpix.h"
#include "../src/earth.h"

int main() {

    cout << "now testing our own HealpixGrid...\n";
    cout << "Using HealpixGrid 10 \n";
    HealpixGrid *gGrid = new HealpixGrid(10);
    cout << "---\n";
    cout << "earth location : lat = " << 23.567 << " lon = " << 45.6789 << "\n";
    GeoPointing pt = GeoPointing(23.567,45.6789);
    cout << "integer code for earth location : "<< gGrid->ang2pix(pt)<<"\n";
    cout << "integer code for earth location [method 2]: "<< gGrid->get_code(23.567,45.6789)<<"\n";
    cout << "---\n";
    cout << "searching codes in 5 km circle around earth location\n";
    vector<int> codeList = vector<int>();
    double ar = 5000 / EARTH_PERIMETER;
    gGrid->get_codes_in_disc(23.567,45.6789,ar,codeList);
    cout << "results = [\n";
    vector<int>::iterator it;
    for(it = codeList.begin();it != codeList.end();++it){
        cout << *it << endl;
    }
    cout << "]\n";
    cout << "End of test\n";
    return 0;
}
