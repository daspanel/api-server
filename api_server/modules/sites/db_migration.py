# -*- coding: utf-8 -*-
"""sites db migration."""
from __future__ import absolute_import, unicode_literals, division, print_function
from distutils.version import StrictVersion
import os, logging, random, string, json, copy, collections

logger = logging.getLogger(__name__)

# Module imports
from .models.tinyj import DASPANEL_DATABASESFILE, SITES_DB, SITES_DB_FMT, SiteVersion, SiteRedirects, SiteModel
from .errors import SITES_ERRORS

logger.info("MIGRATING DB: {0}".format(DASPANEL_DATABASESFILE))

def to_011(site):
    prev_version = "0.1.0"
    curr_version = "0.1.1"
    try:
        if StrictVersion(site._fmt_version) < StrictVersion(prev_version):
            site._fmt_version = curr_version
            site.save()
        else:
            if StrictVersion(site._fmt_version) < StrictVersion(prev_version):
                return "Failed step: {0} because record version {1} is < {2}".format(curr_version, site._fmt_version, prev_version)
            else:
                logger.info("Ignoring step: {0}".format(curr_version))
    except Exception as e:
        logger.exception("Migration failed in step {0}: {1}".format(curr_version, str(e)))
        return "ERROR: {0}".format(str(e))
    return "OK"

def to_012(site):
    prev_version = "0.1.1"
    curr_version = "0.1.2"
    try:
        if StrictVersion(site._fmt_version) == StrictVersion(prev_version):
            for rec in site.versions:
                rec.root_dir = "/"
            site._fmt_version = curr_version
            site.save()
        else:
            if StrictVersion(site._fmt_version) < StrictVersion(prev_version):
                return "Failed step: {0} because record version {1} is < {2}".format(curr_version, site._fmt_version, prev_version)
            else:
                logger.info("Ignoring step: {0}".format(curr_version))
    except Exception as e:
        logger.exception("Migration failed in step {0}: {1}".format(curr_version, str(e)))
        return "ERROR: {0}".format(str(e))
    return "OK"

def to_013(site):
    prev_version = "0.1.2"
    curr_version = "0.1.3"
    try:
        if StrictVersion(site._fmt_version) == StrictVersion(prev_version):
            pass
            #site._fmt_version = curr_version
            #site.save()
        else:
            if StrictVersion(site._fmt_version) < StrictVersion(prev_version):
                return "Failed step: {0} because record version {1} is < {2}".format(curr_version, site._fmt_version, prev_version)
            else:
                logger.info("Ignoring step: {0}".format(curr_version))
    except Exception as e:
        logger.exception("Migration failed in step {0}: {1}".format(curr_version, str(e)))
        return "ERROR: {0}".format(str(e))
    return "OK"

class SitesDbMigrate(object):
    def __init__(self, to_version="0.1.0"):
        self.to_version = to_version
        self.steps = collections.OrderedDict()
        self.steps["0.1.1"] = to_011
        self.steps["0.1.2"] = to_012
        self.steps["0.1.3"] = to_013
        self.steps_done = collections.OrderedDict()

    def migrate(self):
        try:
            allrec = SiteModel.all()
            for rec in allrec:
                logger.info("\n=== BOF migrating database of site : {0} ===".format(rec._cuid))
                for version, f in self.steps.items():
                    if StrictVersion(version) <= StrictVersion(self.to_version):
                        logger.info("Migration step: {0}".format(version))
                        self.steps_done[version] = f(rec)
                        if not self.steps_done[version] == "OK":
                            raise Exception(self.steps_done[version])
                logger.info("=== EOF migrating database of site : {0} ===\n".format(rec._cuid))
            return True
        except Exception as e:
            #https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
            #logger.error("Failed to open file", exc_info=True)
            logger.exception("Migration failed in step: {0}".format(str(e)))
            return False
