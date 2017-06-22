# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import os

# http://stackoverflow.com/questions/28035685/improper-use-of-new-to-generate-classes

class PluginParams(dict):
    def __init__(self, **params):
        self['tenant'] = 'none'
        self['bucket'] = '/opt/daspanel/data/tenant'

    def __getattr__(self, item):
        return self[item]


class DasTenant(object):
    'Class for Tenant system'
    name = "DasTenant"
    
    def __init__(self, **params):
        self._params  = PluginParams()
        if (len(params)) > 0:
            self._params.update(params['payload'])
        self._params.cfgfile = '{0}/{1}.json'.format(self._params.bucket, self._params.tenant)
        print('DasTenant __init__', self._params)

    def auth(self, key):
        if not self.key == os.environ['DASPANEL_SYS_UUID']:
            return False
        return True


def register(module_name, handler_collection):
    handler_collection.add_class(module_name, DasTenant)

