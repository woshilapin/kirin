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

from __future__ import absolute_import, print_function, unicode_literals, division
from tests.mock_navitia import navitia_response

response = navitia_response.NavitiaResponse()

response.queries = [
    "vehicle_journeys/?filter=vehicle_journey.has_code(source, Code-midnight-UTC)&depth=2&since=20171211T170000+0000&until=20171212T000000+0000"
    # resquest time is UTC -> 12:00 is 07:00 local time in Sherbrooke
]

response.response_code = 200

response.json_response = """
{
    "disruptions": [],
    "feed_publishers": [
        {
            "id": "builder",
            "license": "ODBL",
            "name": "departure board",
            "url": "www.canaltp.fr"
        }
    ],
    "links": [
    ],
    "pagination": {
        "items_on_page": 1,
        "items_per_page": 25,
        "start_page": 0,
        "total_result": 1
    },
    "vehicle_journeys": [
        {
            "calendars": [
                {
                    "active_periods": [
                        {
                            "begin": "20120615",
                            "end": "20130615"
                        }
                    ],
                    "week_pattern": {
                        "friday": true,
                        "monday": false,
                        "saturday": false,
                        "sunday": false,
                        "thursday": false,
                        "tuesday": false,
                        "wednesday": false
                    }
                }
            ],
            "disruptions": [],
            "id": "R:vj1",
            "name": "R:vj1",
            "stop_times": [
                {
                    "arrival_time": "190000",
                    "departure_time": "190000",
                    "utc_arrival_time": "000000",
                    "utc_departure_time": "000000",
                    "headsign": "R:vj1",
"journey_pattern_point": {
                        "id": "journey_pattern_point:14"
                    },
                    "stop_point": {
                        "codes": [
                            {
                                "type": "source",
                                "value": "Code-StopR1"
                            }
                        ],
                        "coord": {
                            "lat": "0",
                            "lon": "0"
                        },
                        "equipments": [
                            "has_wheelchair_boarding",
                            "has_bike_accepted"
                        ],
                        "id": "StopR1",
                        "label": "StopR1",
                        "links": [],
                        "name": "StopR1",
                        "stop_area": {
                            "coord": {
                                "lat": "0",
                                "lon": "0"
                            },
                            "id": "StopR1",
                            "label": "StopR1",
                            "links": [],
                            "name": "StopR1",
                            "timezone": "America/Montreal"
                        }
                    }
                },
                {
                    "arrival_time": "191000",
                    "departure_time": "191000",
                    "utc_arrival_time": "001000",
                    "utc_departure_time": "001000",
                    "headsign": "R:vj1",
                    "journey_pattern_point": {
                        "id": "journey_pattern_point:15"
                    },
                    "stop_point": {
                        "codes": [
                            {
                                "type": "source",
                                "value": "Code-StopR2"
                            }
                        ],
                        "coord": {
                            "lat": "0",
                            "lon": "0"
                        },
                        "equipments": [
                            "has_wheelchair_boarding",
                            "has_bike_accepted"
                        ],
                        "id": "StopR2",
                        "label": "StopR2",
                        "links": [],
                        "name": "StopR2",
                        "stop_area": {
                            "coord": {
                                "lat": "0",
                                "lon": "0"
                            },
                            "id": "StopR2",
                            "label": "StopR2",
                            "links": [],
                            "name": "StopR2",
                            "timezone": "America/Montreal"
                        }
                    }
                },
                {
                    "arrival_time": "192000",
                    "departure_time": "192000",
                    "utc_arrival_time": "002000",
                    "utc_departure_time": "002000",
                    "headsign": "R:vj1",
                    "journey_pattern_point": {
                        "id": "journey_pattern_point:16"
                    },
                    "stop_point": {
                        "codes": [
                            {
                                "type": "source",
                                "value": "Code-StopR3"
                            }
                        ],
                        "coord": {
                            "lat": "0",
                            "lon": "0"
                        },
                        "equipments": [
                            "has_wheelchair_boarding",
                            "has_bike_accepted"
                        ],
                        "id": "StopR3",
                        "label": "StopR3",
                        "links": [],
                        "name": "StopR3",
                        "stop_area": {
                            "coord": {
                                "lat": "0",
                                "lon": "0"
                            },
                            "id": "StopR3",
                            "label": "StopR3",
                            "links": [],
                            "name": "StopR3",
                            "timezone": "America/Montreal"
                        }
                    }
                }
            ],
            "trip": {
                "id": "R:vj1",
                "name": "R:vj1"
            },
            "validity_pattern": {
                "beginning_date": "20120614",
                "days": "100000010000001000000100000010000001000000100000010000001000000100000010000001000000100000010000001000000100000010000001000000100000010000001000000100000010000001000000100000010000001000000100000010000001000000100000010000001000000100000010000001000000100000010000001000000100000010000001000000100000010000001000000100000010000001000000100000010000001000000100000010"
            }
        }
    ]
}
"""
