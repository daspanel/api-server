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
from .models.tinyj import SITES_DB, SiteVersion, SiteRedirects, SiteModel
from .errors import SITES_ERRORS

# API server imports
from connexion import request, NoContent
from daspanel_connexion_utils import api_fail

def redirects_get_all(cuid):
    tenant = request.headers['Authorization']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return api_fail(DASPANEL_ERRORS, 'INVALIDAPIKEY', tenant)
    try:
        site = SiteModel.get(cuid=cuid)
    except:
        return api_fail(SITES_ERRORS, 'NOTFOUND', cuid)
    return site.to_struct()['redirects']

def redirects_get_item(cuid, rcuid):
    tenant = request.headers['Authorization']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return api_fail(DASPANEL_ERRORS, 'INVALIDAPIKEY', tenant)
    try:
        site = SiteModel.get(cuid=cuid)
    except:
        return api_fail(SITES_ERRORS, 'NOTFOUND', cuid)
    redirect = None
    for v in site.to_struct()['redirects']:
        if v['_cuid'] == rcuid:
            redirect = v
            break 
    if redirect == None:
        return api_fail(SITES_ERRORS, 'REDIRECTNOTFOUND', rcuid)
    return redirect

def redirects_edit_item(cuid, rcuid, bdata):
    tenant = request.headers['Authorization']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return api_fail(DASPANEL_ERRORS, 'INVALIDAPIKEY', tenant)
    if (not CONFIG.pubsub.drivers.plugin_exist(CONFIG.pubsub.active)):
        return api_fail(DASPANEL_ERRORS, 'PSMISSINGDRIVER', CONFIG.pubsub.active)

    try:
        site = SiteModel.get(cuid=cuid)
    except:
        return api_fail(SITES_ERRORS, 'NOTFOUND', cuid)
    if not site.version_exist(bdata['version']):
        return api_fail(SITES_ERRORS, 'VERSIONNOTFOUND', bdata['version'], site_id)

    redirects = site.to_struct()['redirects']
    vedit = -1
    for i, v in enumerate(redirects):
        if v['_cuid'] == rcuid:
            vedit = i
            break
    if vedit == -1:
        return api_fail(SITES_ERRORS, 'REDIRECTNOTFOUND', rcuid)

    redirects[vedit]['hosturl'] = bdata['hosturl']
    redirects[vedit]['domain'] = bdata['domain']
    redirects[vedit]['ssl'] = bdata['ssl']
    redirects[vedit]['sslcert'] = bdata['sslcert']
    redirects[vedit]['version'] = bdata['version']
    site.redirects = redirects
    site._last_update = datetime.utcnow()
    site.validate()
    site.save()

    pubsub = CONFIG.pubsub.drivers.get_instance(CONFIG.pubsub.active, 'DasPubSub', password=tenant)
    pubsub.publish('{0}:daspanel:sites'.format(tenant), 'daspanel.sites')

    return redirects[vedit], 200

def redirects_delete_item(cuid, rcuid):
    tenant = request.headers['Authorization']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return api_fail(DASPANEL_ERRORS, 'INVALIDAPIKEY', tenant)
    if (not CONFIG.pubsub.drivers.plugin_exist(CONFIG.pubsub.active)):
        return api_fail(DASPANEL_ERRORS, 'PSMISSINGDRIVER', CONFIG.pubsub.active)

    try:
        site = SiteModel.get(cuid=cuid)
    except:
        return api_fail(SITES_ERRORS, 'NOTFOUND', cuid)

    redirects = site.to_struct()['redirects']
    vdel = -1
    for i, v in enumerate(redirects):
        if v['_cuid'] == rcuid:
            vdel = i
            break
    if vdel == -1:
        return api_fail(SITES_ERRORS, 'REDIRECTNOTFOUND', rcuid)

    del redirects[vdel]
    site.redirects = redirects
    site._last_update = datetime.utcnow()
    site.validate()
    site.save()

    pubsub = CONFIG.pubsub.drivers.get_instance(CONFIG.pubsub.active, 'DasPubSub', password=tenant)
    pubsub.publish('{0}:daspanel:sites'.format(tenant), 'daspanel.sites')


