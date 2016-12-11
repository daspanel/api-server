# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import os
import errno
import shutil

# http://stackoverflow.com/questions/28035685/improper-use-of-new-to-generate-classes

class PluginParams(dict):
    def __init__(self, **params):
        self['tenant'] = None
        self['bucket'] = 'NOBUCKET'
        self['basedir'] = '/opt/daspanel/'
        self['datadir'] = '/opt/daspanel/data'

    def __getattr__(self, item):
        return self[item]


class DasFs(object):
    'Class to manipulate local filesystem'
    name = "DasFs"
    

    def __init__(self, **params):
        self._params  = PluginParams()
        if (len(params)) > 0:
            self._params.update(params['payload'])

        print("self._params.datadir 1 = ", self._params.datadir)
        self._params.datadir = '{0}/{1}/'.format(self._params.datadir, self._params.bucket)
        print("self._params.datadir 2 = ", self._params.datadir)

    def dirname(self, path):
       print('dirname: ', os.path.dirname(path))
       return os.path.dirname(path)

    def exists(self, thefile):
        full_path = '{0}{1}'.format(self._params.datadir, thefile)
        print('exists: ', full_path)
        return os.path.exists(full_path)

    def remove(self, path):
        full_path = '{0}{1}'.format(self._params.datadir, path)
        print('DASFs Remove: ', full_path)
        return os.remove(full_path)

    def copy2(self, source_file, dest_file):
        source = '{0}{1}'.format(self._params.datadir, source_file)
        dest   = '{0}{1}'.format(self._params.datadir, dest_file)
        print('source: ', source)
        print('dest  : ', dest)
        filedir = self.dirname(dest_file) 
        print('copy2 filedir: ', filedir)
        try:
            self.mkdir(filedir)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

        shutil.copy2(source, dest)

        return True

    def exists(self, thefile):
        full_path = '{0}{1}'.format(self._params.datadir, thefile)
        print('exists: ', full_path)
        return os.path.exists(full_path)

    def isfile(self, thefile):
        full_path = '{0}{1}'.format(self._params.datadir, thefile)
        print('isfile: ', full_path)
        return os.path.isfile(full_path)

    def mkdir(self, directory):
        thedir = '{0}{1}'.format(self._params.datadir, directory)
        print('mkdir Creating dir: ', thedir)
        if not os.path.exists(thedir):
            try:
                os.makedirs(thedir)
            except OSError as error:
                if error.errno != errno.EEXIST:
                    raise

    def rmtree(self, directory):
        thedir = '{0}{1}'.format(self._params.datadir, directory)
        print('rmtree dir: ', thedir)
        shutil.rmtree(thedir)

    def cptree(self, orig, dest):
        theorigdir = '{0}{1}'.format(self._params.datadir, orig)
        print('cloning from: ', theorigdir)
        thedestdir = '{0}{1}'.format(self._params.datadir, dest)
        print('cloning to  : ', thedestdir)
        shutil.copytree(theorigdir, thedestdir)

    def write_file(self, filepath, contents):
        full_path = '{0}{1}'.format(self._params.datadir, filepath)
        print("WRITED: ", full_path)
        filedir = os.path.dirname(full_path)  
        try:
            os.makedirs(filedir)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
            
        f = os.open(full_path, os.O_RDWR|os.O_CREAT|os.O_TRUNC)
        os.write(f,contents)
        os.close(f)
        return

def register(module_name, handler_collection):
    handler_collection.add_class(module_name, DasFs)

