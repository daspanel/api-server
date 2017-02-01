# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import sys, os, errno

try:
    from daspanel_fs import DasFs
except:
    from lib.daspanel_fs.fslocal import DasFs

from jinja2 import Environment, FileSystemLoader

import config as CONFIG

class PluginParams(dict):
    def __init__(self, **params):
        self['basedir'] = '/opt/daspanel'
        self['datadir'] = '/opt/daspanel/data'

    def __getattr__(self, item):
        return self[item]

class SitesConf():
    'Class to manipulate CaddyServer site conf file'
    name = "SitesConf"

    def __init__(self, **params):
        self._params  = PluginParams()
        if (len(params)) > 0:
            self._params.update(params['payload'])

        # Filesystem layer
        self.fs = CONFIG.fs.drivers.get_instance('local', 'DasFs', tenant=self._params['tenant'], bucket=self._params['bucket'])

        # Imutable data
        self.basedir = self.fs._params.basedir
        self.templatesdir = self.fs._params.basedir + '/conf-templates/caddy/etc/caddy/sites-templates'
        self.templates = Environment(loader=FileSystemLoader(self.templatesdir))

        # Tenant data
        self._params['datadir'] = self.fs._params.datadir
        self.tenant_templatesdir = self._params.datadir + '/conf-templates/caddy/etc/caddy/sites-templates'
        self.tenant_templates = Environment(loader=FileSystemLoader(self.tenant_templatesdir))
        self.certspath = self._params.datadir + '/certs'

        # Relative paths where to save data
        self.sitesavailabledir = '/conf/caddy/etc/caddy/sites-available'
        self.sitesenableddir = '/conf/caddy/etc/caddy/sites-enabled'

        print("TEMPLATEDIR=", self.templatesdir)

    def reload(self):
        '''Force reload of configuration files using inotify.'''
        filepath = self.sitesenableddir + '/FORCERELOAD'
        self.fs.write_file(filepath=filepath, contents='1')
        return True

    def deactivate(self, site):
        enfilepath = self.sitesenableddir + '/' + site['_cuid'] + '.conf'
        print('enfilepath: ', enfilepath)
        if self.fs.exists(enfilepath):
            try:
                self.fs.remove(enfilepath)
            except OSError as e:
                if e.errno != errno.ENOENT:
                    print('deactivate OSError: ', e)
                raise
            return True
        else:
            return False

    def activate(self, site):
        filepath = self.sitesavailabledir + '/' + site['_cuid'] + '.conf'
        avfilepath = self.sitesavailabledir + '/' + site['_cuid'] + '.conf'
        print('avfilepath: ', avfilepath)
        enfilepath = self.sitesenableddir + '/' + site['_cuid'] + '.conf'
        print('enfilepath: ', enfilepath)
        if self.fs.isfile(avfilepath):
            if not self.fs.exists(enfilepath):
                try:
                    #os.symlink(avfilepath, enfilepath)
                    self.fs.copy2(avfilepath, enfilepath)
                except Exception as e:
                    print(e)
                    return False
            else:
                print("File exist: " + enfilepath)
                return False
        else:
            print("File not exist: " + avfilepath)
            return False
        print("Site active")
        return True


    def generate(self, site):
        tmplresult = ''
        template = "{0}-{1}.template".format(site['sitetype'], site['runtime'])
        template_file = "{0}/{1}".format(self.templatesdir, template)
        #tenant_template_file = "{0}/{1}".format(self.tenant_templatesdir, template)
        tenant_template_file = "/conf-templates/caddy/etc/caddy/sites-templates/{0}".format(template)
        print("TEMPLATE={0}".format(template))
        print("SYSTEM TEMPLATE FILE: {0}".format(template_file))
        print("TENANT TEMPLATE FILE: {0}{1}".format(self.tenant_templatesdir, template))

        #https://github.com/veselosky/jinja2_s3loader

        if (self.fs.isfile(tenant_template_file)):
            template_obj = self.tenant_templates.get_template(template)
            print("USING TENANT TEMPLATE")
        else:
            if (os.path.isfile(template_file)):
                template_obj = self.templates.get_template(template)
                print("USING SYSTEM TEMPLATE")
            else:
                print("Error1: template not found: {0} or {1}".format(template_file, tenant_template_file))
                return False, "{0}".format(template)

        for host in site['redirects']:
            print("Processing host: " + host['hosturl'] + '.' + host['domain'])
            tmplresult = tmplresult + self.generate_redirect(host=host, site=site, template=template_obj)

        # Generate default dir of the site
        tmplresult = tmplresult + self.generate_subdomain(site=site, template=template_obj)

        filepath = self.sitesavailabledir + '/' + site['_cuid'] + '.conf'
        print("Saving site '%s' caddy conf to: %s" % (site['_cuid'], filepath))
        self.fs.write_file(filepath=filepath, contents=tmplresult)
        return True, ""

    def generate_subdomain(self, site, template):
        variables = {}
        variables['sitetype'] = site['sitetype']
        variables['domain'] = 'sites.' + CONFIG.daspanel.host
        variables['ssl'] = ''
        variables['sslcert'] = ''
        variables['name'] = '{0}.{1}:80'.format(site['_cuid'], variables['domain'])
        variables['certpath'] = ''        
        variables['dir'] = self._params['datadir'] + '/' + site['active_dir']
        data = template.render(variables)
        return data.decode('utf-8')

    def generate_redirect(self, host, site, template):
        print(host)
        variables = {}
        variables['sitetype'] = site['sitetype']
        variables['domain'] = host['domain']
        variables['ssl'] = host['ssl']
        variables['sslcert'] = host['sslcert']
        variables['name'] = host['hosturl'] + '.' + host['domain'] + ':80' + ' ' + host['hosturl'] + '.' + host['domain'] + ':443'
        if host['hosturl'] == 'www':
            variables['name'] += ' ' + host['domain'] + ':80' + ' ' + host['domain'] + ':443'
        if not host['ssl']:
            variables['certpath'] = self.certspath        
        else:
            variables['certpath'] = self.certspath + '/' + host['hosturl'] + '.' + host['domain']
        variables['dir'] = self._params['datadir'] + '/' + site['active_dir']
        data = template.render(variables)
        return data.decode('utf-8')


def register(module_name, handler_collection):
    handler_collection.add_class(module_name, SitesConf)

