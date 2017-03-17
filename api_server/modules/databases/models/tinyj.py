# -*- coding: utf-8 -*-
"""Configuration models."""
from __future__ import absolute_import, division, print_function
import os
from datetime import datetime
from tinydb_jsonorm import Database
from tinydb_jsonorm import TinyJsonModel
from tinydb_jsonorm import fields
from jsonmodels import models, validators

dbucket = os.environ['DASPANEL_SYS_UUID']
DASPANEL_DATABASESFILE = '/opt/daspanel/data/' + dbucket + '/db/daspanel-databases.json'

# Open config database, creating it if not exists
DATABASES_DB = Database(DASPANEL_DATABASESFILE)

class DatabaseModel(TinyJsonModel):
    __tablename__ = "databases"

    dbprovider = fields.StringField(required=True, validators=[validators.Length(5, 63)])
    dbdescription = fields.StringField(required=True, validators=[validators.Length(1, 255)])
    dbname = fields.StringField(required=True, validators=[validators.Length(1, 63)])
    dbuser = fields.StringField(required=True, validators=[validators.Length(1, 32)])
    _last_update = fields.DateTimeField(required=True)
    _created_at = fields.DateTimeField(required=True)

    def __init__(self, *args, **kwargs):
        self._last_update = datetime.utcnow()
        self._created_at = self._last_update
        #if 'db' in kwargs:
        #    self.Meta.database = kwargs['db']
        super(DatabaseModel, self).__init__(*args, **kwargs)
        
    class Meta:
        database = DATABASES_DB


