# coding=utf-8

# Copyright (c) 2001-2020, Canal TP and/or its affiliates. All rights reserved.
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
import flask
from flask import url_for
from flask.globals import current_app
from flask_restful import Resource, marshal, abort
from kirin.exceptions import InvalidArguments
import navitia_wrapper
from kirin import redis_client
from kirin.core import model
from kirin.core.types import ConnectorType


def get_piv_contributors(include_deactivated=False):
    """
    :return: all PIV contributors from db (not configurable via file)
    """
    piv_contributors = [
        c
        for c in model.Contributor.find_by_connector_type(
            ConnectorType.piv.value, include_deactivated=include_deactivated
        )
    ]
    return piv_contributors


def _get_piv(req):
    if not req.data:
        raise InvalidArguments("no piv data provided")
    return req.data


def make_navitia_wrapper(contributor):
    return navitia_wrapper.Navitia(
        url=current_app.config.get(str("NAVITIA_URL")),
        token=contributor.navitia_token,
        timeout=current_app.config.get(str("NAVITIA_TIMEOUT"), 5),
        cache=redis_client,
        query_timeout=current_app.config.get(str("NAVITIA_QUERY_CACHE_TIMEOUT"), 600),
        pubdate_timeout=current_app.config.get(str("NAVITIA_PUBDATE_CACHE_TIMEOUT"), 600),
    ).instance(contributor.navitia_coverage)


class PivIndex(Resource):
    def get(self):
        contributors = get_piv_contributors()

        if not contributors:
            return {"message": "No PIV contributor defined"}, 200

        response = {c.id: {"href": url_for("piv", id=c.id, _external=True)} for c in contributors}
        return response, 200


class Piv(Resource):
    def post(self, id=None):
        if id is None:
            abort(400, message="Contributor's id is missing")

        contributor = (
            model.Contributor.query_existing().filter_by(id=id, connector_type=ConnectorType.piv.value).first()
        )
        if not contributor:
            abort(404, message="Contributor '{}' not found".format(id))

        raw_json = _get_piv(flask.globals.request)

        # TODO: store and handle PIV feed
        return {"message": "PIV feed processed"}, 200