# coding=utf-8

# Copyright (c) 2001-2015, Canal TP and/or its affiliates. All rights reserved.
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

from flask_restful import Resource, url_for
import kirin
from kirin.version import version
from flask import current_app
from kirin.core import model


class Index(Resource):
    def get(self):
        response = {
            "status": {"href": url_for("status", _external=True)},
            "cots": {"href": url_for("cots", _external=True)},
        }
        return response, 200


class Status(Resource):
    def get(self):
        res = model.RealTimeUpdate.get_probes_by_contributor()
        res["version"] = version
        res["db_pool_status"] = kirin.db.engine.pool.status()
        res["db_version"] = kirin.db.engine.scalar("select version_num from alembic_version;")
        res["navitia_url"] = current_app.config["NAVITIA_URL"]
        res["rabbitmq_info"] = kirin.rabbitmq_handler.info()
        return res, 200
