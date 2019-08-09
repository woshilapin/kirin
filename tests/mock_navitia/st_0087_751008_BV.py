# coding=utf-8
#
# Copyright (c) 2001-2018, Canal TP and/or its affiliates. All rights reserved.
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
import navitia_response

response = navitia_response.NavitiaResponse()

response.queries = ['stop_points/?filter=stop_area.has_code("CR-CI-CH", "0087-751008-BV")&count=1']

response.response_code = 200

response.json_response = """
{
"stop_points": [
    {
      "name": "gare de Marseille-St-Charles",
      "links": [],
      "coord": {
        "lat": "43.30273",
        "lon": "5.380659"
      },
      "label": "gare de Marseille-St-Charles",
      "equipments": [],
      "id": "stop_point:OCE:SP:CarTER-87751008",
      "stop_area": {
        "codes": [
          {
            "type": "CR-CI-CH",
            "value": "0087-751008-BV"
          },
          {
            "type": "UIC8",
            "value": "87751008"
          },
          {
            "type": "external_code",
            "value": "OCE87751008"
          }
        ],
        "name": "gare de Marseille-St-Charles",
        "links": [],
        "coord": {
          "lat": "43.30273",
          "lon": "5.380659"
        },
        "label": "gare de Marseille-St-Charles",
        "timezone": "Europe/Paris",
        "id": "stop_area:OCE:SA:87751008"
      }
    }
  ]
}
"""
