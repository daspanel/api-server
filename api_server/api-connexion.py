#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""API Server

Daspanel API server

 :copyright: (c) 2016, Abner G Jacobsen.
             All rights reserved.
 :license:   GNU General Public License v3, see LICENSE for more details.

"""
from __future__ import absolute_import, division, print_function
from __about__ import *
import os, sys
import connexion
from flask_cors import CORS
import datetime
import logging

import config as CONFIG

logger = logging.getLogger(__name__)

from modules.sites.models.tinyj import SITES_DB_FMT
from modules.sites.db_migration import SitesDbMigrate
upg_sites = SitesDbMigrate(SITES_DB_FMT)
if not upg_sites.migrate():
    print("\n==== Sites DB Migrate Failed ====")
    for step, status in upg_sites.steps_done.items():
        print(step, status)
    sys.exit()
else:
    print("\n==== Sites DB Migrate Success ====")

del(SITES_DB_FMT)
del(SitesDbMigrate)

# Create Connexion app
app = connexion.App(__name__)

# Add api blueprints
app.add_api('swagger/apiserver.yaml', base_path='/1.0/info')
app.add_api('swagger/tenants.yaml', base_path='/1.0/tenants')
app.add_api('swagger/sites.yaml', base_path='/1.0/sites')

# Trick: app.app is the Flask app object inside Connexion app object
flask_app = app.app
flask_app.logger_name = "daspanel_api_server"

# add CORS support
CORS(app.app)

