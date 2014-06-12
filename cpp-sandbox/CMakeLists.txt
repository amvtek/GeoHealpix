project(healpix)
cmake_minimum_required(VERSION 2.8)
include(FindProtobuf)
find_package(Protobuf REQUIRED)
include_directories(${PROTOBUF_INCLUDE_DIR})
#define lib sources
SET(lib_sources
    ../src/healpix/error_handling.cc ../src/healpix/pointing.cc 
    ../src/healpix/string_utils.cc ../src/healpix/geom_utils.cc
    ../src/healpix/healpix_tables.cc ../src/healpix/healpix_base.cc
    ../src/earth.cc ../src/slotinfo.cc 
    ../src/protobuf/slotinfo.pb.cc
    )
add_library(healpixlite ${lib_sources})
add_executable(runtest test.cc)
target_link_libraries(runtest healpixlite)
add_executable(runtest1 test1.cc)
target_link_libraries(runtest1 healpixlite)
add_executable(runtest2 test2.cc)
target_link_libraries(runtest2 healpixlite ${PROTOBUF_LIBRARY})

