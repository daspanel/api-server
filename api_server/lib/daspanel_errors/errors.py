#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sites errors
~~~~~~~~~~~~

Contains error definitions for Daspanel system.

:copyright: (c) 2016 by Abner G Jacobsen
:licence: GPL-3, see LICENCE for more details
"""
from __future__ import absolute_import, division, print_function

error_doc = 'https://daspanel.com/docs/api/daspanel/errors'

class ApiErrorMsgType(list):
    def __init__(self, *args):
        # HTTP code
        self.append(args[0])
        # Title
        self.append(args[1])
        # Detail
        self.append(args[2])
        # Type URI
        self.append(args[3])

    def __getattr__(self, item):
        return self[item]

def error_msg(error_list, errid, *args):
    #print("error_msg.error_list: ", error_list)
    #print("error_msg.errid: ", errid)
    #print("error_msg.args: ", *args)
    retlist = error_list[errid]
    #print("retlist: ", retlist)
    retlist[2] = retlist[2].format(*args)
    return retlist

DASPANEL_ERRORS = {
    'NOTFOUND': ApiErrorMsgType(404, 'Not Found', 
        'Not found: {0}', error_doc),
    'INVALIDAPIKEY': ApiErrorMsgType(401, 
        'Invalid API Key', 'Invalid API key: {0}', error_doc),
    'FSMISSINGDRIVER': ApiErrorMsgType(401, 'Missing File System Driver', 
        'DasPanel Api server is not running this file system driver: {0}', 
        error_doc),
    'FSDIREXISTS': ApiErrorMsgType(401, 'Directory Exists', 
        'Directory exists in file system: {0}', 
        error_doc),
    'FSFILEEXISTS': ApiErrorMsgType(401, 'File Exists', 
        'File exists in file system: {0}', 
        error_doc),
    'NOTZIPFILE': ApiErrorMsgType(401, 'File is not zip', 
        'File is not of the type zip: {0}', 
        error_doc),
    'PSMISSINGDRIVER': ApiErrorMsgType(401, 'Missing PubSub System Driver', 
        'DasPanel Api server is not running this pubsub system driver: {0}', 
        error_doc),
}

