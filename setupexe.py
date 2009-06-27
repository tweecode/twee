#
# This builds an .exe out of Tweebox for use with Windows.
# Call this with this command line: setupexe.py py2exe

import sys, os
from distutils.core import setup
import py2exe

sys.path.append(os.getcwd() + os.sep + 'lib')
setup(windows=['tweebox.py'])
