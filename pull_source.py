# -*- coding: utf-8 -*-
"""
    pull_source.py
    ~~~~~~~~~~~~~~

    I extract from healpix sourceforge project the subset of c++ sourcefiles
    that is necessary to build the geohealpix extension module.

    :copyright: (c) 2012 by sc AmvTek srl
    :email: devel@amvtek.com
"""

import argparse, os, shutil
BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))

sourceList = [
        "Healpix_cxx/healpix_tables.h",
        "Healpix_cxx/healpix_tables.cc",
        "cxxsupport/datatypes.h",
        "cxxsupport/error_handling.h",
        "cxxsupport/error_handling.cc",
        "cxxsupport/string_utils.h",
        "cxxsupport/string_utils.cc",
        "Healpix_cxx/healpix_base.h",
        "Healpix_cxx/healpix_base.cc",
        "cxxsupport/pointing.h",
        "cxxsupport/pointing.cc",
        "cxxsupport/arr.h",
        "cxxsupport/rangeset.h",
        "cxxsupport/geom_utils.h",
        "cxxsupport/geom_utils.cc",
        "cxxsupport/lsconstants.h",
        "cxxsupport/vec3.h",
        "cxxsupport/math_utils.h",
        "cxxsupport/alloc_utils.h",
        ]

def input_folder(path):
    "validate that path is likely to contain healpix project..."
    path = os.path.join(BASE_FOLDER,path)
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError("input folder does not exists")
    path = os.path.join(path,"src/cxx")
    for fp in [os.path.join(path,s) for s in sourceList]:
        if not os.path.isfile(fp):
            raise argparse.ArgumentTypeError("input folder not as expected")
    return path

def output_folder(path):
    "validate that path corresponds to an existing folder"
    path = os.path.join(BASE_FOLDER,path)
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError("output folder does not exists")
    return path

parser = argparse.ArgumentParser(
        description="Import c++ source files from healpix sourceforge project"
        )
parser.add_argument('-o','--output',default='src/healpix',type=output_folder,
        help='destination folder where to export extracted sources'
        )

parser.add_argument('input',type=input_folder,
        help='folder containing healpix sourceforge project'
        )
args = parser.parse_args()

inputFolder = args.input
outputFolder = args.output

for fp in [os.path.join(inputFolder,s) for s in sourceList]:
    print "transferring ",os.path.basename(fp)
    shutil.copy(fp,outputFolder)
