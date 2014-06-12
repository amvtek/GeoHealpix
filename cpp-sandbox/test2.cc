#include <iostream>
#include <string>

#include "../src/slotinfo.h"

using namespace std;

typedef struct {
    char datas[64];
} Chunk;

static void test_pb01(){

    cout << "Testing protobuf serialization for schema slotinfos..." << endl;
    cout << "Intenting constructing Location instance : " << endl;

    Location loc = Location();
    loc.set_lat(45.0987);
    loc.set_lon(-67.98456);

    cout << "loc : " << endl << loc.DebugString();
    cout << "end of test";
}

static void test_slotinfo() {

    string dumId = string("dummyId");
    
    cout << "Found : " << UnitInfoEncoder::getSlotHeader(dumId) << endl;
}

static void test_UnitInfoEncoder() {

    string dumId = string("dummy");

    cout << "creating UnitInfoEncoder with 'dummy'" << endl;
    UnitInfoEncoder encoder1 = UnitInfoEncoder(dumId);
    cout << "---" << endl;
    cout << "creating UnitInfoEncoder with 'dummyAAAA'" << endl;
    dumId.resize(9,'A');
    UnitInfoEncoder encoder2 = UnitInfoEncoder(dumId);
}

static void test_UnitInfoEncoder02() {
    
    // construct identifier of size 16
    string dumId = string();
    dumId.resize(16,'k');

    // determine ChunkInfo size...
    int chunkSize = UnitInfoEncoder::getChunkSize(dumId);
    cout << "using id of size 16, full ChunkInfo size is " << chunkSize << endl;

    // construct encoder
    cout << "---" << endl;
    cout << "creating UnitInfoEncoder "<< endl;
    UnitInfoEncoder encoder = UnitInfoEncoder(dumId);

    // attend lat,lon encoding ...
    cout << "Using encoder to encode < lat = 45.0 | lon = 23.567 >"<< endl;
    string buf = string();
    encoder.encodeLatLon(45.0,23.567,&buf);
    cout << "encoded unitInfo size is "<< buf.size() << endl;
    cout << "now appending timestamp to unitInfo" << endl;
    encoder.encodeTimeStamp(123456,&buf);
    cout << "after appending timestamp,encoded unitInfo size is "<< buf.size() << endl;

}

int main() {
    
    cout << "---" << endl;
    test_UnitInfoEncoder02();
    
    return 0;
}



