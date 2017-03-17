#!/usr/bin/env python
from __future__ import absolute_import, division, print_function
import os
from datetime import datetime
import logging
import pprint

from modules.domains.models.tinyj import DOMAINS_DB, DomainModel
from modules.sites.models.tinyj import SITES_DB, SiteModel
from connexion import NoContent, request
#NoContent = object()


def get_item(cuid):
    tenant = request.headers['X-Api-Key']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return {"message": "Invalid X-Api-Key: {0}".format(tenant)}, 401
    try:
        rec = DomainModel.get(cuid=cuid)
    except:
        return NoContent, 404
    return rec.to_struct()

def get_all():
    tenant = request.headers['X-Api-Key']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return {"message": "Invalid X-Api-Key: {0}".format(tenant)}, 401
    all_rows = DomainModel.all()
    return [rec.to_struct() for rec in all_rows]

def new_item(bdata):
    tenant = request.headers['X-Api-Key']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return {"message": "Invalid X-Api-Key: {0}".format(tenant)}, 401
    if DomainModel.domainexist(bdata['domain']):
        return {"message": "Domain already exist in database: {0}".format(bdata['domain'])}, 401
    newrec = DomainModel(**bdata)
    newrec._created_at = datetime.utcnow()
    newrec._last_update = newrec._created_at
    newrec.validate()
    newrec.insert()
    return newrec.to_struct(), 201

def edit_item(cuid, bdata):
    tenant = request.headers['X-Api-Key']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return {"message": "Invalid X-Api-Key: {0}".format(tenant)}, 401
    try:
        rec2edit = DomainModel.get(cuid=cuid)
    except:
        return NoContent, 404
    rec2edit.dnsprovider = bdata["dnsprovider"]
    rec2edit._last_update = datetime.utcnow()
    rec2edit.validate()
    rec2edit.save()
    
def delete_item(cuid):
    tenant = request.headers['X-Api-Key']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return {"message": "Invalid X-Api-Key: {0}".format(tenant)}, 401
    try:
        rec2delete = DomainModel.get(cuid=cuid)
    except:
        return NoContent, 404
    if SiteModel.domainredirected(rec2delete.domain):
        return {"message": "Domain in use by site redirect: {0}".format(rec2delete.domain)}, 401

    rec2delete.delete()