def redirects_new_item(cuid, bdata):
    tenant = request.headers['Authorization']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return api_fail(DASPANEL_ERRORS, 'INVALIDAPIKEY', tenant)
    if (not CONFIG.pubsub.drivers.plugin_exist(CONFIG.pubsub.active)):
        return api_fail(DASPANEL_ERRORS, 'PSMISSINGDRIVER', CONFIG.pubsub.active)

    try:
        site = SiteModel.get(cuid=cuid)
    except:
        return api_fail(SITES_ERRORS, 'NOTFOUND', cuid)
    if not site.version_exist(bdata['version']):
        return api_fail(SITES_ERRORS, 'VERSIONNOTFOUND', bdata['version'], site_id)
    result, site_id = site.redirected_used(bdata['domain'], bdata['hosturl'])
    if result:
        return api_fail(SITES_ERRORS, 'REDIRECTEXISTS', bdata['hosturl'], bdata['domain'], site_id)
    newredir = SiteRedirects(**bdata)
    newredir.validate()
    site.redirects.append(newredir)
    site._last_update = datetime.utcnow()
    site.validate()
    site.save()

    pubsub = CONFIG.pubsub.drivers.get_instance(CONFIG.pubsub.active, 'DasPubSub', password=tenant)
    pubsub.publish('{0}:daspanel:sites'.format(tenant), 'daspanel.sites')

    return newredir.to_struct(), 201


def versions_activate(cuid, vcuid):
    tenant = request.headers['Authorization']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return api_fail(DASPANEL_ERRORS, 'INVALIDAPIKEY', tenant)
    if (not CONFIG.pubsub.drivers.plugin_exist(CONFIG.pubsub.active)):
        return api_fail(DASPANEL_ERRORS, 'PSMISSINGDRIVER', CONFIG.pubsub.active)

    try:
        site = SiteModel.get(cuid=cuid)
    except:
        return api_fail(SITES_ERRORS, 'NOTFOUND', cuid)
    versions = site.to_struct()['versions']
    vedit = -1
    for i, v in enumerate(versions):
        if v['_cuid'] == vcuid:
            vedit = i
            break
    if vedit == -1:
        return api_fail(SITES_ERRORS, 'VERSIONNOTFOUND', vcuid)
    site.active_version = versions[vedit]['_cuid']
    site.active_dir = versions[vedit]['directory']
    site._last_update = datetime.utcnow()
    site.validate()
    site.save()
    pubsub = CONFIG.pubsub.drivers.get_instance(CONFIG.pubsub.active, 'DasPubSub', password=tenant)
    pubsub.publish('{0}:daspanel:sites'.format(tenant), 'daspanel.sites')

    return site.to_struct(), 200

def versions_clone(cuid, vcuid):
    tenant = request.headers['Authorization']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return api_fail(DASPANEL_ERRORS, 'INVALIDAPIKEY', tenant)
    if (not CONFIG.fs.drivers.plugin_exist(CONFIG.fs.active)):
        return api_fail(DASPANEL_ERRORS, 'FSMISSINGDRIVER', CONFIG.fs.active)
    if (not CONFIG.pubsub.drivers.plugin_exist(CONFIG.pubsub.active)):
        return api_fail(DASPANEL_ERRORS, 'PSMISSINGDRIVER', CONFIG.pubsub.active)

    try:
        site = SiteModel.get(cuid=cuid)
    except:
        return api_fail(SITES_ERRORS, 'NOTFOUND', cuid)

    versions = site.to_struct()['versions']
    vedit = -1
    for i, v in enumerate(versions):
        if v['_cuid'] == vcuid:
            vedit = i
            break
    if vedit == -1:
        return api_fail(SITES_ERRORS, 'VERSIONNOTFOUND', vcuid)

    fs = CONFIG.fs.drivers.get_instance(CONFIG.fs.active, 'DasFs', tenant=tenant, bucket=tenant)
    if not fs.exists(versions[vedit]['directory']):
        return api_fail(SITES_ERRORS, 'VERSIONDIRNOTFOUND', vcuid, versions[vedit]['directory'])

    newver = SiteVersion()
    newver.date = datetime.utcnow()
    newver.description = 'Clone of version: ' + versions[vedit]['description']
    newver.tag = '0.1.0'
    newver.directory = 'content/' + cuid + '/v/' + '{:%Y-%m-%d-%H%M%S-%f}'.format(newver.date)
    newver.sitetype = versions[vedit]["sitetype"]
    newver.runtime = versions[vedit]["runtime"]
    newver.validate()
    site.versions.append(newver)
    site._last_update = datetime.utcnow()
    site.validate()
    site.save()

    if fs.exists(newver.directory):
        fs.rmtree(newver.directory)
    fs.cptree(versions[vedit]['directory'], newver.directory)

    pubsub = CONFIG.pubsub.drivers.get_instance(CONFIG.pubsub.active, 'DasPubSub', password=tenant)
    pubsub.publish('{0}:daspanel:sites'.format(tenant), 'daspanel.sites')

    return newver.to_struct(), 201

