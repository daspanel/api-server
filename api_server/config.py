# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import os, random, string, json

try:
    from daspanel_plugin import PluginCollection
except:
    from lib.daspanel_plugin import PluginCollection

def gen_pass(ucase=5, lcase=5, digits=6, schars=0):
    password = ''
    for i in range(int(ucase)):
        password += string.uppercase[random.randint(0,len(string.uppercase)-1)]
    for i in range(int(lcase)):
        password += string.lowercase[random.randint(0,len(string.lowercase)-1)]
    for i in range(int(digits)):
        password += string.digits[random.randint(0,len(string.digits)-1)]
    for i in range(int(schars)):
        password += string.punctuation[random.randint(0,len(string.punctuation)-1)]

    return ''.join(random.sample(password,len(password)))

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
daspanel.cfg_version = '0.1.0'
daspanel.def_cfg = {}
daspanel.def_cfg['sys'] = {}
daspanel.def_cfg['sys']['hostname'] = os.getenv('DASPANEL_SYS_HOSTNAME', 'daspanel.site')
daspanel.def_cfg['sys']['apiserver'] = os.getenv('DASPANEL_SYS_HOSTNAME', 'http://daspanel-api:8080/1.0')
daspanel.def_cfg['sys']['admin'] = os.getenv('DASPANEL_SYS_ADMIN', 'admin@{0}'.format(daspanel.def_cfg['sys']['hostname']))
daspanel.def_cfg['sys']['password'] = os.getenv('DASPANEL_SYS_PASSWORD', gen_pass())
daspanel.def_cfg['sys']['msghub'] = os.getenv('DASPANEL_SYS_MSGHUB', 'mail-catcher')
daspanel.def_cfg['sys']['debug'] = os.getenv('DASPANEL_SYS_DEBUG', False)
daspanel.def_cfg['smtp'] = {}
daspanel.def_cfg['smtp']['type'] = 'mail-catcher'
daspanel.def_cfg['smtp']['server'] = 'daspanel-mail-catcher:1025'
daspanel.def_cfg['smtp']['user'] = daspanel.def_cfg['sys']['admin']
daspanel.def_cfg['smtp']['password'] = os.getenv('DASPANEL_SYS_UUID', gen_pass())
daspanel.def_cfg['redis'] = {}
daspanel.def_cfg['redis']['server'] = 'daspanel-redis'
daspanel.def_cfg['redis']['port'] = 6379
daspanel.def_cfg['redis']['database'] = 0
daspanel.def_cfg['redis']['user'] = ''
daspanel.def_cfg['redis']['password'] = os.getenv('DASPANEL_SYS_UUID', gen_pass())

# MySql
mysql = ConfigSection("MySQL specific configuration")
mysql.user = 'root'
mysql.pwd = 'secret'
mysql.host = 'localhost'
mysql.port = 3306
mysql.database = 'mydb'
print("Loading MySql config: ", mysql)

# Redis
redis = ConfigSection("Redis configuration")
redis.host = 'daspanel-redis'
redis.port = 6379
redis.db = '0'
redis.password = None
print("Loading Redis config: ", redis)

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

# Filesystem drivers
fs = ConfigSection("File System")
fs.drivers = PluginCollection(plugin_source='lib.daspanel_fs.drivers', alt_pkg='daspanel_fs_drivers_')
drivers = 'local'
drvlist = drivers.split()
for drv in drvlist:
    if (not fs.drivers.load(name=drv)):
        raise ValueError("Can not load filesystem driver API: {0}".format(drv))
fs.active = 'local'

# PubSub drivers
pubsub = ConfigSection("PubSub drivers")
print("Loading config: ", pubsub)
pubsub.drivers = PluginCollection(plugin_source='lib.daspanel_pubsub', alt_pkg='daspanel_pubsub_drivers_')
drivers = 'redis'
drvlist = drivers.split()
for drv in drvlist:
    if (not pubsub.drivers.load(name=drv)):
        raise ValueError("Can not load pubsub driver: {0}".format(drv))
pubsub.active = 'redis'

# Tenant drivers
tenant = ConfigSection("Tenant drivers")
print("Loading config: ", tenant)
tenant.drivers = PluginCollection(plugin_source='modules.tenants.drivers', alt_pkg='daspanel_tenant_drivers_')
drivers = 'standalone'
drvlist = drivers.split()
for drv in drvlist:
    if (not tenant.drivers.load(name=drv)):
        raise ValueError("Can not load tenant driver: {0}".format(drv))
tenant.active = 'standalone'


