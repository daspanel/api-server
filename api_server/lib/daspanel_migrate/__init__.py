# -*- coding: utf-8 -*-
"""
    daspanel_migrate
    ----------------

    Daspanel-Migrate extension

    :copyright: (c) 2017 by Daspanel.
    :license: MIT, see LICENSE for more details.
"""
from __future__ import absolute_import, unicode_literals, division, print_function
from .__about__ import *  # noqa

__all__ = ["TinyDbMigrate"]

# http://docs.python-guide.org/en/latest/writing/structure/
# http://stackoverflow.com/questions/1944569/how-do-i-write-good-correct-package-init-py-files
from .tinydb import TinyDbMigrate


