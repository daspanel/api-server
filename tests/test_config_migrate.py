# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import os, sys, time, json

sys.path.insert(0, 'api_server')

import pytest

try:
    from daspanel_migrate import TinyDbMigrate
except:
    from lib.daspanel_migrate import TinyDbMigrate

config_010 = 'tests/cfg_data/config-0.1.0.json'
config_011 = 'tests/cfg_data/config-0.1.1.json'

def test_default():

    with open(config_010, 'r') as fp:
        tenant_cfg = json.load(fp)
        print("\n************** START FROM 0.1.0 *******************")
        print(json.dumps(tenant_cfg))
        test_001 = TinyDbMigrate('0.1.0', '0.1.1', tenant_cfg)
        if not test_001.migrate():
            print("\n==== Failed ====")
            for step, status in test_001.steps_done.items():
                print(step, status)
        else:
            print(json.dumps(test_001.to_data))
        print("\n************** END IN 0.1.1 ***********************")

#with open(config_011, 'r') as fp:
#    tenant_cfg = json.load(fp)
#    print("\n************** START FROM 0.1.0 *******************")
#    print(json.dumps(tenant_cfg))
#    tenant_cfg = migrate('0.1.0', '0.1.2', tenant_cfg)
#    print(json.dumps(tenant_cfg))
#    print("\n************** END IN 0.1.2 ***********************")
