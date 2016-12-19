# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import os
import errno
import shutil
import zipfile
from distutils.dir_util import copy_tree

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

    def copy_tree(self, orig, dest):
        theorigdir = '{0}{1}'.format(self._params.datadir, orig)
        print('copying from: ', theorigdir)
        thedestdir = '{0}{1}'.format(self._params.datadir, dest)
        print('copying to  : ', thedestdir)
        copy_tree(theorigdir, thedestdir)

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

    def open(self, filepath, mode):
        full_path = '{0}{1}'.format(self._params.datadir, filepath)
        print("FS.OPEN: ", full_path)
        return open(full_path, mode)

    def is_zip(self, filepath):
        full_path = '{0}{1}'.format(self._params.datadir, filepath)
        print("FS.IS_ZIP: ", full_path)
        return zipfile.is_zipfile(full_path)

    def extract_zip(self, filepath, todir):
        file_full_path = '{0}{1}'.format(self._params.datadir, filepath)
        dir_full_path = '{0}{1}'.format(self._params.datadir, todir)
        print("FS.IS_ZIP: ", file_full_path, dir_full_path)
        zipfile.ZipFile(file_full_path, "r").extractall(dir_full_path)

    def zip_index_exist(self, filepath):
        result = False
        full_path = '{0}{1}'.format(self._params.datadir, filepath)
        print("FS.ZIP_HAVEINDEX: ", full_path)
        with zipfile.ZipFile(full_path, "r") as z:
            for zfile in z.namelist():
                zfile = os.path.split(zfile)
                if zfile[1] == 'index.html' or zfile[1] == 'index.php':
                    print(zfile)
                    result = True
                    break
        return result

    def site_root(self, dir):
        index_dir = None
        dir_full_path = '{0}{1}'.format(self._params.datadir, dir)
        print("FS.SITE_ROOT: ", dir_full_path)
        for root, dirs, files in os.walk(dir_full_path):
            if 'index.html' in files or 'index.php' in files:
                index_dir = root.replace(self._params.datadir, '')
                break
        return index_dir

def register(module_name, handler_collection):
    handler_collection.add_class(module_name, DasFs)

