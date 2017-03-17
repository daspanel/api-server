#!/usr/bin/env python
from __future__ import absolute_import, division, print_function
import os
from datetime import datetime
import logging
import pprint

from modules.databases.models.tinyj import DATABASES_DB, DatabaseModel
from lib.daspanel_uuid.uuid import UuidGen
from connexion import NoContent, request
#NoContent = object()


def get_item(cuid):
    tenant = request.headers['X-Api-Key']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return {"message": "Invalid X-Api-Key: {0}".format(tenant)}, 401
    try:
        database = DatabaseModel.get(cuid=cuid)
    except:
        return NoContent, 404
    return database.to_struct()

def get_all():
    tenant = request.headers['X-Api-Key']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return {"message": "Invalid X-Api-Key: {0}".format(tenant)}, 401
    all_rows = DatabaseModel.all()
    return [db.to_struct() for db in all_rows]

def new_item(bdata):
    tenant = request.headers['X-Api-Key']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return {"message": "Invalid X-Api-Key: {0}".format(tenant)}, 401
    uuid = UuidGen()
    newrec = DatabaseModel(**bdata)
    dbpwd = uuid.gen_pass()
    newrec._created_at = datetime.utcnow()
    newrec._last_update = newrec._created_at
    newrec.validate()
    newrec.insert()
    return {"password": dbpwd}, 201

def edit_item(cuid, bdata):
    tenant = request.headers['X-Api-Key']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return {"message": "Invalid X-Api-Key: {0}".format(tenant)}, 401
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return NoContent, 401
    try:
        rec2edit = DatabaseModel.get(cuid=cuid)
    except:
        return NoContent, 404
    rec2edit.dbdescription = bdata["dbdescription"]
    rec2edit._last_update = datetime.utcnow()
    rec2edit.validate()
    rec2edit.save()
    #return {"newpaswd": "xxxxx"}, 200
    
def delete_item(cuid):
    tenant = request.headers['X-Api-Key']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return {"message": "Invalid X-Api-Key: {0}".format(tenant)}, 401
    try:
        rec2delete = DatabaseModel.get(cuid=cuid)
    except:
        return NoContent, 404
    rec2delete.delete()

def chgpwd_item(cuid, bdata):
    tenant = request.headers['X-Api-Key']
    if not tenant == os.environ['DASPANEL_SYS_UUID']:
        return {"message": "Invalid X-Api-Key: {0}".format(tenant)}, 401
    try:
        rec2edit = DatabaseModel.get(cuid=cuid)
    except:
        return NoContent, 404
    if "password" in bdata:
        newpwd = bdata["password"]
    else:
        uuid = UuidGen()
        newpwd = uuid.gen_pass()
    return {"password": newpwd}, 200

def get_database2s():
    #all_rows = DatabaseModel.all()
    table = DATABASES_DB.table(DatabaseModel.__tablename__, cache_size=None)
    all_rows = table.all()
    qlist = []
    qlist = [DatabaseModel(eid=row.eid, **row) for row in all_rows]
    print("\nRecords in database: %d" % len(qlist))
    for rec in qlist:
        print("Rec: ", rec.id, rec._cuid, rec.dbprovider, rec.dbdescription, rec.dbname, rec.dbuser)
        print(rec.to_struct())
    #return all_rows
    return [db.to_struct() for db in qlist]




