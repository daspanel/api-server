#!/usr/bin/env python
from __future__ import absolute_import, division, print_function

# Daspanel system imports
from lib.daspanel_errors import error_msg

# API server imports
from connexion import problem

import werkzeug.exceptions

class DaspanelApiException(werkzeug.exceptions.HTTPException):
    pass


class SiteNotFound(DaspanelApiException):
    def __init__(self, message=None):
        """
        :param reason: Reason why the response did not conform to the specification
        :type reason: str
        """
        self.code = 404
        self.reason = 'Site not found'
        self.message = message

    def __str__(self):  # pragma: no cover
        return "{0} '{1}'".format(self.reason, self.message)

    def __repr__(self):  # pragma: no cover
        return "{0} '{1}'".format(self.reason, self.message)


def api_fail(error_list, errid, *args):
    return problem(*error_msg(error_list, errid, *args))

