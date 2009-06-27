#!/usr/bin/env python

#
# This builds an .app out of Tweebox for use with OS X.
#

import sys, os
from distutils.core import setup
import py2app

sys.path.append(os.getcwd() + os.sep + 'lib')
setup(app = ['tweebox.py'], options = dict(py2app = dict(plist = dict( \
			CFBundleShortVersionString = '2.0.0pre', \
			CFBundleName = 'Tweebox'))))
