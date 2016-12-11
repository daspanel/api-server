#!/usr/bin/env python
import datetime
import logging

from connexion import NoContent

# our memory-only pet storage
SERVICES = []
SERVICES.append(
    {'service': 'sites', 'urls': {'endpoint': '/1.0/sites', 'endpoint_doc': '/1.0/sites/ui/'}}
)

def status():
    return NoContent, 200

def services():
    return [service for service in SERVICES], 200
    #return NoContent, 200


