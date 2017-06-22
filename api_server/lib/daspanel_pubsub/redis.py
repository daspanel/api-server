# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
from redis import Redis

# http://stackoverflow.com/questions/28035685/improper-use-of-new-to-generate-classes

class PluginParams(dict):
    def __init__(self, **params):
        self['tenant'] = None
        self['host'] = 'daspanel-redis'
        self['db'] = 0
        self['port'] = 6379
        self['password'] = self['tenant']

    def __getattr__(self, item):
        return self[item]


class DasPubSub(object):
    'Class to PubSub messages'
    name = "DasPubSub"
    
    def __init__(self, **params):
        self._params  = PluginParams()
        if (len(params)) > 0:
            self._params.update(params['payload'])

        # Redis connection
        self.conn = Redis(
            host=self._params.host, 
            port=self._params.port, 
            db=self._params.db, 
            password=self._params.password
        )

    def publish(self, channel, message):
       return self.conn.publish(channel, message)

def register(module_name, handler_collection):
    handler_collection.add_class(module_name, DasPubSub)

