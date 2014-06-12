# -*- coding: utf-8 -*-

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

from glob import glob

# list extension sources
sources = []
sources.extend(glob("src/*.pyx"))
sources.extend(glob("src/*.cc"))
sources.extend(glob("src/healpix/*.cc"))

# list headers
headers = []
headers.extend(glob("src/*.h"))
headers.extend(glob("src/healpix/*.h"))

setup(
    cmdclass={'build_ext': build_ext},
    headers=headers,
    ext_modules=[Extension('geohealpix', sources, language='c++')],
)

