# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import sys, os, errno

try:
    from daspanel_fs import DasFs
except:
    from lib.daspanel_fs.fslocal import DasFs

from jinja2 import Environment, FileSystemLoader

class PluginParams(dict):
    def __init__(self, **params):
        self['basedir'] = '/opt/daspanel'
        self['datadir'] = '/opt/daspanel/data'

    def __getattr__(self, item):
        return self[item]

class SitesConf():
    'Class to manipulate NGINX site conf file'
    name = "SitesConf"

    def __init__(self, **params):
        self._params  = PluginParams()
        if (len(params)) > 0:
            self._params.update(params['payload'])

        self._params['datadir'] = "{0}/{1}".format(self._params.datadir, self._params.tenant)
        self.basedir = self._params.basedir
        self.templatesdir = self._params.basedir + '/conf-templates/nginx/etc/nginx/sites-templates'
        self.tenant_templatesdir = self._params.datadir + '/conf-templates/nginx/etc/nginx/sites-templates'
        self.sitesavailabledir = self._params.datadir + '/conf/nginx/etc/nginx/sites-available'
        self.sitesenableddir = self._params.datadir + '/etc/nginx/sites-enabled'
        self.sitesenableddir = self._params.datadir + '/etc/nginx/sites-enabled'
        print("TEMPLATEDIR=", self.templatesdir)
        self.templates = Environment(loader=FileSystemLoader(self.templatesdir))
        self.tenant_templates = Environment(loader=FileSystemLoader(self.tenant_templatesdir))
        self.certspath = self._params.datadir + '/certs'

    def writeFile(self, filepath, contents):
        print("WRITED: ", filepath)
        filedir = os.path.dirname(filepath)  
        try:
            os.makedirs(filedir)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
            
        f = os.open(filepath, os.O_RDWR|os.O_CREAT|os.O_TRUNC)
        os.write(f,contents)
        os.close(f)
        return


    def generate(self, site):
        tmplresult = ''
        template = "{0}-{1}.template".format(site['sitetype'], site['runtime'])
        template_file = "{0}/{1}".format(self.templatesdir, template)
        tenant_template_file = "{0}/{1}".format(self.tenant_templatesdir, template)
        print("TEMPLATE={0}".format(template))
        print("SYSTEM TEMPLATE FILE: {0}".format(template_file))
        print("TENANT TEMPLATE FILE: {0}".format(tenant_template_file))

        #https://github.com/veselosky/jinja2_s3loader

        if (os.path.isfile(tenant_template_file)):
            template_obj = self.tenant_templates.get_template(template)
            print("USING TENANT TEMPLATE")
        else:
            if (os.path.isfile(template_file)):
                template_obj = self.templates.get_template(template)
                print("USING SYSTEM TEMPLATE")
            else:
                print("Error1: template not found: {0} or {1}".format(template_file, tenant_template_file))
                return False

        for host in site['redirects']:
            print("Processing host: " + host['hosturl'] + '.' + host['domain'])
            tmplresult = tmplresult + self.generate_redirect(host=host, site=site, template=template_obj)
        filepath = self.sitesavailabledir + '/' + site['_cuid'] + '.conf'
        print("Saving domain '%s' nginx conf to: %s" % (host['domain'], filepath))
        self.writeFile(filepath=filepath, contents=tmplresult)
        return True

    def generate_redirect(self, host, site, template):
        variables = {}
        variables['sitetype'] = site['sitetype']
        variables['domain'] = host['domain']
        variables['ssl'] = host['ssl']
        variables['sslcert'] = host['sslcert']
        variables['name'] = host['hosturl'] + '.' + host['domain'] + ':80' + ' ' + host['hosturl'] + '.' + host['domain'] + ':443'
        if host['hosturl'] == 'www':
            variables['name'] += ' ' + host['domain'] + ':80' + ' ' + host['domain'] + ':443'
        if host['ssl'] == 'No':
            variables['certpath'] = self.certspath        
        else:
            variables['certpath'] = self.certspath + '/' + host['hosturl'] + '.' + host['domain']
        variables['dir'] = self._params['datadir'] + '/' + site['active_dir']
        data = template.render(variables)
        return data.decode('utf-8')


def register(module_name, handler_collection):
    handler_collection.add_class(module_name, SitesConf)

