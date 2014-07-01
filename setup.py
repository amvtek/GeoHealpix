# -*- coding: utf-8 -*-

from distutils.core import setup
from distutils.extension import Extension

from glob import glob

# list extension sources
sources = []
sources.extend(glob("src/*.cc"))
sources.extend(glob("src/*.cpp"))
sources.extend(glob("src/healpix/*.cc"))

# list headers
headers = []
headers.extend(glob("src/*.h"))
headers.extend(glob("src/healpix/*.h"))

setup(
    name="geohealpix",
    version="1.2.0",
    description="Efficient Geohashing using HEALPIX global grid",
    author="AmvTek development team",
    author_email="devel@amvtek.com",
    url="http://www.amvtek.com",
    headers=headers,
    ext_modules=[Extension('geohealpix', sources, language='c++')],
    )

