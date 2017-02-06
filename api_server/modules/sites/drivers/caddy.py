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
        return True, ""

    def deactivate(self, site):
        enfilepath = self.sitesenableddir + '/' + site['_cuid'] + '.conf'
        print('enfilepath: ', enfilepath)
        if self.fs.exists(enfilepath):
            try:
                self.fs.remove(enfilepath)
            except OSError as e:
                if e.errno != errno.ENOENT:
                    print('deactivate OSError: ', e)
                return False, "Filesystem error"
            return True, ""
        else:
            return False, "Site not active"

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
                    return False, "Filesystem error"
            else:
                print("File exist: " + enfilepath)
                return False, "Site already active"
        else:
            print("File not exist: " + avfilepath)
            return False, "Site dont have configuration. Generate it first and after activate it"
        print("Site active")
        return True, ""

    def get_template(self, sitetype, runtime):
        template_obj = None
        template = "{0}-{1}.template".format(sitetype, runtime)
        template_file = "{0}/{1}".format(self.templatesdir, template)
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
                #return False, "{0}".format(template)
        return template_obj

    def generate(self, site):
        tmplresult = ''

        # Get info about current active version of the site
        vindex = -1
        site_versions = site['versions']
        for i, v in enumerate(site_versions):
            if v['_cuid'] == site['active_version']:
                vindex = i
                break
        if vindex == -1:
            return False, "Version not found: {0}".format(site['active_version'])
        active_version = site_versions[vindex]
        print('Generating site using version: ', active_version)

        # Get template for the current active version of the site
        template_obj = self.get_template(active_version['sitetype'], active_version['runtime'])
        if template_obj == None:
            return False, "Template not found for {0} {1}".format(active_version['sitetype'], active_version['runtime'])

        # Generate default conf of the site
        tmplresult = tmplresult + self.generate_subdomain(site=site, template=template_obj)

        # Generate conf for each redirect using default version of the site
        for host in site['redirects']:
            print("Processing host: " + host['hosturl'] + '.' + host['domain'])
            tmplresult = tmplresult + self.generate_redirect(host=host, site=site, template=template_obj)

        # Generate conf for each version of the site
        for version in site['versions']:
            print("Processing version: " + version['description'])
            template_obj = self.get_template(version['sitetype'], version['runtime'])
            if template_obj == None:
                return False, "Template not found for vesion {0}: {1} {2}".format(
                    version['_cuid'], version['sitetype'], version['runtime']
                )

            tmplresult = tmplresult + self.generate_version(version=version, site=site, template=template_obj)

        filepath = self.sitesavailabledir + '/' + site['_cuid'] + '.conf'
        print("Saving site '%s' caddy conf to: %s" % (site['_cuid'], filepath))
        self.fs.write_file(filepath=filepath, contents=tmplresult)
        return True, ""

    def generate_version(self, version, site, template):
        variables = {}
        variables['sitetype'] = site['sitetype']
        variables['domain'] = 'sites.' + CONFIG.daspanel.host
        variables['ssl'] = ''
        variables['sslcert'] = ''
        variables['name'] = '{0}.v.{1}.{2}:80'.format(
            version['_cuid'], site['_cuid'], variables['domain']
        )
        if not site['urlprefix'] == site['_cuid']:
            variables['name'] += ' ' + '{0}.v.{1}.{2}:80'.format(
                version['_cuid'], site['urlprefix'], variables['domain']
            )

        variables['certpath'] = ''
        variables['dir'] = self._params['datadir'] + '/' + version['directory']
        data = template.render(variables)
        return data.decode('utf-8')

    def generate_subdomain(self, site, template):
        variables = {}
        variables['sitetype'] = site['sitetype']
        variables['domain'] = 'sites.' + CONFIG.daspanel.host
        variables['ssl'] = ''
        variables['sslcert'] = ''
        variables['name'] = '{0}.{1}:80'.format(site['_cuid'], variables['domain'])
        if not site['urlprefix'] == site['_cuid']:
            variables['name'] += ' ' + '{0}.{1}:80'.format(site['urlprefix'], variables['domain'])
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

