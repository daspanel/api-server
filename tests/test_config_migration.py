# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
from distutils.version import StrictVersion
import os, random, string, json, copy, collections

def to_011(cfg_data):
    tmp_data = copy.deepcopy(cfg_data)
    tmp_data['sys']['config_version'] = '0.1.1'
    for item in tmp_data['engines']:
        if item['runtime'] == 'php56':
            item['sitetypes'].extend([
                {'_cuid': '', 'sitetype': 'laravel5x', 'description': 'Laravel 5.X'},
                {'_cuid': '', 'sitetype': 'codeigniter3x', 'description': 'CodeIgniter 3.X'}
            ])
    return tmp_data

def to_012(cfg_data):
    tmp_data = copy.deepcopy(cfg_data)
    tmp_data['sys']['config_version'] = '0.1.2'
    return tmp_data

steps = collections.OrderedDict()
steps['0.1.1'] = to_011
steps['0.1.2'] = to_012

def migrate(from_version, to_version, cfg_data):
    tmp_data = copy.deepcopy(cfg_data)
    for version, f in steps.items():
        if StrictVersion(version) > StrictVersion(from_version):
            if StrictVersion(version) <= StrictVersion(to_version):
                print("\n=== Running migration step: ", version, "===")
                tmp_data = f(cfg_data)
    return tmp_data

config_010 = 'data/config-0.1.0.json'
config_011 = 'data/config-0.1.1.json'

with open(config_010, 'r') as fp:
    tenant_cfg = json.load(fp)
    print("\n************** START FROM 0.1.0 *******************")
    print(json.dumps(tenant_cfg))
    tenant_cfg = migrate('0.1.0', '0.1.1', tenant_cfg)
    print(json.dumps(tenant_cfg))
    print("\n************** END IN 0.1.1 ***********************")

with open(config_011, 'r') as fp:
    tenant_cfg = json.load(fp)
    print("\n************** START FROM 0.1.0 *******************")
    print(json.dumps(tenant_cfg))
    tenant_cfg = migrate('0.1.0', '0.1.2', tenant_cfg)
    print(json.dumps(tenant_cfg))
    print("\n************** END IN 0.1.2 ***********************")
