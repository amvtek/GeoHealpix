#  -*- coding: utf-8 -*-

# depending upon python version use stdlib unittest or external unittest2...
import os
import sys
if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

# patch sys.path to ease running tests during development
# developer may set the environment variable HEALPIX_BUILD_PATH
# so that newly built extension module can be imported

buildPath = os.environ.get('HEALPIX_BUILD_PATH')
print "---"
if buildPath is not None:
    print "Found HEALPIX_BUILD_PATH : %s" % buildPath
    sys.path.insert(0, buildPath)