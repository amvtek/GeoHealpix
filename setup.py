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
    long_description=open('README.txt').read(),
    author="AmvTek developers",
    author_email="devel@amvtek.com",
    url="https://github.com/amvtek/GeoHealpix",
    licence='LICENSE',
    headers=headers,
    ext_modules=[Extension('geohealpix', sources, language='c++')],
    install_requires=[

    ]
    )

