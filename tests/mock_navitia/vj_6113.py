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
    "vehicle_journeys/?depth=2&since=20151006T101600+0000&headsign=6113&show_codes=true&until=20151006T153400+0000",
    "vehicle_journeys/?depth=2&since=20121120T100000+0000&headsign=6113&show_codes=true&until=20121120T170000+0000",
]

response.response_code = 200

response.json_response = """{
    "vehicle_journeys": [
        {
            "codes": [
                {
                    "type": "external_code",
                    "value": "OCESN006113F02009"
                }
            ],
            "name": "6113",
            "journey_pattern": {
                "route": {
                    "direction": {
                        "embedded_type": "stop_area",
                        "quality": 0,
                        "stop_area": {
                            "codes": [
                                {
                                    "type": "external_code",
                                    "value": "OCE87751008"
                                }
                            ],
                            "name": "gare de Marseille-St-Charles",
                            "links": [

                            ],
                            "coord": {
                                "lat": "43.30273",
                                "lon": "5.380659"
                            },
                            "label": "gare de Marseille-St-Charles",
                            "timezone": "Europe/Paris",
                            "id": "stop_area:OCE:SA:87751008"
                        },
                        "name": "gare de Marseille-St-Charles",
                        "id": "stop_area:OCE:SA:87751008"
                    },
                    "codes": [
                        {
                            "type": "external_code",
                            "value": "OCETGV-87686006-87751008-2"
                        }
                    ],
                    "name": "Paris-Gare-de-Lyon vers Marseille-St-Charles",
                    "links": [

                    ],
                    "is_frequence": "false",
                    "geojson": {
                        "type": "MultiLineString",
                        "coordinates": [

                        ]
                    },
                    "id": "route:OCE:TGV-87686006-87751008-2"
                },
                "name": "gare de Marseille-St-Charles",
                "id": "journey_pattern:OCE:TGV-87751008-87686006-4066"
            },
            "calendars": [
                {
                    "active_periods": [
                        {
                            "begin": "20150916",
                            "end": "20151017"
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
                    "arrival_time": "123700",
                    "utc_arrival_time": "103700",
                    "utc_departure_time": "103700",
                    "journey_pattern_point": {
                        "id": "OCE:TGV-87751008-87686006-4066:OCE:SP:TGV-87686006:0"
                    },
                    "headsign": "6113",
                    "departure_time": "123700",
                    "stop_point": {
                        "codes": [
                            {
                                "type": "external_code",
                                "value": "OCETGV-87686006"
                            }
                        ],
                        "name": "gare de Paris-Gare-de-Lyon",
                        "links": [

                        ],
                        "coord": {
                            "lat": "48.844924",
                            "lon": "2.373481"
                        },
                        "label": "gare de Paris-Gare-de-Lyon",
                        "equipments": [

                        ],
                        "id": "stop_point:OCE:SP:TGV-87686006",
                        "stop_area": {
                            "codes": [
                                {
                                    "type": "external_code",
                                    "value": "OCE87686006"
                                }
                            ],
                            "name": "gare de Paris-Gare-de-Lyon",
                            "links": [

                            ],
                            "coord": {
                                "lat": "48.844924",
                                "lon": "2.373481"
                            },
                            "label": "gare de Paris-Gare-de-Lyon",
                            "timezone": "Europe/Paris",
                            "id": "stop_area:OCE:SA:87686006"
                        }
                    }
                },
                {
                    "arrival_time": "152100",
                    "utc_arrival_time": "132100",
                    "utc_departure_time": "132400",
                    "journey_pattern_point": {
                        "id": "OCE:TGV-87751008-87686006-4066:OCE:SP:TGV-87318964:1"
                    },
                    "headsign": "6113",
                    "departure_time": "152400",
                    "stop_point": {
                        "codes": [
                            {
                                "type": "external_code",
                                "value": "OCETGV-87318964"
                            }
                        ],
                        "name": "gare de Avignon-TGV",
                        "links": [

                        ],
                        "coord": {
                            "lat": "43.921963",
                            "lon": "4.78616"
                        },
                        "label": "gare de Avignon-TGV",
                        "equipments": [

                        ],
                        "id": "stop_point:OCE:SP:TGV-87318964",
                        "stop_area": {
                            "codes": [
                                {
                                    "type": "external_code",
                                    "value": "OCE87318964"
                                }
                            ],
                            "name": "gare de Avignon-TGV",
                            "links": [

                            ],
                            "coord": {
                                "lat": "43.921963",
                                "lon": "4.78616"
                            },
                            "label": "gare de Avignon-TGV",
                            "timezone": "Europe/Paris",
                            "id": "stop_area:OCE:SA:87318964"
                        }
                    }
                },
                {
                    "arrival_time": "154300",
                    "utc_arrival_time": "134300",
                    "utc_departure_time": "134600",
                    "journey_pattern_point": {
                        "id": "OCE:TGV-87751008-87686006-4066:OCE:SP:TGV-87319012:2"
                    },
                    "headsign": "6113",
                    "departure_time": "154600",
                    "stop_point": {
                        "codes": [
                            {
                                "type": "external_code",
                                "value": "OCETGV-87319012"
                            }
                        ],
                        "name": "gare de Aix-en-Provence-TGV",
                        "links": [

                        ],
                        "coord": {
                            "lat": "43.455151",
                            "lon": "5.317273"
                        },
                        "label": "gare de Aix-en-Provence-TGV",
                        "equipments": [

                        ],
                        "id": "stop_point:OCE:SP:TGV-87319012",
                        "stop_area": {
                            "codes": [
                                {
                                    "type": "external_code",
                                    "value": "OCE87319012"
                                }
                            ],
                            "name": "gare de Aix-en-Provence-TGV",
                            "links": [

                            ],
                            "coord": {
                                "lat": "43.455151",
                                "lon": "5.317273"
                            },
                            "label": "gare de Aix-en-Provence-TGV",
                            "timezone": "Europe/Paris",
                            "id": "stop_area:OCE:SA:87319012"
                        }
                    }
                },
                {
                    "arrival_time": "160300",
                    "utc_arrival_time": "140300",
                    "utc_departure_time": "140300",
                    "journey_pattern_point": {
                        "id": "OCE:TGV-87751008-87686006-4066:OCE:SP:TGV-87751008:3"
                    },
                    "headsign": "6113",
                    "departure_time": "160300",
                    "stop_point": {
                        "codes": [
                            {
                                "type": "external_code",
                                "value": "OCETGV-87751008"
                            }
                        ],
                        "name": "gare de Marseille-St-Charles",
                        "links": [

                        ],
                        "coord": {
                            "lat": "43.30273",
                            "lon": "5.380659"
                        },
                        "label": "gare de Marseille-St-Charles",
                        "equipments": [

                        ],
                        "id": "stop_point:OCE:SP:TGV-87751008",
                        "stop_area": {
                            "codes": [
                                {
                                    "type": "external_code",
                                    "value": "OCE87751008"
                                }
                            ],
                            "name": "gare de Marseille-St-Charles",
                            "links": [

                            ],
                            "coord": {
                                "lat": "43.30273",
                                "lon": "5.380659"
                            },
                            "label": "gare de Marseille-St-Charles",
                            "timezone": "Europe/Paris",
                            "id": "stop_area:OCE:SA:87751008"
                        }
                    }
                }
            ],
            "validity_pattern": {
                "beginning_date": "20150915",
                "days": "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000011111111111111111111111111111110"
            },
            "id": "vehicle_journey:OCETGV-87686006-87751008-2:25768",
            "trip": {"id": "trip:OCETGV-87686006-87751008-2:25768"}
        }
    ],
    "disruptions": [

    ],
    "pagination": {
        "start_page": 0,
        "items_on_page": 1,
        "items_per_page": 25,
        "total_result": 1
    },
    "links": [
        {
            "href": "http://localhost:5000/v1/coverage/navitia/stop_points/{stop_point.id}",
            "type": "stop_point",
            "rel": "stop_points",
            "templated": true
        },
        {
            "href": "http://localhost:5000/v1/coverage/navitia/stop_areas/{stop_area.id}",
            "type": "stop_area",
            "rel": "stop_areas",
            "templated": true
        },
        {
            "href": "http://localhost:5000/v1/coverage/navitia/journey_patterns/{journey_pattern.id}",
            "type": "journey_pattern",
            "rel": "journey_patterns",
            "templated": true
        },
        {
            "href": "http://localhost:5000/v1/coverage/navitia/routes/{route.id}",
            "type": "route",
            "rel": "routes",
            "templated": true
        },
        {
            "href": "http://localhost:5000/v1/coverage/navitia/journey_pattern_points/{journey_pattern_point.id}",
            "type": "journey_pattern_point",
            "rel": "journey_pattern_points",
            "templated": true
        },
        {
            "href": "http://localhost:5000/v1/coverage/navitia/vehicle_journeys/{vehicle_journeys.id}",
            "type": "vehicle_journeys",
            "rel": "vehicle_journeys",
            "templated": true
        },
        {
            "href": "http://localhost:5000/v1/coverage/navitia/vehicle_journeys",
            "type": "first",
            "templated": false
        }
    ],
    "feed_publishers": [
        {
            "url": "",
            "id": "navitia",
            "license": "",
            "name": ""
        }
    ]
}"""
