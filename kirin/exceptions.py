# coding=utf-8

# Copyright (c) 2001, Canal TP and/or its affiliates. All rights reserved.
#
# This file is part of Navitia,
#     the software to build cool stuff with public transport.
#
# Hope you'll enjoy and contribute to this project,
#     powered by Canal TP (www.canaltp.fr).
# Help us simplify mobility and open public transport:
#     a non ending quest to the responsive locomotion way of traveling!
#
# LICENCE: This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Stay tuned using
# twitter @navitia
# [matrix] channel #navitia:matrix.org (https://app.element.io/#/room/#navitia:matrix.org)
# https://groups.google.com/d/forum/navitia
# www.navitia.io
from __future__ import absolute_import, print_function, unicode_literals, division
from werkzeug.exceptions import HTTPException


class KirinException(HTTPException):
    """
    All kirin exception must inherit from this one and define a code and a short message
    """

    def __init__(self, detailed_message=None):
        super(KirinException, self).__init__()
        self.data = {"status": self.code, "message": self.message}
        if detailed_message:
            self.data["error"] = detailed_message

    def __str__(self):
        code = self.code if self.code is not None else "???"
        res = "{c} {n}:".format(c=code, n=self.name)
        if self.description is not None:
            res += " {} -".format(self.description)
        if self.message is not None:
            res += " {} -".format(self.message)
        if self.data and "error" in self.data:
            res += " {}".format(self.data["error"])
        return res


class InvalidArguments(KirinException):
    code = 400
    message = "invalid arguments"


class ObjectNotFound(KirinException):
    code = 404
    message = "object not found"


class MessageNotPublished(KirinException):
    code = 500
    message = "impossible to publish message on network"


class InternalException(KirinException):
    code = 500
    message = "an internal error occurred"


class SubServiceError(KirinException):
    code = 404
    message = "object not found (error on sub-service)"


class UnauthorizedOnSubService(SubServiceError):
    message = "object not found (unauthorized on sub-service)"


class UnsupportedValue(KirinException):
    code = 400
    message = "unsupported value"
