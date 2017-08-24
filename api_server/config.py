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
daspanel.hostname = os.getenv('DASPANEL_SYS_HOSTNAME', 'daspanel.site')
daspanel.cfg_version = '0.1.0'
daspanel.def_cfg = {}
daspanel.def_cfg['sys'] = {}
daspanel.def_cfg['sys']['hostname'] = daspanel.hostname
daspanel.def_cfg['sys']['host'] = daspanel.hostname
daspanel.def_cfg['sys']['config_version'] = '0.1.0'
daspanel.def_cfg['sys']['apiserver'] = os.getenv('DASPANEL_SYS_APISERVER', 'http://daspanel-api:8080/1.0')
daspanel.def_cfg['sys']['admin'] = os.getenv('DASPANEL_SYS_ADMIN', 'admin@{0}'.format(daspanel.hostname))
daspanel.def_cfg['sys']['password'] = os.getenv('DASPANEL_SYS_PASSWORD', gen_pass())
daspanel.def_cfg['sys']['msghub'] = os.getenv('DASPANEL_SYS_MSGHUB', 'mail-catcher')
daspanel.def_cfg['sys']['debug'] = os.getenv('DASPANEL_SYS_DEBUG', False)
daspanel.def_cfg['smtp'] = {}
daspanel.def_cfg['smtp']['type'] = 'mail-catcher'
daspanel.def_cfg['smtp']['server'] = 'daspanel-mail-catcher:1025'
daspanel.def_cfg['smtp']['user'] = daspanel.def_cfg['sys']['admin']
daspanel.def_cfg['smtp']['password'] = os.getenv('DASPANEL_SYS_UUID')
daspanel.def_cfg['redis'] = {}
daspanel.def_cfg['redis']['server'] = 'daspanel-redis'
daspanel.def_cfg['redis']['port'] = 6379
daspanel.def_cfg['redis']['database'] = 0
daspanel.def_cfg['redis']['user'] = ''
daspanel.def_cfg['redis']['password'] = gen_pass()
daspanel.def_cfg['s3'] = {}
daspanel.def_cfg['s3']['browser_url'] = 'https://s3.svc.{0}'.format(daspanel.hostname)
daspanel.def_cfg['s3']['endpoint'] = 'https://s3.svc.{0}'.format(daspanel.hostname)
daspanel.def_cfg['s3']['region'] = 'us-east-1'
daspanel.def_cfg['s3']['access_key'] = os.getenv('DASPANEL_SYS_UUID')[0:20]
daspanel.def_cfg['s3']['secret_key'] = gen_pass()
daspanel.def_cfg['mysql'] = {}
daspanel.def_cfg['mysql']['server'] = 'daspanel-mysql'
daspanel.def_cfg['mysql']['port'] = 3306
daspanel.def_cfg['mysql']['user'] = os.getenv('DASPANEL_SYS_UUID')
daspanel.def_cfg['mysql']['password'] = gen_pass()
daspanel.def_cfg['engines'] = []
daspanel.def_cfg['engines'].extend([
    {'_cuid': 'cj5h6dqar0000325kybi7t8up', 'provider': 'DOCKER', 'runtime': 'php71', 'description': 'PHP 7.1', 'sitetypes': [
        {'_cuid': '', 'sitetype': 'generic', 'description': 'Generic site - PHP71'},
        {'_cuid': '', 'sitetype': 'grav', 'description': 'Grav flat-file CMS'},
        {'_cuid': '', 'sitetype': 'wordpress', 'description': 'Wordpress 4.X'},
        {'_cuid': '', 'sitetype': 'cakephp2x', 'description': 'CakePHP 2.X'},
        {'_cuid': '', 'sitetype': 'nextcloud12x', 'description': 'Nextcloud 12.X'}
    ]},
    {'_cuid': 'cj5h6e0490000325kdnaltrcy', 'provider': 'DOCKER', 'runtime': 'php70', 'description': 'PHP 7.0', 'sitetypes': [
        {'_cuid': '', 'sitetype': 'generic', 'description': 'Generic site - PHP70'},
        {'_cuid': '', 'sitetype': 'grav', 'description': 'Grav flat-file CMS'},
        {'_cuid': '', 'sitetype': 'wordpress', 'description': 'Wordpress 4.X'},
        {'_cuid': '', 'sitetype': 'cakephp2x', 'description': 'CakePHP 2.X'},
        {'_cuid': '', 'sitetype': 'nextcloud12x', 'description': 'Nextcloud 12.X'}
    ]},
    {'_cuid': 'cj5h6e68y0000325kq5k643q4', 'provider': 'DOCKER', 'runtime': 'php56', 'description': 'PHP 5.6', 'sitetypes': [
        {'_cuid': '', 'sitetype': 'generic', 'description': 'Generic site - PHP56'},
        {'_cuid': '', 'sitetype': 'grav', 'description': 'Grav flat-file CMS'},
        {'_cuid': '', 'sitetype': 'wordpress', 'description': 'Wordpress 4.X'},
        {'_cuid': '', 'sitetype': 'cakephp2x', 'description': 'CakePHP 2.X'},
        {'_cuid': '', 'sitetype': 'nextcloud12x', 'description': 'Nextcloud 12.X'}
    ]},
    {'_cuid': 'cj5h6eczq0000325kx0i6534o', 'provider': 'DOCKER', 'runtime': 'static', 'description': 'Static', 'sitetypes': [
        {'_cuid': '', 'sitetype': 'generic', 'description': 'Generic site - Static'}
    ]}
])
daspanel.def_cfg['filemanager'] = {}
daspanel.def_cfg['filemanager']['user'] = daspanel.def_cfg['sys']['admin']
daspanel.def_cfg['filemanager']['password'] = gen_pass()

# Loads existing tenant config or create a new one if missing
config_file = '/opt/daspanel/data/{0}/db/{0}.json'.format(os.getenv('DASPANEL_SYS_UUID'))
if os.path.exists(config_file):
    with open(config_file, 'r') as fp:
        #tenant_cfg = json.load(fp)
        daspanel.def_cfg.update(json.load(fp))
    # If hostname has changed
    if (not daspanel.def_cfg['sys']['hostname'] == daspanel.hostname):
        daspanel.def_cfg['sys']['hostname'] = daspanel.hostname
        daspanel.def_cfg['sys']['host'] = daspanel.hostname
        with open(config_file, 'w') as fp:
            json.dump(daspanel.def_cfg, fp, ensure_ascii=False)

else:
    with open(config_file, 'w') as fp:
        json.dump(daspanel.def_cfg, fp, ensure_ascii=False)


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
pubsub.cfg = {}
pubsub.cfg['redis'] = daspanel.def_cfg['redis']

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