def versions_edit_item(cuid, vcuid, bdata):
    tenant = request.headers['Authorization']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return api_fail(DASPANEL_ERRORS, 'INVALIDAPIKEY', tenant)
    if (not CONFIG.pubsub.drivers.plugin_exist(CONFIG.pubsub.active)):
        return api_fail(DASPANEL_ERRORS, 'PSMISSINGDRIVER', CONFIG.pubsub.active)

    try:
        site = SiteModel.get(cuid=cuid)
    except:
        return api_fail(SITES_ERRORS, 'NOTFOUND', cuid)
    versions = site.to_struct()['versions']
    vedit = -1
    for i, v in enumerate(versions):
        if v['_cuid'] == vcuid:
            vedit = i
            break
    if vedit == -1:
        return api_fail(SITES_ERRORS, 'VERSIONNOTFOUND', vcuid)
    versions[vedit]['description'] = bdata['description']
    versions[vedit]['tag'] = bdata['tag']
    versions[vedit]['sitetype'] = bdata["sitetype"]
    versions[vedit]['runtime'] = bdata["runtime"]

    site.versions = versions
    site._last_update = datetime.utcnow()
    site.validate()
    site.save()

    pubsub = CONFIG.pubsub.drivers.get_instance(CONFIG.pubsub.active, 'DasPubSub', password=tenant)
    pubsub.publish('{0}:daspanel:sites'.format(tenant), 'daspanel.sites')

    return versions[vedit], 200

def versions_delete_item(cuid, vcuid):
    tenant = request.headers['Authorization']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return api_fail(DASPANEL_ERRORS, 'INVALIDAPIKEY', tenant)
    if (not CONFIG.fs.drivers.plugin_exist(CONFIG.fs.active)):
        return api_fail(DASPANEL_ERRORS, 'FSMISSINGDRIVER', CONFIG.fs.active)
    if (not CONFIG.pubsub.drivers.plugin_exist(CONFIG.pubsub.active)):
        return api_fail(DASPANEL_ERRORS, 'PSMISSINGDRIVER', CONFIG.pubsub.active)

    try:
        site = SiteModel.get(cuid=cuid)
    except:
        return api_fail(SITES_ERRORS, 'NOTFOUND', cuid)
    if site.active_version == vcuid:
        return api_fail(SITES_ERRORS, 'VERSIONISACTIVE', vcuid, site.sitedescription)
        #return {"errors": [], "message": "Cann't delete current active version of the site"}, 400

    #somelist[:] = [tup for tup in somelist if determine(tup)]
    versions = site.to_struct()['versions']
    vdel = -1
    for i, v in enumerate(versions):
        if v['_cuid'] == vcuid:
            vdel = i
            break
    if vdel == -1:
        return api_fail(SITES_ERRORS, 'VERSIONNOTFOUND', vcuid)

    fs = CONFIG.fs.drivers.get_instance(CONFIG.fs.active, 'DasFs', tenant=tenant, bucket=tenant)
    if fs.exists(versions[vdel]['directory']):
        fs.rmtree(versions[vdel]['directory'])

    del versions[vdel]
    site.versions = versions
    site._last_update = datetime.utcnow()
    site.validate()
    site.save()

    pubsub = CONFIG.pubsub.drivers.get_instance(CONFIG.pubsub.active, 'DasPubSub', password=tenant)
    pubsub.publish('{0}:daspanel:sites'.format(tenant), 'daspanel.sites')

    return NoContent, 204

