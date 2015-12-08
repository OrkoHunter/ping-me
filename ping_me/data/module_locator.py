"""Locate the data files in the eggs to open."""

# NOTE : This module is redundant now. It was used to locate the csv file
# present inside the installed egg. But as the wheels do not respect relative
# path for data files, using a file may be dangerous and hence the data is
# kept as a dictionary inside `countrylist.py`. The following code is not
# deleted from the package because of love.

import os
import sys

def we_are_frozen():
    return hasattr(sys, "frozen")

def modeule_path():
    encoding = sys.getfilesystemencoding()
    if we_are_frozen():
        return os.path.dirname(unicode(sys.executable, encoding))
    return os.path.dirname(unicode(__file__, encoding))
