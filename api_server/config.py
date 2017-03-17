# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import os

try:
    from daspanel_plugin import PluginCollection
except:
    from lib.daspanel_plugin import PluginCollection

class ConfigSection(object):

    def __init__(self, *args):
        self.__header__ = str(args[0]) if args else None

    def __repr__(self):
        if self.__header__ is None:
             return super(Struct, self).__repr__()
        return self.__header__

    def next(self):
        """ Fake iteration functionality.
        """
        raise StopIteration

    def __iter__(self):
        """ Fake iteration functionality.
        We skip magic attribues and Structs, and return the rest.
        """
        ks = self.__dict__.keys()
        for k in ks:
            if not k.startswith('__') and not isinstance(k, Struct):
                yield getattr(self, k)

    def __len__(self):
        """ Don't count magic attributes or Structs.
        """
        ks = self.__dict__.keys()
        return len([k for k in ks if not k.startswith('__')\
                    and not isinstance(k, Struct)])


daspanel = ConfigSection("DASPANEL config")
daspanel.host = os.getenv('DASPANEL_SYS_HOSTNAME', 'daspanel.site')

mysql = ConfigSection("MySQL specific configuration")
mysql.user = 'root'
mysql.pwd = 'secret'
mysql.host = 'localhost'
mysql.port = 3306
mysql.database = 'mydb'
print("Loading config: ", mysql)

sites = ConfigSection("Sites module drivers")
print("Loading config: ", sites)
sites.drivers = PluginCollection(plugin_source='modules.sites.drivers', alt_pkg='daspanel_http_service_')
drivers = 'nginx caddy'
drvlist = drivers.split()

for drv in drvlist:
    if (not sites.drivers.load(name=drv)):
        raise ValueError("Can not load driver in sites serice api: {0}".format(drv))


api = ConfigSection("API config")
api.error_types = 'https://daspanel.com/docs/api/errors/types'

fs = ConfigSection("File System")
fs.drivers = PluginCollection(plugin_source='lib.daspanel_fs.drivers', alt_pkg='daspanel_fs_drivers_')
drivers = 'local'
drvlist = drivers.split()
for drv in drvlist:
    if (not fs.drivers.load(name=drv)):
        raise ValueError("Can not load filesystem driver API: {0}".format(drv))
fs.active = 'local'