def versions_get_item(cuid, vcuid):
    tenant = request.headers['Authorization']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return api_fail(DASPANEL_ERRORS, 'INVALIDAPIKEY', tenant)
    try:
        site = SiteModel.get(cuid=cuid)
    except:
        return api_fail(SITES_ERRORS, 'NOTFOUND', cuid)
    version = None
    for v in site.to_struct()['versions']:
        if v['_cuid'] == vcuid:
            version = v
            break 
    if version == None:
        return api_fail(SITES_ERRORS, 'VERSIONNOTFOUND', vcuid)
    return version

def versions_get_all(cuid):
    tenant = request.headers['Authorization']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return api_fail(DASPANEL_ERRORS, 'INVALIDAPIKEY', tenant)
    try:
        site = SiteModel.get(cuid=cuid)
    except:
        return api_fail(SITES_ERRORS, 'NOTFOUND', cuid)
    return site.to_struct()['versions']


def versions_new_item(cuid, bdata):
    tenant = request.headers['Authorization']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return api_fail(DASPANEL_ERRORS, 'INVALIDAPIKEY', tenant)
    if (not CONFIG.fs.drivers.plugin_exist(CONFIG.fs.active)):
        return api_fail(DASPANEL_ERRORS, 'FSMISSINGDRIVER', CONFIG.fs.active)
    if (not CONFIG.pubsub.drivers.plugin_exist(CONFIG.pubsub.active)):
        return api_fail(DASPANEL_ERRORS, 'PSMISSINGDRIVER', CONFIG.pubsub.active)

    try:
        site = SiteModel.get(cuid=cuid)
    except:
        return api_fail(SITES_ERRORS, 'NOTFOUND', cuid)

    newver = SiteVersion(**bdata)
    newver.date = datetime.utcnow()
    newver.directory = 'content/' + cuid + '/v/' + '{:%Y-%m-%d-%H%M%S-%f}'.format(newver.date)
    newver.validate()
    site.versions.append(newver)
    site._last_update = datetime.utcnow()
    site.validate()
    site.save()

    fs = CONFIG.fs.drivers.get_instance(CONFIG.fs.active, 'DasFs', tenant=tenant, bucket=tenant)
    fs.mkdir(newver.directory)

    pubsub = CONFIG.pubsub.drivers.get_instance(CONFIG.pubsub.active, 'DasPubSub', password=tenant)
    pubsub.publish('{0}:daspanel:sites'.format(tenant), 'daspanel.sites')

    return newver.to_struct(), 201

def get_item(cuid):
    tenant = request.headers['Authorization']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return api_fail(DASPANEL_ERRORS, 'INVALIDAPIKEY', tenant)
    try:
        site = SiteModel.get(cuid=cuid)
    except:
        return api_fail(SITES_ERRORS, 'NOTFOUND', cuid)
    return site.to_struct()

