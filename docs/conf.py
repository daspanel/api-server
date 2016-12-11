# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os

from sphinx_celery import conf

globals().update(conf.build_config(
    'api_server', __file__,
    project='api_server',
    # version_dev='2.0',
    # version_stable='1.4',
    canonical_url='http://api_server.readthedocs.org',
    webdomain='',
    github_project='admindaspanel/api_server',
    copyright='2016',
    html_logo='images/logo.png',
    html_favicon='images/favicon.ico',
    html_prepend_sidebars=[],
    include_intersphinx={'python', 'sphinx'},
    # django_settings='testproj.settings',
    # path_additions=[os.path.join(os.pardir, 'testproj')],
    # apicheck_ignore_modules=[
    #   'api_server',
    # ],
))

settings = {}
ignored_settings = {
    # Deprecated broker settings (replaced by broker_url)
    'broker_host',
}

def configcheck_project_settings():
    #from celery.app.defaults import NAMESPACES, flatten
    #settings.update(dict(flatten(NAMESPACES)))
    return set(settings)

def is_deprecated_setting(setting):
    try:
        return settings[setting].deprecate_by
    except KeyError:
        pass

def configcheck_should_ignore(setting):
    return setting in ignored_settings or is_deprecated_setting(setting)

