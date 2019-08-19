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
from tests.mock_navitia import navitia_response

response = navitia_response.NavitiaResponse()

response.queries = ['stop_points/?filter=stop_area.has_code("CR-CI-CH", "0087-215632-00")&count=1']

response.response_code = 200

response.json_response = """{
  "pagination": {
    "start_page": 0,
    "items_on_page": 1,
    "items_per_page": 1,
    "total_result": 2
  },
  "links": [
    {
      "href": "http://localhost:5001/v1/coverage/stif/stop_points/{stop_points.id}",
      "type": "stop_points",
      "rel": "stop_points",
      "templated": true
    },
    {
      "href": "http://localhost:5001/v1/coverage/stif/stop_areas/{stop_area.id}",
      "type": "stop_area",
      "rel": "stop_areas",
      "templated": true
    },
    {
      "href": "http://localhost:5001/v1/coverage/stif/stop_points/{stop_points.id}/route_schedules",
      "type": "route_schedules",
      "rel": "route_schedules",
      "templated": true
    },
    {
      "href": "http://localhost:5001/v1/coverage/stif/stop_points/{stop_points.id}/stop_schedules",
      "type": "stop_schedules",
      "rel": "stop_schedules",
      "templated": true
    },
    {
      "href": "http://localhost:5001/v1/coverage/stif/stop_points/{stop_points.id}/arrivals",
      "type": "arrivals",
      "templated": true,
      "rel": "arrivals"
    },
    {
      "href": "http://localhost:5001/v1/coverage/stif/stop_points/{stop_points.id}/departures",
      "type": "departures",
      "rel": "departures",
      "templated": true
    },
    {
      "href": "http://localhost:5001/v1/coverage/stif/stop_points/{stop_points.id}/places_nearby",
      "type": "places_nearby",
      "rel": "places_nearby",
      "templated": true
    },
    {
      "href": "http://localhost:5001/v1/coverage/stif/stop_points/{stop_points.id}/journeys",
      "type": "journey",
      "rel": "journeys",
      "templated": true
    },
    {
      "href": "http://localhost:5001/v1/coverage/stif/stop_points?filter=stop_area.has_code%28%22CR-CI-CH%22%2C+%220087-215632-00%22%29&count=1&start_page=1",
      "type": "next",
      "templated": false
    },
    {
      "href": "http://localhost:5001/v1/coverage/stif/stop_points?filter=stop_area.has_code%28%22CR-CI-CH%22%2C+%220087-215632-00%22%29&count=1&start_page=1",
      "type": "last",
      "templated": false
    },
    {
      "href": "http://localhost:5001/v1/coverage/stif/stop_points?filter=stop_area.has_code%28%22CR-CI-CH%22%2C+%220087-215632-00%22%29&count=1",
      "type": "first",
      "templated": false
    }
  ],
  "disruptions": [],
  "feed_publishers": [],
  "context": {
    "timezone": "Europe/Paris",
    "current_datetime": "20190510T161500"
  },
  "stop_points": [
    {
      "name": "gare de Oermingen",
      "links": [],
      "coord": {
        "lat": "49.001025",
        "lon": "7.131844"
      },
      "label": "gare de Oermingen (Oermingen)",
      "equipments": [],
      "administrative_regions": [
        {
          "insee": "67355",
          "name": "Oermingen",
          "level": 8,
          "coord": {
            "lat": "48.999905",
            "lon": "7.129222"
          },
          "label": "Oermingen (67970)",
          "id": "admin:fr:67355",
          "zip_code": "67970"
        }
      ],
      "fare_zone": {
        "name": "0"
      },
      "id": "stop_point:OCE:SP:CarTER-87215632",
      "stop_area": {
        "codes": [
          {
            "type": "CR-CI-CH",
            "value": "0087-215632-00"
          },
          {
            "type": "UIC8",
            "value": "87215632"
          },
          {
            "type": "external_code",
            "value": "OCE87215632"
          }
        ],
        "name": "gare de Oermingen",
        "links": [],
        "coord": {
          "lat": "49.001025",
          "lon": "7.131844"
        },
        "label": "gare de Oermingen (Oermingen)",
        "timezone": "Europe/Paris",
        "id": "stop_area:OCE:SA:87215632"
      }
    }
  ]
}
"""
