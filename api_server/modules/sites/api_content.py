#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""API Server

Daspanel API server - Sites module

 :copyright: (c) 2016, Abner G Jacobsen.
             All rights reserved.
 :license:   GNU General Public License v3, see LICENSE for more details.
"""
from __future__ import absolute_import, division, print_function
import os, pycurl
from datetime import datetime
import logging
import importlib
from pprint import pprint

# Daspanel system imports
from lib.daspanel_uuid.uuid import UuidGen
from lib.daspanel_errors import DASPANEL_ERRORS

# Load configuration
import config as CONFIG

# Module imports
from .models.tinyj import SITES_DB, SiteVersion, SiteRedirects, SiteModel
from .errors import SITES_ERRORS

# API server imports
from connexion import NoContent, request
from daspanel_connexion_utils import api_fail

def install_remotezip(cuid, bdata):
    tenant = request.headers['X-Api-Key']
    if not tenant == os.environ['DASPANEL_GUUID']:
        return api_fail(DASPANEL_ERRORS, 'INVALIDAPIKEY', tenant)
    try:
        site = SiteModel.get(cuid=cuid)
    except:
        return api_fail(SITES_ERRORS, 'NOTFOUND', cuid)
    print(bdata)

    content_id = UuidGen().gen_uniqid()
    tmp_file = 'upload/tmp/{0}.zip'.format(content_id)
    tmp_dir  = 'upload/tmp/{0}.tmp'.format(content_id)
    fs = CONFIG.fs.drivers.get_instance(CONFIG.fs.active, 'DasFs', tenant=tenant, bucket=tenant)
    if not fs.exists(tmp_file):
        fs.mkdir(tmp_dir)
        with fs.open(tmp_file, 'wb') as f:
            c = pycurl.Curl()
            c.setopt(c.URL, bdata['url'])
            c.setopt(c.FOLLOWLOCATION, True)
            c.setopt(c.VERBOSE, 1)
            c.setopt(c.WRITEDATA, f)
            c.perform()
            c.close()

        if fs.is_zip(tmp_file) is False:
            fs.remove(tmp_file)
            fs.rmtree(tmp_dir)
            return api_fail(DASPANEL_ERRORS, 'NOTZIPFILE', bdata['url'])

        fs.extract_zip(tmp_file, tmp_dir)
        fs.remove(tmp_file)

        content_root = fs.site_root(tmp_dir)
        if content_root == None:
            fs.remove(tmp_file)
            fs.rmtree(tmp_dir)
            return api_fail(SITES_ERRORS, 'CONTENTWITHOUTINDEX', bdata['url'])

        print ('Copying from: ', content_root, 'To: ', site.active_dir)
        fs.copy_tree(content_root, site.active_dir)
        fs.rmtree(tmp_dir)

    else:
        return api_fail(DASPANEL_ERRORS, 'FSFILEEXISTS', tmp_file)

    return {"location": site.active_dir}, 202

