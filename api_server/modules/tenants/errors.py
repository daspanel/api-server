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

error_doc = 'https://daspanel.com/docs/api/tenants/errors'

TENANTS_ERRORS = {
    'NOTFOUND': ApiErrorMsgType(404, 'Not Found', 
        'Tenant not found: {0}', error_doc),
    'MISSINGDRIVER': ApiErrorMsgType(401, 'Missing Driver', 
        'DasPanel Api server for tenants is not running this driver: {0}', 
        error_doc),
}

