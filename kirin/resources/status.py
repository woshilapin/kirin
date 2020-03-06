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

from __future__ import absolute_import, print_function, unicode_literals, division
from flask_restful import Resource
import kirin
from kirin.version import version
from flask import current_app
from kirin.utils import (
    get_database_version,
    get_database_info,
    can_connect_to_navitia,
    can_connect_to_database,
    get_database_pool_status,
)


class Status(Resource):
    def get(self):
        res = get_database_info()
        res["version"] = version
        res["db_pool_status"] = get_database_pool_status()
        res["db_version"] = get_database_version()
        res["navitia_url"] = current_app.config[str("NAVITIA_URL")]
        res["rabbitmq_info"] = kirin.rmq_handler.info()
        res["navitia_connection"] = "OK" if can_connect_to_navitia() else "KO"
        res["db_connection"] = "OK" if can_connect_to_database() else "KO"

        return res, 200
