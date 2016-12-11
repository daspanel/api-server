#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sites errors
~~~~~~~~~~~~

Contains error definitions for the Sites module.

:copyright: (c) 2016 by Abner G Jacobsen
:licence: GPL-3, see LICENCE for more details
"""
#from __future__ import absolute_import, unicode_literals
from __future__ import absolute_import, division, print_function

from lib.daspanel_errors import ApiErrorMsgType

error_doc = 'https://daspanel.com/docs/api/sites/errors'

SITES_ERRORS = {
    'NOTFOUND': ApiErrorMsgType(404, 'Not Found', 
        'Site not found: {0}', error_doc),
    'REDIRECTNOTFOUND': ApiErrorMsgType(404, 'Redirect Not Found', 
        'Redirect not found: {0}', error_doc),
    'REDIRECTEXISTS': ApiErrorMsgType(400, 'Redirect exist', 
        'Redirect exist: {0}.{1} in site {2}', error_doc),
    'VERSIONNOTFOUND': ApiErrorMsgType(404, 'Version Not Found', 
        'Version not found: {0}', error_doc),
    'VERSIONDIRNOTFOUND': ApiErrorMsgType(401, 'Version Directory Not Found', 
        'Version directory not found: {0} - {1}', error_doc),
    'MISSINGDRIVER': ApiErrorMsgType(401, 'Missing Driver', 
        'DasPanel Api server for sites is not running this driver: {0}', 
        error_doc),
}

