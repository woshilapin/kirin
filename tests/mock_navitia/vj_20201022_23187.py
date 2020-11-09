# coding=utf-8

#  Copyright (c) Canal TP and/or its affiliates. All rights reserved.
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
from tests.mock_navitia import navitia_response

response = navitia_response.NavitiaResponse()

response.queries = [
    'vehicle_journeys/?filter=vehicle_journey.has_code("rt_piv", "2020-10-22:23187:1187:rail:regionalRail:FERRE")&depth=2&show_codes=true',
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
            "href": "http://localhost:5000/v1/coverage/default/stop_points/{stop_point.id}",
            "type": "stop_point",
            "rel": "stop_points",
            "templated": true
        },
        {
            "href": "http://localhost:5000/v1/coverage/default/stop_areas/{stop_area.id}",
            "type": "stop_area",
            "rel": "stop_areas",
            "templated": true
        },
        {
            "href": "http://localhost:5000/v1/coverage/default/journey_patterns/{journey_pattern.id}",
            "type": "journey_pattern",
            "rel": "journey_patterns",
            "templated": true
        },
        {
            "href": "http://localhost:5000/v1/coverage/default/disruptions/{disruptions.id}",
            "type": "disruptions",
            "rel": "disruptions",
            "templated": true
        },
        {
            "href": "http://localhost:5000/v1/coverage/default/routes/{route.id}",
            "type": "route",
            "rel": "routes",
            "templated": true
        },
        {
            "href": "http://localhost:5000/v1/coverage/default/disruptions/{disruption.id}",
            "type": "disruption",
            "rel": "disruptions",
            "templated": true
        },
        {
            "href": "http://localhost:5000/v1/coverage/default/journey_pattern_points/{journey_pattern_point.id}",
            "type": "journey_pattern_point",
            "rel": "journey_pattern_points",
            "templated": true
        },
        {
            "href": "http://localhost:5000/v1/coverage/default/vehicle_journeys/{vehicle_journeys.id}",
            "type": "vehicle_journeys",
            "rel": "vehicle_journeys",
            "templated": true
        },
        {
            "href": "http://localhost:5000/v1/coverage/default/trips/{trip.id}",
            "type": "trip",
            "rel": "trips",
            "templated": true
        },
        {
            "href": "http://localhost:5000/v1/coverage/default/vehicle_journeys?filter=vehicle_journey.has_code%28%22rt_piv%22%2C+%222020-10-22%3A23187%3A1187%3Arail%3AregionalRail%3AFERRE%22%29&depth=2&show_codes=true",
            "type": "first",
            "templated": false
        }
    ],
    "disruptions": [],
    "feed_publishers": [
        {
            "url": "",
            "id": "default",
            "license": "Private (unspecified)",
            "name": "Sncf PIV"
        }
    ],
    "context": {
        "timezone": "Europe/Paris",
        "current_datetime": "20201023T151251"
    },
    "vehicle_journeys": [
        {
            "codes": [
                {
                    "type": "rt_piv",
                    "value": "2020-10-22:23187:1187:rail:regionalRail:FERRE"
                },
                {
                    "type": "source",
                    "value": "7311859b76bd5a817c32a16884caa7a6"
                }
            ],
            "name": "23187",
            "journey_pattern": {
                "route": {
                    "direction": {
                        "embedded_type": "stop_area",
                        "stop_area": {
                            "codes": [
                                {
                                    "type": "source",
                                    "value": "87745497"
                                }
                            ],
                            "name": "",
                            "links": [],
                            "coord": {
                                "lat": "0",
                                "lon": "0"
                            },
                            "label": "",
                            "timezone": "Europe/Paris",
                            "id": "stop_area:PIV:87745497"
                        },
                        "quality": 0,
                        "name": "",
                        "id": "stop_area:PIV:87745497"
                    },
                    "name": "L4",
                    "links": [],
                    "is_frequence": "False",
                    "geojson": {
                        "type": "MultiLineString",
                        "coordinates": []
                    },
                    "direction_type": "forward",
                    "id": "route:PIV:FR:Line::3DCDF960-BA93-4443-899F-283A2A13B7FE:"
                },
                "id": "journey_pattern:3736",
                "name": "journey_pattern:3736"
            },
            "disruptions": [],
            "calendars": [
                {
                    "active_periods": [
                        {
                            "begin": "20201022",
                            "end": "20201023"
                        }
                    ],
                    "week_pattern": {
                        "monday": false,
                        "tuesday": false,
                        "friday": false,
                        "wednesday": false,
                        "thursday": true,
                        "sunday": false,
                        "saturday": false
                    }
                }
            ],
            "stop_times": [
                {
                    "stop_point": {
                        "name": "",
                        "links": [],
                        "coord": {
                            "lat": "0",
                            "lon": "0"
                        },
                        "label": "",
                        "equipments": [],
                        "id": "stop_point:PIV:85010231:Train",
                        "stop_area": {
                            "codes": [
                                {
                                    "type": "source",
                                    "value": "85010231"
                                }
                            ],
                            "name": "",
                            "links": [],
                            "coord": {
                                "lat": "0",
                                "lon": "0"
                            },
                            "label": "",
                            "timezone": "Europe/Paris",
                            "id": "stop_area:PIV:85010231"
                        }
                    },
                    "utc_arrival_time": "203400",
                    "utc_departure_time": "203400",
                    "headsign": "PIV:2020-10-22:23187:1187:Train",
                    "arrival_time": "223400",
                    "journey_pattern_point": {
                        "id": "journey_pattern_point:38356"
                    },
                    "drop_off_allowed": false,
                    "pickup_allowed": true,
                    "departure_time": "223400"
                },
                {
                    "stop_point": {
                        "name": "",
                        "links": [],
                        "coord": {
                            "lat": "0",
                            "lon": "0"
                        },
                        "label": "",
                        "equipments": [],
                        "id": "stop_point:PIV:85010157:Train",
                        "stop_area": {
                            "codes": [
                                {
                                    "type": "source",
                                    "value": "85010157"
                                }
                            ],
                            "name": "",
                            "links": [],
                            "coord": {
                                "lat": "0",
                                "lon": "0"
                            },
                            "label": "",
                            "timezone": "Europe/Paris",
                            "id": "stop_area:PIV:85010157"
                        }
                    },
                    "utc_arrival_time": "203500",
                    "utc_departure_time": "203530",
                    "headsign": "PIV:2020-10-22:23187:1187:Train",
                    "arrival_time": "223500",
                    "journey_pattern_point": {
                        "id": "journey_pattern_point:38357"
                    },
                    "drop_off_allowed": true,
                    "pickup_allowed": true,
                    "departure_time": "223530"
                },
                {
                    "stop_point": {
                        "name": "",
                        "links": [],
                        "coord": {
                            "lat": "0",
                            "lon": "0"
                        },
                        "label": "",
                        "equipments": [],
                        "id": "stop_point:PIV:85010140:Train",
                        "stop_area": {
                            "codes": [
                                {
                                    "type": "source",
                                    "value": "85010140"
                                }
                            ],
                            "name": "",
                            "links": [],
                            "coord": {
                                "lat": "0",
                                "lon": "0"
                            },
                            "label": "",
                            "timezone": "Europe/Paris",
                            "id": "stop_area:PIV:85010140"
                        }
                    },
                    "utc_arrival_time": "204700",
                    "utc_departure_time": "204800",
                    "headsign": "PIV:2020-10-22:23187:1187:Train",
                    "arrival_time": "224700",
                    "journey_pattern_point": {
                        "id": "journey_pattern_point:38358"
                    },
                    "drop_off_allowed": true,
                    "pickup_allowed": true,
                    "departure_time": "224800"
                },
                {
                    "stop_point": {
                        "name": "",
                        "links": [],
                        "coord": {
                            "lat": "0",
                            "lon": "0"
                        },
                        "label": "",
                        "equipments": [],
                        "id": "stop_point:PIV:85162735:Train",
                        "stop_area": {
                            "codes": [
                                {
                                    "type": "source",
                                    "value": "85162735"
                                }
                            ],
                            "name": "",
                            "links": [],
                            "coord": {
                                "lat": "0",
                                "lon": "0"
                            },
                            "label": "",
                            "timezone": "Europe/Paris",
                            "id": "stop_area:PIV:85162735"
                        }
                    },
                    "utc_arrival_time": "211600",
                    "utc_departure_time": "211700",
                    "headsign": "PIV:2020-10-22:23187:1187:Train",
                    "arrival_time": "231600",
                    "journey_pattern_point": {
                        "id": "journey_pattern_point:38370"
                    },
                    "drop_off_allowed": true,
                    "pickup_allowed": true,
                    "departure_time": "231700"
                },
                {
                    "stop_point": {
                        "name": "",
                        "links": [],
                        "coord": {
                            "lat": "0",
                            "lon": "0"
                        },
                        "label": "",
                        "equipments": [],
                        "id": "stop_point:PIV:85162750:Train",
                        "stop_area": {
                            "codes": [
                                {
                                    "type": "source",
                                    "value": "85162750"
                                }
                            ],
                            "name": "",
                            "links": [],
                            "coord": {
                                "lat": "0",
                                "lon": "0"
                            },
                            "label": "",
                            "timezone": "Europe/Paris",
                            "id": "stop_area:PIV:85162750"
                        }
                    },
                    "utc_arrival_time": "211900",
                    "utc_departure_time": "212000",
                    "headsign": "PIV:2020-10-22:23187:1187:Train",
                    "arrival_time": "231900",
                    "journey_pattern_point": {
                        "id": "journey_pattern_point:38371"
                    },
                    "drop_off_allowed": true,
                    "pickup_allowed": true,
                    "departure_time": "232000"
                },
                {
                    "stop_point": {
                        "name": "",
                        "links": [],
                        "coord": {
                            "lat": "0",
                            "lon": "0"
                        },
                        "label": "",
                        "equipments": [],
                        "id": "stop_point:PIV:87745497:Train",
                        "stop_area": {
                            "codes": [
                                {
                                    "type": "source",
                                    "value": "87745497"
                                }
                            ],
                            "name": "",
                            "links": [],
                            "coord": {
                                "lat": "0",
                                "lon": "0"
                            },
                            "label": "",
                            "timezone": "Europe/Paris",
                            "id": "stop_area:PIV:87745497"
                        }
                    },
                    "utc_arrival_time": "212500",
                    "utc_departure_time": "212500",
                    "headsign": "PIV:2020-10-22:23187:1187:Train",
                    "arrival_time": "232500",
                    "journey_pattern_point": {
                        "id": "journey_pattern_point:38372"
                    },
                    "drop_off_allowed": true,
                    "pickup_allowed": false,
                    "departure_time": "232500"
                }
            ],
            "validity_pattern": {
                "beginning_date": "20201017",
                "days": "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000"
            },
            "headsign": "PIV:2020-10-22:23187:1187:Train",
            "id": "vehicle_journey:PIV:2020-10-22:23187:1187:Train",
            "trip": {
                "id": "PIV:2020-10-22:23187:1187:Train",
                "name": "23187"
            }
        }
    ]
}"""
