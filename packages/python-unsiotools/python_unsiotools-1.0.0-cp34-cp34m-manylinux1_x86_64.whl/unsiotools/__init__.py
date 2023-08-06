
from __future__ import print_function

try:
	from unsiotools.py_unstools import *
except:
	import sys
	print("Unable to import [unsiotools.py_unstools]....",file=sys.stderr)

from .version import version as __version__
