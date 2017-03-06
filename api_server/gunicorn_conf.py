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
import multiprocessing

# to tune see http://gunicorn-docs.readthedocs.org/en/latest/settings.html
# to run: /usr/bin/gunicorn -c /opt/daspanel/apiserver/gunicorn_conf.py api-connexion:app

DEF_GUNICORN_CFG = {}

# to serve directly via TCP:
DEF_GUNICORN_CFG['bind'] = "0.0.0.0:5000"
DEF_GUNICORN_CFG['backlog'] = "1024"

# for nginx or other proxy:
#bind = "unix:/app/run/gunicorn.sock"

#DEF_GUNICORN_CFG['workers'] = multiprocessing.cpu_count() * 2 + 1
DEF_GUNICORN_CFG['workers'] = 1

# should save some memory, must be = False if reload = True:
DEF_GUNICORN_CFG['preload_app'] = True

DEF_GUNICORN_CFG['worker_class'] = 'sync'

# only relevant for async workers:
DEF_GUNICORN_CFG['worker_connections'] = 50

# set this if workers appear to leak memory or have some other longer-lived
# problem. Then they'll automatically restart after they've serviced this many
# requests:
DEF_GUNICORN_CFG['max_requests'] = 512

# App name
DEF_GUNICORN_CFG['proc_name'] = 'api_server'

# User and group - let's this to be set by env variables
DEF_GUNICORN_CFG['user'] = 'daspanel'
DEF_GUNICORN_CFG['group'] = 'daspanel'

DEF_GUNICORN_CFG['chdir'] = '.'

# logging:
DEF_GUNICORN_CFG['logconfig'] = 'gunicorn_logging.conf'
DEF_GUNICORN_CFG['accesslog'] = '-'
DEF_GUNICORN_CFG['errorlog']  = '-'
DEF_GUNICORN_CFG['loglevel'] = 'info'

# where to store the PID file:
DEF_GUNICORN_CFG['pidfile'] = '/var/run/api_server.pid'

# Defaults is 360.  This is how long the master will wait to hear from a worker
# before killing it.  Can set higher if there are some longer running requests:
DEF_GUNICORN_CFG['timeout'] = 360

# only use True for development:
DEF_GUNICORN_CFG['reload'] = False

# for performance:
DEF_GUNICORN_CFG['keepalive'] = 3

