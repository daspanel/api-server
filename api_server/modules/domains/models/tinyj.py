# -*- coding: utf-8 -*-
"""Configuration models."""
from __future__ import absolute_import, division, print_function
import os
from datetime import datetime
from tinydb_jsonorm import Database
from tinydb_jsonorm import TinyJsonModel
from tinydb_jsonorm import fields
from jsonmodels import models, validators
from tinydb import where

dbucket = os.environ['DASPANEL_GUUID']
DASPANEL_DATABASESFILE = '/opt/daspanel/data/' + dbucket + '/db/daspanel-domains.json'

# Open config database, creating it if not exists
DOMAINS_DB = Database(DASPANEL_DATABASESFILE)


class DomainModel(TinyJsonModel):
    __tablename__ = "domains"

    domain = fields.StringField(required=True, validators=[validators.Length(1, 255)])
    dnsprovider = fields.StringField(required=True, validators=[validators.Length(1, 25)])
    _last_update = fields.DateTimeField(required=True)
    _created_at = fields.DateTimeField(required=True)

    def __init__(self, *args, **kwargs):
        self._last_update = datetime.utcnow()
        self._created_at = self._last_update
        #if 'db' in kwargs:
        #    self.Meta.database = kwargs['db']
        super(DomainModel, self).__init__(*args, **kwargs)

    @classmethod
    def domainexist(cls, domain):
        table = cls.Meta.database.table(cls.__tablename__)
        query = where('domain') == domain
        row = table.get(cond=query)
        if row is not None:
            return True
        else:
            return False
    
    class Meta:
        database = DOMAINS_DB


