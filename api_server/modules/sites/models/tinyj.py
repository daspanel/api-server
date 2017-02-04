# -*- coding: utf-8 -*-
"""Configuration models."""
from __future__ import absolute_import, division, print_function
import os
from datetime import datetime
from tinydb_jsonorm import Database
from tinydb_jsonorm import TinyJsonModel
from tinydb_jsonorm import fields
from jsonmodels import models, validators

dbucket = os.environ['DASPANEL_GUUID']
DASPANEL_DATABASESFILE = '/opt/daspanel/data/' + dbucket + '/db/daspanel-sites.json'

# Open sites database, creating it if not exists
SITES_DB = Database(DASPANEL_DATABASESFILE)

class SiteVersion(TinyJsonModel):
    __tablename__ = "siteversions"
    description = fields.StringField(required=True, validators=[validators.Length(1, 255)])
    tag = fields.StringField(required=True, validators=[validators.Length(1, 255)])
    date = fields.DateTimeField(required=True)
    directory = fields.StringField(required=True, validators=[validators.Length(1, 255)])


class SiteRedirects(TinyJsonModel):
    __tablename__ = "siteredirects"
    hosturl = fields.StringField(required=True, validators=[validators.Length(0, 255)])
    domain = fields.StringField(required=True, validators=[validators.Length(1, 255)])
    ssl = fields.BoolField(required=True)
    sslcert = fields.StringField(required=False, validators=[validators.Length(0, 255)])
    sslkey = fields.StringField(required=False, validators=[validators.Length(0, 255)])


class SiteModel(TinyJsonModel):
    __tablename__ = "sites"
    urlprefix = fields.StringField(required=True, validators=[validators.Length(1, 255)])
    sitetype = fields.StringField(required=True, validators=[validators.Length(1, 64)])
    sitedescription = fields.StringField(required=True, validators=[validators.Length(1, 255)])
    runtime = fields.StringField(required=True, validators=[validators.Length(1, 64)])
    versions = fields.ListField(['SiteVersion'])
    redirects = fields.ListField(['SiteRedirects'])
    active_version = fields.StringField(required=True, validators=[validators.Length(1, 25)])
    active_dir = fields.StringField(required=True, validators=[validators.Length(1, 255)])
    _last_update = fields.DateTimeField(required=True)
    _created_at = fields.DateTimeField(required=True)

    def __init__(self, *args, **kwargs):
        self._last_update = datetime.utcnow()
        self._created_at = self._last_update
        #if 'db' in kwargs:
        #    self.Meta.database = kwargs['db']
        super(SiteModel, self).__init__(*args, **kwargs)

    def redirectexist(self, domain, host):
        records = self.to_struct()['redirects']
        for i, v in enumerate(records):
            if v['domain'] == domain and v['hosturl'] == host:
                return True
        return False

    @classmethod
    def redirected_used(cls, domain, host):
        table = cls.Meta.database.table(cls.__tablename__)
        allrec = table.all()
        for rec in allrec:
            sublst = rec['redirects']
            for i, v in enumerate(sublst):
                if v['domain'] == domain and v['hosturl'] == host:
                    return True, rec['_cuid']
        return False, None

    @classmethod
    def urlprefix_used(cls, prefix):
        table = cls.Meta.database.table(cls.__tablename__)
        allrec = table.all()
        for rec in allrec:
            if rec['urlprefix'] == prefix:
                return True, rec['_cuid']
        return False, None
        
    class Meta:
        database = SITES_DB


