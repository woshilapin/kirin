# coding=utf-8

# Copyright (c) 2001-2019, Canal TP and/or its affiliates. All rights reserved.
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
# IRC #navitia on freenode
# https://groups.google.com/d/forum/navitia
# www.navitia.io

from __future__ import absolute_import, print_function, unicode_literals, division
import flask
from flask_restful import Resource, marshal_with_field, marshal_with, fields, abort
from kirin.core import model

contributor_fields = {
    "id": fields.String,
    "navitia_coverage": fields.String,
    "navitia_token": fields.String,
    "feed_url": fields.String,
    "connector_type": fields.String,
}


class Contributors(Resource):
    @marshal_with_field(fields.List(fields.Nested(contributor_fields)))
    def get(self, id=None):
        q = model.db.session.query(model.Contributor)

        if id is not None:
            q = q.filter(model.Contributor.id == id)

        return q.all()

    @marshal_with(contributor_fields)
    def post(self):
        data = flask.request.get_json()
        token = data.get("navitia_token", None)
        feed_url = data.get("feed_url", None)
        try:
            new_contrib = model.Contributor(
                data["id"], data["navitia_coverage"], data["connector_type"], token, feed_url
            )
            model.db.session.add(new_contrib)
            model.db.session.commit()
            return new_contrib, 201
        except KeyError as e:
            err_msg = "Missing attribute '{}' in input data to construct a contributor".format(e)
            abort(400, message=err_msg)
        except Exception as e:
            abort(400, message="Error while creating contributor - {}".format(e))