def get_httpconf(hostname):
    tenant = request.headers['Authorization']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return api_fail(DASPANEL_ERRORS, 'INVALIDAPIKEY', tenant)
    sites = SiteModel.all()
    entries = []
    for site in sites:
        sitecfg = {
            '_cuid': site._cuid,
            'sitedescription': site.sitedescription,
            'enabled': True,
            'configs': []
        }
        for version in site.versions:
            vrec = {
                'sitetype': version.sitetype,
                'engine': version.runtime,
                'name': '{0}.v.{1}.sites.{2}'.format(version._cuid, site._cuid, hostname),
                'ssl': 'self',
                'sslcert': '',
                'certpath': '',
                'dir': version.directory,
                'domain': hostname
            }
            sitecfg['configs'].append(vrec)
            if not site.urlprefix == site._cuid:
                vrec = {
                    'sitetype': version.sitetype,
                    'engine': version.runtime,
                    'name': '{0}.v.{1}.sites.{2}'.format(version._cuid, site.urlprefix, hostname),
                    'ssl': 'self',
                    'sslcert': '',
                    'certpath': '',
                    'dir': version.directory,
                    'domain': hostname
                }
                sitecfg['configs'].append(vrec)

        for host in site.redirects:
            result, host_version = site.get_version(host.version)
            if not result:
                return api_fail(SITES_ERRORS, 'VERSIONNOTFOUND', host.version)
            hrec = {
                'sitetype': host_version['sitetype'],
                'engine': host_version['runtime'],
                'name': '{0}.{1}'.format(host.hosturl, host.domain),
                'ssl': host.ssl,
                'sslcert': '',
                'certpath': '/certs',
                'dir': host_version['directory'],
                'domain': host.domain
            }
            #if host.ssl:
            hrec['certpath'] = '/certs/{0}'.format(host.domain)
            sitecfg['configs'].append(hrec)
            if host.hosturl == 'www':
                hrec = {
                    'sitetype': host_version['sitetype'],
                    'engine': host_version['runtime'],
                    'name': '{0}'.format(host.domain),
                    'ssl': host.ssl,
                    'sslcert': '',
                    'certpath': '/certs',
                    'dir': host_version['directory'],
                    'domain': host.domain
                }
                #if host.ssl:
                hrec['certpath'] = '/certs/{0}'.format(host.domain)
                sitecfg['configs'].append(hrec)

        result, cur_version = site.get_version(site.active_version)
        if not result:
            return api_fail(SITES_ERRORS, 'VERSIONNOTFOUND', site.active_version)
        master = {
            'sitetype': cur_version['sitetype'],
            'engine': cur_version['runtime'],
            'name': '{0}.sites.{1}'.format(site._cuid, hostname),
            'ssl': 'self',
            'sslcert': '',
            'certpath': '',
            'dir': site.active_dir,
            'domain': hostname
        }
        sitecfg['configs'].append(master)
        if not site.urlprefix == site._cuid:
            master = {
                'sitetype': cur_version['sitetype'],
                'engine': cur_version['runtime'],
                'name': '{0}.sites.{1}'.format(site.urlprefix, hostname),
                'ssl': 'self',
                'sslcert': '',
                'certpath': '',
                'dir': site.active_dir,
                'domain': hostname
            }
            sitecfg['configs'].append(master)

        entries.append(sitecfg)
    return entries


def get_all():
    tenant = request.headers['Authorization']
    if (not CONFIG.tenant.drivers.plugin_exist(CONFIG.tenant.active)):
        return api_fail(DASPANEL_ERRORS, 'TENANTMISSINGDRIVER', CONFIG.tenant.active)
    cur_tenant = CONFIG.tenant.drivers.get_instance(CONFIG.tenant.active, 'DasTenant', tenant=request.headers['Authorization'])
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return api_fail(DASPANEL_ERRORS, 'INVALIDAPIKEY', tenant)
    all_rows = SiteModel.all()
    return [site.to_struct() for site in all_rows]

