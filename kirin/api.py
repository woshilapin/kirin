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
import logging

from flask.signals import got_request_exception
import flask_restful
from flask import request
from kirin import resources
from kirin.piv import piv
from kirin.gtfs_rt import gtfs_rt
from kirin.cots import cots
from kirin import app

from kirin.utils import log_exception

flask_restful.representations.json.settings = {"indent": 4}  # we always want pretty json

api = flask_restful.Api(app, catch_all_404s=True)
api.app.url_map.strict_slashes = False

api.add_resource(resources.Index, "/", endpoint=str("index"))
api.add_resource(resources.Status, "/status", endpoint=str("status"))
api.add_resource(cots.Cots, "/cots", endpoint=str("cots"))
api.add_resource(piv.PivIndex, "/piv", endpoint=str("piv_index"))
api.add_resource(piv.Piv, "/piv/<string:id>", endpoint=str("piv"))
api.add_resource(gtfs_rt.GtfsRTIndex, "/gtfs_rt", endpoint=str("gtfs_rt_index"))
api.add_resource(gtfs_rt.GtfsRT, "/gtfs_rt/<string:id>", endpoint=str("gtfs_rt"))
api.add_resource(
    resources.Contributors, "/contributors", "/contributors/<string:id>", endpoint=str("contributors")
)
api.add_resource(resources.Health, "/health", endpoint=str("health"))


def _log_exception(sender, exception):
    log_exception(exception, request.url)


got_request_exception.connect(_log_exception, app)


@app.after_request
def access_log(response, *args, **kwargs):
    logger = logging.getLogger("kirin.access")
    logger.info('"%s %s" %s', request.method, request.full_path, response.status_code)
    return response
