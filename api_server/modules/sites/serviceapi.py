#!/usr/bin/env python
from __future__ import absolute_import, division, print_function
import os
from datetime import datetime
import logging
import importlib
from pprint import pprint

# Daspanel system imports
from lib.daspanel_uuid.uuid import UuidGen
from lib.daspanel_errors import DASPANEL_ERRORS
#try:
#    from daspanel_fs import DasFs
#except:
#    from lib.daspanel_fs.fslocal import DasFs

# Load configuration
import config as CONFIG

# Module imports
from modules.sites.models.tinyj import SITES_DB, SiteVersion, SiteRedirects, SiteModel
from .errors import SITES_ERRORS

# API server imports
from connexion import NoContent, request
from daspanel_connexion_utils import api_fail

def httpserver_reload(servertype):
    tenant = request.headers['Authorization']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return api_fail(DASPANEL_ERRORS, 'INVALIDAPIKEY', tenant)
    if (not CONFIG.pubsub.drivers.plugin_exist(CONFIG.pubsub.active)):
        return api_fail(DASPANEL_ERRORS, 'FSMISSINGDRIVER', CONFIG.pubsub.active)
    pubsub = CONFIG.pubsub.drivers.get_instance(CONFIG.pubsub.active, 'DasPubSub', **CONFIG.pubsub.cfg[CONFIG.pubsub.active])
    pubsub.publish('{0}:daspanel:sites'.format(tenant), 'daspanel.sites')

    return NoContent, 204

def httpserver_deactivate(cuid, servertype):
    tenant = request.headers['Authorization']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return api_fail(DASPANEL_ERRORS, 'INVALIDAPIKEY', tenant)
    try:
        site = SiteModel.get(cuid=cuid)
    except:
        return api_fail(SITES_ERRORS, 'NOTFOUND', cuid)
    if (not CONFIG.sites.drivers.plugin_exist(servertype)):
        return api_fail(SITES_ERRORS, 'MISSINGDRIVER', servertype)

    driver =  CONFIG.sites.drivers.get_instance(servertype, 'SitesConf', tenant=tenant, bucket=tenant)
    status, result = driver.deactivate(site.to_struct())
    if status:
        return NoContent, 204
    else:
        return api_fail(SITES_ERRORS, 'SITEDESACTIVATIONERROR', result, servertype)

def httpserver_activate(cuid, servertype):
    tenant = request.headers['Authorization']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return api_fail(DASPANEL_ERRORS, 'INVALIDAPIKEY', tenant)
    try:
        site = SiteModel.get(cuid=cuid)
    except:
        return api_fail(SITES_ERRORS, 'NOTFOUND', cuid)
    if (not CONFIG.sites.drivers.plugin_exist(servertype)):
        return api_fail(SITES_ERRORS, 'MISSINGDRIVER', servertype)

    driver =  CONFIG.sites.drivers.get_instance(servertype, 'SitesConf', tenant=tenant, bucket=tenant)
    status, result = driver.activate(site.to_struct())
    if status:
        return NoContent, 204
    else:
        return api_fail(SITES_ERRORS, 'SITEACTIVATIONERROR', result, servertype)

def httpserver_delete(cuid, servertype):
    tenant = request.headers['Authorization']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return api_fail(DASPANEL_ERRORS, 'INVALIDAPIKEY', tenant)
    try:
        site = SiteModel.get(cuid=cuid)
    except:
        return api_fail(SITES_ERRORS, 'NOTFOUND', cuid)
    if (not CONFIG.sites.drivers.plugin_exist(servertype)):
        return api_fail(SITES_ERRORS, 'MISSINGDRIVER', servertype)

    driver =  CONFIG.sites.drivers.get_instance(servertype, 'SitesConf', tenant=tenant, bucket=tenant)
    status, result = driver.delete(site.to_struct())
    if status:
        return NoContent, 204
    else:
        return api_fail(SITES_ERRORS, 'SITECFGDELERROR', result, servertype)

def httpserver_gencfg(cuid, servertype):
    tenant = request.headers['Authorization']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return api_fail(DASPANEL_ERRORS, 'INVALIDAPIKEY', tenant)
    try:
        site = SiteModel.get(cuid=cuid)
    except:
        return api_fail(SITES_ERRORS, 'NOTFOUND', cuid)
    if (not CONFIG.sites.drivers.plugin_exist(servertype)):
        return api_fail(SITES_ERRORS, 'MISSINGDRIVER', servertype)
    #https://github.com/veselosky/jinja2_s3loader
    #VERIFICAR SE TEM TEMPLATE DO TENANT OU SYSTEM
    #CARREGAR TEMPLATE
    #GERAR CFG USANDO TEMPLATE

    #gen_cfg = site_drivers.get_instance(servertype, 'SitesConf', tenant=tenant)
    gen_cfg =  CONFIG.sites.drivers.get_instance(servertype, 'SitesConf', tenant=tenant, bucket=tenant)
    status, result = gen_cfg.generate(site.to_struct())
    if not status:
        return api_fail(SITES_ERRORS, 'TEMPLATENOTFOUND', result, servertype)
    return NoContent, 204
    #return gen_cfg._params