def new_item(bdata):
    tenant = request.headers['Authorization']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return api_fail(DASPANEL_ERRORS, 'INVALIDAPIKEY', tenant)
    if (not CONFIG.fs.drivers.plugin_exist(CONFIG.fs.active)):
        return api_fail(DASPANEL_ERRORS, 'FSMISSINGDRIVER', CONFIG.fs.active)
    if (not CONFIG.pubsub.drivers.plugin_exist(CONFIG.pubsub.active)):
        return api_fail(DASPANEL_ERRORS, 'PSMISSINGDRIVER', CONFIG.pubsub.active)

    newrec = SiteModel(**bdata)
    newrec.urlprefix = newrec._cuid
    newrec._created_at = datetime.utcnow()
    newrec._last_update = newrec._created_at
    newver = SiteVersion()
    newver.date = newrec._created_at
    newver.description = 'Initial version'
    newver.tag = '0.1.0'
    newver.sitetype = bdata['sitetype']
    newver.runtime = bdata['runtime']
    newver.directory = 'content/' + newrec._cuid + '/v/' + '{:%Y-%m-%d-%H%M%S-%f}'.format(newver.date)
    newver.validate()
    newrec.versions.append(newver)
    newrec.active_version = newver._cuid
    newrec.active_dir = newver.directory
    newrec.redirects = []    
    newrec.validate()
    newrec.insert()
    fs = CONFIG.fs.drivers.get_instance(CONFIG.fs.active, 'DasFs', tenant=tenant, bucket=tenant)
    if not fs.exists(newver.directory):
        fs.mkdir(newver.directory)

    pubsub = CONFIG.pubsub.drivers.get_instance(CONFIG.pubsub.active, 'DasPubSub', password=tenant)
    pubsub.publish('{0}:daspanel:sites'.format(tenant), 'daspanel.sites')

    return newrec.to_struct(), 201

def edit_item(cuid, bdata):
    tenant = request.headers['Authorization']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return api_fail(DASPANEL_ERRORS, 'INVALIDAPIKEY', tenant)
    if (not CONFIG.pubsub.drivers.plugin_exist(CONFIG.pubsub.active)):
        return api_fail(DASPANEL_ERRORS, 'PSMISSINGDRIVER', CONFIG.pubsub.active)

    try:
        rec2edit = SiteModel.get(cuid=cuid)
    except:
        return api_fail(SITES_ERRORS, 'NOTFOUND', cuid)

    result, site_id = rec2edit.urlprefix_used(bdata["urlprefix"])
    if result and (not cuid == site_id):
        return api_fail(SITES_ERRORS, 'URLPREFIXEXIST', bdata["urlprefix"], site_id)

    rec2edit.sitedescription = bdata["sitedescription"]
    rec2edit.urlprefix = bdata["urlprefix"]
    rec2edit._last_update = datetime.utcnow()
    rec2edit.validate()
    rec2edit.save()

    pubsub = CONFIG.pubsub.drivers.get_instance(CONFIG.pubsub.active, 'DasPubSub', password=tenant)
    pubsub.publish('{0}:daspanel:sites'.format(tenant), 'daspanel.sites')

    #return {"newpaswd": "xxxxx"}, 200
    
def delete_item(cuid):
    tenant = request.headers['Authorization']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return api_fail(DASPANEL_ERRORS, 'INVALIDAPIKEY', tenant)
    if (not CONFIG.fs.drivers.plugin_exist(CONFIG.fs.active)):
        return api_fail(DASPANEL_ERRORS, 'FSMISSINGDRIVER', CONFIG.fs.active)
    if (not CONFIG.pubsub.drivers.plugin_exist(CONFIG.pubsub.active)):
        return api_fail(DASPANEL_ERRORS, 'PSMISSINGDRIVER', CONFIG.pubsub.active)

    try:
        rec2delete = SiteModel.get(cuid=cuid)
    except:
        return api_fail(SITES_ERRORS, 'NOTFOUND', cuid)

    fs = CONFIG.fs.drivers.get_instance(CONFIG.fs.active, 'DasFs', tenant=tenant, bucket=tenant)
    if fs.exists('content/' + cuid):
        fs.rmtree('content/' + cuid)

    pubsub = CONFIG.pubsub.drivers.get_instance(CONFIG.pubsub.active, 'DasPubSub', password=tenant)
    pubsub.publish('{0}:daspanel:sites'.format(tenant), 'daspanel.sites')

    rec2delete.delete()

def chgpwd_item(cuid, bdata):
    tenant = request.headers['Authorization']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return api_fail(DASPANEL_ERRORS, 'INVALIDAPIKEY', tenant)
    try:
        rec2edit = SiteModel.get(cuid=cuid)
    except:
        return api_fail(SITES_ERRORS, 'NOTFOUND', cuid)
    if "password" in bdata:
        newpwd = bdata["password"]
    else:
        uuid = UuidGen()
        newpwd = uuid.gen_pass()
    return {"password": newpwd}, 200




