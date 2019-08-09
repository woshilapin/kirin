# coding=utf-8

#  Copyright (c) 2001-2018, Canal TP and/or its affiliates. All rights reserved.
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
import navitia_response
from __future__ import absolute_import, print_function, unicode_literals, division

response = navitia_response.NavitiaResponse()

response.queries = [
    "vehicle_journeys/?depth=2&since=20121119T224500+0000&headsign=8837&show_codes=true&until=20121120T021500+0000"
]

response.response_code = 200

response.json_response = """{
  "pagination": {
    "start_page": 0,
    "items_on_page": 1,
    "items_per_page": 25,
    "total_result": 1
  },
  "links": [
    {
      "href": "http://localhost:5001/v1/coverage/stif/stop_points/{stop_point.id}",
      "type": "stop_point",
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
      "href": "http://localhost:5001/v1/coverage/stif/journey_patterns/{journey_pattern.id}",
      "type": "journey_pattern",
      "rel": "journey_patterns",
      "templated": true
    },
    {
      "href": "http://localhost:5001/v1/coverage/stif/routes/{route.id}",
      "type": "route",
      "rel": "routes",
      "templated": true
    },
    {
      "href": "http://localhost:5001/v1/coverage/stif/journey_pattern_points/{journey_pattern_point.id}",
      "type": "journey_pattern_point",
      "rel": "journey_pattern_points",
      "templated": true
    },
    {
      "href": "http://localhost:5001/v1/coverage/stif/vehicle_journeys/{vehicle_journeys.id}",
      "type": "vehicle_journeys",
      "rel": "vehicle_journeys",
      "templated": true
    },
    {
      "href": "http://localhost:5001/v1/coverage/stif/trips/{trip.id}",
      "type": "trip",
      "rel": "trips",
      "templated": true
    },
    {
      "href": "http://localhost:5001/v1/coverage/stif/vehicle_journeys?depth=2&show_codes=true&since=20121119T224500%2B0000&headsign=8837&until=20121120T021500%2B0000",
      "type": "first",
      "templated": false
    }
  ],
  "disruptions": [],
  "feed_publishers": [],
  "context": {
    "timezone": "Europe/Paris",
    "current_datetime": "20190513T114949"
  },
  "vehicle_journeys": [
    {
      "codes": [],
      "name": "8837",
      "journey_pattern": {
        "route": {
          "direction": {
            "embedded_type": "stop_area",
            "stop_area": {
              "codes": [
                {
                  "type": "CR-CI-CH",
                  "value": "0080-205427-BV"
                },
                {
                  "type": "UIC8",
                  "value": "80206581"
                },
                {
                  "type": "external_code",
                  "value": "OCE80206581"
                }
              ],
              "name": "gare de Muenchen-Aeroport-J-Str",
              "links": [],
              "coord": {
                "lat": "0",
                "lon": "0"
              },
              "label": "gare de Muenchen-Aeroport-J-Str",
              "timezone": "Europe/Paris",
              "id": "stop_area:OCE:SA:80206581"
            },
            "quality": 0,
            "name": "gare de Muenchen-Aeroport-J-Str",
            "id": "stop_area:OCE:SA:80206581"
          },
          "name": "Herrsching vers Muenchen-Aeroport-J-Str",
          "links": [],
          "is_frequence": "False",
          "geojson": {
            "type": "MultiLineString",
            "coordinates": []
          },
          "direction_type": "forward",
          "id": "route:OCE:Train-80203422-80206581-1"
        },
        "id": "journey_pattern:8784",
        "name": "journey_pattern:8784"
      },
      "disruptions": [],
      "calendars": [
        {
          "active_periods": [
            {
              "begin": "20121027",
              "end": "20121208"
            }
          ],
          "week_pattern": {
            "monday": true,
            "tuesday": true,
            "friday": true,
            "wednesday": true,
            "thursday": true,
            "sunday": true,
            "saturday": true
          }
        }
      ],
      "stop_times": [
        {
          "stop_point": {
            "name": "gare de Herrsching",
            "links": [],
            "coord": {
              "lat": "0",
              "lon": "0"
            },
            "label": "gare de Herrsching",
            "equipments": [],
            "fare_zone": {
              "name": "0"
            },
            "id": "stop_point:OCE:SP:Train-80203422",
            "stop_area": {
              "codes": [
                {
                  "type": "CR-CI-CH",
                  "value": "0080-203422-BV"
                },
                {
                  "type": "UIC8",
                  "value": "80203422"
                },
                {
                  "type": "external_code",
                  "value": "OCE80203422"
                }
              ],
              "name": "gare de Herrsching",
              "links": [],
              "coord": {
                "lat": "0",
                "lon": "0"
              },
              "label": "gare de Herrsching",
              "timezone": "Europe/Paris",
              "id": "stop_area:OCE:SA:80203422"
            }
          },
          "utc_arrival_time": "234500",
          "utc_departure_time": "234500",
          "headsign": "8837",
          "arrival_time": "004500",
          "journey_pattern_point": {
            "id": "journey_pattern_point:83963"
          },
          "departure_time": "004500"
        },
        {
          "stop_point": {
            "name": "gare de Muenchen hbf (Tief)",
            "links": [],
            "coord": {
              "lat": "0",
              "lon": "0"
            },
            "label": "gare de Muenchen hbf (Tief)",
            "equipments": [],
            "fare_zone": {
              "name": "0"
            },
            "id": "stop_point:OCE:SP:Train-80205815",
            "stop_area": {
              "codes": [
                {
                  "type": "CR-CI-CH",
                  "value": "0080-205815-BV"
                },
                {
                  "type": "UIC8",
                  "value": "80205815"
                },
                {
                  "type": "external_code",
                  "value": "OCE80205815"
                }
              ],
              "name": "gare de Muenchen hbf (Tief)",
              "links": [],
              "coord": {
                "lat": "0",
                "lon": "0"
              },
              "label": "gare de Muenchen hbf (Tief)",
              "timezone": "Europe/Paris",
              "id": "stop_area:OCE:SA:80205815"
            }
          },
          "utc_arrival_time": "003400",
          "utc_departure_time": "003500",
          "headsign": "8837",
          "arrival_time": "013400",
          "journey_pattern_point": {
            "id": "journey_pattern_point:83964"
          },
          "departure_time": "013500"
        },
        {
          "stop_point": {
            "name": "gare de Muenchen-Aeroport-J-Str",
            "links": [],
            "coord": {
              "lat": "0",
              "lon": "0"
            },
            "label": "gare de Muenchen-Aeroport-J-Str",
            "equipments": [],
            "fare_zone": {
              "name": "0"
            },
            "id": "stop_point:OCE:SP:Train-80206581",
            "stop_area": {
              "codes": [
                {
                  "type": "CR-CI-CH",
                  "value": "0080-205427-BV"
                },
                {
                  "type": "UIC8",
                  "value": "80206581"
                },
                {
                  "type": "external_code",
                  "value": "OCE80206581"
                }
              ],
              "name": "gare de Muenchen-Aeroport-J-Str",
              "links": [],
              "coord": {
                "lat": "0",
                "lon": "0"
              },
              "label": "gare de Muenchen-Aeroport-J-Str",
              "timezone": "Europe/Paris",
              "id": "stop_area:OCE:SA:80206581"
            }
          },
          "utc_arrival_time": "011500",
          "utc_departure_time": "011500",
          "headsign": "8837",
          "arrival_time": "021500",
          "journey_pattern_point": {
            "id": "journey_pattern_point:83965"
          },
          "departure_time": "021500"
        }
      ],
      "validity_pattern": {
        "beginning_date": "20120913",
        "days": "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000011111111111111111111111111111111111111111100000000000000000000000000000000000000000000"
      },
      "id": "vehicle_journey:OCE:DB008837F01001_dst_1",
      "trip": {
        "id": "OCE:DB008837F01001",
        "name": "8837"
      }
    }
  ]
}"""
