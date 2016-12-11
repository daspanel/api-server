#!/usr/bin/env python
from __future__ import absolute_import, division, print_function
import os
import connexion
import datetime
import logging

from raven.contrib.flask import Sentry

import config as CONFIG

logging.basicConfig(level=logging.INFO)

app = connexion.App(__name__)

app.add_api('swagger/apiserver.yaml')
#app.add_api('swagger/databases.yaml', base_path='/1.0/databases')
#app.add_api('swagger/domains.yaml', base_path='/1.0/domains')
app.add_api('swagger/sites.yaml', base_path='/1.0/sites')


# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app

# app.app is the Flask app object
application = app.app
sentry = Sentry(application, dsn='https://90ba14f0f5f947369379a2eb2e63391e:6c32e551d4104dd99287e16200218d24@sentry.io/98530')

if __name__ == '__main__':

    # run our standalone gevent server
    app.run(host='0.0.0.0', port=8080)
