import os
import errno
import shutil

# http://stackoverflow.com/questions/28035685/improper-use-of-new-to-generate-classes

class DasFs(object):
    def __init__(self, service='local', tenant='', bucket=''):
        self.service = service
        self.tenant = tenant
        self.bucket = bucket

    def mkdir(self, directory):
        thedir = '/opt/daspanel/data/{0}/{1}'.format(self.bucket, directory)
        if not os.path.exists(thedir):
            try:
                os.makedirs(thedir)
            except OSError as error:
                if error.errno != errno.EEXIST:
                    raise

    def rmtree(self, directory):
        thedir = '/opt/daspanel/data/{0}/{1}'.format(self.bucket, directory)
        shutil.rmtree(thedir)

    def cptree(self, orig, dest):
        theorigdir = '/opt/daspanel/data/{0}/{1}'.format(self.bucket, orig)
        thedestdir = '/opt/daspanel/data/{0}/{1}'.format(self.bucket, dest)
        shutil.copytree(theorigdir, thedestdir)


