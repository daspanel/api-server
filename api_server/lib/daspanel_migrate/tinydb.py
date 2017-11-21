# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division, print_function
from distutils.version import StrictVersion
import os
import logging
import random
import string
import json
import copy
import collections

def to_011(cfg_data):
    tmp_data = copy.deepcopy(cfg_data)
    tmp_data["sys"]["config_version"] = "0.1.1"
    for item in tmp_data["engines"]:
        if item["runtime"] == "php56":
            item["sitetypes"].extend([
                {"_cuid": "", "sitetype": "laravel5x", "description": "Laravel 5.X"},
                {"_cuid": "", "sitetype": "codeigniter3x", "description": "CodeIgniter 3.X"}
            ])
    return tmp_data

def to_012(cfg_data):
    tmp_data = copy.deepcopy(cfg_data)
    tmp_data["sys"]["config_version"] = "0.1.2"
    for item in tmp_data["engines"]:
        if item["runtime"] == "php71":
            item["sitetypes"].extend([
                {"_cuid": "", "sitetype": "laravel5x", "description": "Laravel 5.X"},
                {"_cuid": "", "sitetype": "codeigniter3x", "description": "CodeIgniter 3.X"}
            ])
    return tmp_data

def to_013(cfg_data):
    tmp_data = copy.deepcopy(cfg_data)
    tmp_data['sys']['config_version'] = '0.1.3'
    rt_list = ['php56', 'php70', 'php71']
    for item in tmp_data['engines']:
        if item['runtime'] in rt_list:
            item['sitetypes'].extend([{'_cuid': '','sitetype': 'symfony','description': 'Symfony Framework'}])

    return tmp_data


def to_014(cfg_data):
    tmp_data = copy.deepcopy(cfg_data)
    tmp_data['sys']['config_version'] = '0.1.4'
    for item in tmp_data['engines']:
        for rec in item['sitetypes']:
            rec['root_dir'] = '/'

    return tmp_data


def to_015(cfg_data):
    tmp_data = copy.deepcopy(cfg_data)
    tmp_data['sys']['config_version'] = '0.1.5'
    rt_list = ['php70']
    for item in tmp_data['engines']:
        if item['runtime'] in rt_list:
            item['sitetypes'].extend([{'_cuid': '','sitetype': 'laravel5x','description': 'Laravel 5.X','root_dir': '/public'}, {'_cuid': '','sitetype': 'codeigniter3x','description': 'CodeIgniter 3.X','root_dir': '/'}])

    return tmp_data


def to_016(cfg_data):
    tmp_data = copy.deepcopy(cfg_data)
    tmp_data['sys']['config_version'] = '0.1.6'
    for item in tmp_data['engines']:
        for rec in item['sitetypes']:
            if rec['sitetype'] == 'laravel5x':
                rec['root_dir'] = '/public'
            elif rec['sitetype'] == 'cakephp2x':
                rec['root_dir'] = '/app/webroot'
            elif rec['sitetype'] == 'symfony':
                rec['root_dir'] = '/web'

    return tmp_data

class TinyDbMigrate(object):

    def __init__(self, from_version='0.1.0', to_version='0.1.0', cfg_data={}):
        self.logger = logging.getLogger(__name__)
        self.from_version = from_version
        self.to_version = to_version
        self.from_data = copy.deepcopy(cfg_data)
        self.to_data = copy.deepcopy(cfg_data)
        self.steps = collections.OrderedDict()
        self.steps['0.1.2'] = to_012
        self.steps['0.1.3'] = to_013
        self.steps['0.1.4'] = to_014
        self.steps['0.1.5'] = to_015
        self.steps['0.1.6'] = to_016
        self.steps_done = collections.OrderedDict()

    def migrate(self):
        try:
            for version, f in self.steps.items():
                if StrictVersion(version) > StrictVersion(self.from_version):
                    if StrictVersion(version) <= StrictVersion(self.to_version):
                        self.logger.info("Executing migration step: {0}".format(version))
                        self.to_data = f(self.to_data)
                        self.steps_done[version] = "OK"
            return True
        except Exception as e:
            #https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
            #logger.error("Failed to open file", exc_info=True)
            self.steps_done[version] = "ERROR"
            self.logger.exception("Migration failed in step: {0}".format(version), *args)
            return False
