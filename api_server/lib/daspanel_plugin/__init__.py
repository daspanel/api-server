# -*- coding: utf-8 -*-
"""
    daspanel_plugin
    -------------

    Daspanel-Plugin extension

    :copyright: (c) 2016 by Daspanel.
    :license: MIT, see LICENSE for more details.
"""
from __future__ import absolute_import, division, print_function
from .__about__ import *  # noqa

#from daspanel_flask.__about__ import (
#    __author__, __copyright__, __email__, __license__, __summary__, __title__,
#    __uri__, __version__
#)

__all__ = ["PluginCollection"]

# http://docs.python-guide.org/en/latest/writing/structure/
# http://stackoverflow.com/questions/1944569/how-do-i-write-good-correct-package-init-py-files
from .handler import PluginCollection


