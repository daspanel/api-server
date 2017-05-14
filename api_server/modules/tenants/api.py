#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import os
from datetime import datetime
import logging
from pprint import pprint

# Daspanel system imports
from lib.daspanel_uuid.uuid import UuidGen
from lib.daspanel_errors import DASPANEL_ERRORS, error_msg

# Load configuration
import config as CONFIG

# Module imports
from .errors import TENANTS_ERRORS

# API server imports
from connexion import request, NoContent
from daspanel_connexion_utils import api_fail

def get_tenant(cuid):
    tenant = CONFIG.tenant.drivers.get_instance(CONFIG.tenant.active, 'DasTenant', tenant=cuid)
    if not tenant.auth(request.headers['Authorization']):
        return api_fail(DASPANEL_ERRORS, 'INVALIDAPIKEY', tenant)
    return CONFIG.daspanel.def_cfg
