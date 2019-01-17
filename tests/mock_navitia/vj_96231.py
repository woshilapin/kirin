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

response = navitia_response.NavitiaResponse()

response.queries = [
    'vehicle_journeys/?depth=2&since=20150921T133000+0000&headsign=96231&show_codes=true&until=20150921T173900+0000',
    'vehicle_journeys/?depth=2&since=20150921T132000+0000&headsign=96231&show_codes=true&until=20150921T173900+0000'
]

response.response_code = 200

response.json_response = """{
    "vehicle_journeys": [
        {
            "codes": [
                {
                    "type": "external_code",
                    "value": "OCESN096231F01001"
                }
            ],
            "name": "96231",
            "journey_pattern": {
                "route": {
                    "direction": {
                        "embedded_type": "stop_area",
                        "quality": 0,
                        "stop_area": {
                            "codes": [
                                {
                                    "type": "CR-CI-CH",
                                    "value": "0087-187914-WS"
                                },
                                {
                                    "type": "external_code",
                                    "value": "OCE85000109"
                                }
                            ],
                            "name": "gare de Basel-SBB",
                            "links": [

                            ],
                            "coord": {
                                "lat": "47.547029",
                                "lon": "7.589551"
                            },
                            "label": "gare de Basel-SBB",
                            "timezone": "Europe/Paris",
                            "id": "stop_area:OCE:SA:85000109"
                        },
                        "name": "gare de Basel-SBB",
                        "id": "stop_area:OCE:SA:85000109"
                    },
                    "codes": [
                        {
                            "type": "external_code",
                            "value": "OCETrain TER-87212027-85000109-3"
                        }
                    ],
                    "name": "Strasbourg vers Basel-SBB",
                    "links": [

                    ],
                    "is_frequence": "false",
                    "geojson": {
                        "type": "MultiLineString",
                        "coordinates": [

                        ]
                    },
                    "id": "route:OCE:TrainTER-87212027-85000109-3"
                },
                "name": "gare de Basel-SBB",
                "id": "journey_pattern:OCE:TrainTER-85000109-87212027-1721"
            },
            "calendars": [
                {
                    "active_periods": [
                        {
                            "begin": "20150909",
                            "end": "20151010"
                        }
                    ],
                    "week_pattern": {
                        "monday": true,
                        "tuesday": true,
                        "friday": true,
                        "wednesday": true,
                        "thursday": true,
                        "sunday": false,
                        "saturday": false
                    }
                }
            ],
            "stop_times": [
                {
                    "utc_arrival_time": "152100",
                    "utc_departure_time": "152100",
                    "journey_pattern_point": {
                        "id": "OCE:Train TER-85000109-87212027-1721:OCE:SP:Train TER-87212027:0"
                    },
                    "headsign": "96231",
                    "stop_point": {
                        "codes": [
                            {
                                "type": "external_code",
                                "value": "OCETrain TER-87212027"
                            }
                        ],
                        "name": "gare de Strasbourg",
                        "links": [

                        ],
                        "coord": {
                            "lat": "48.585085",
                            "lon": "7.735595"
                        },
                        "label": "gare de Strasbourg",
                        "equipments": [

                        ],
                        "id": "stop_point:OCE:SP:TrainTER-87212027",
                        "stop_area": {
                            "codes": [
                                {
                                    "type": "CR-CI-CH",
                                    "value": "0087-212027-BV"
                                },
                                {
                                    "type": "external_code",
                                    "value": "OCE87212027"
                                }
                            ],
                            "name": "gare de Strasbourg",
                            "links": [

                            ],
                            "coord": {
                                "lat": "48.585085",
                                "lon": "7.735595"
                            },
                            "label": "gare de Strasbourg",
                            "timezone": "Europe/Paris",
                            "id": "stop_area:OCE:SA:87212027"
                        }
                    }
                },
                {
                    "utc_arrival_time": "153800",
                    "utc_departure_time": "154000",
                    "journey_pattern_point": {
                        "id": "OCE:Train TER-85000109-87212027-1721:OCE:SP:Train TER-87214056:1"
                    },
                    "headsign": "96231",
                    "stop_point": {
                        "codes": [
                            {
                                "type": "external_code",
                                "value": "OCETrain TER-87214056"
                            }
                        ],
                        "name": "gare de Sélestat",
                        "links": [

                        ],
                        "coord": {
                            "lat": "48.259942",
                            "lon": "7.443167"
                        },
                        "label": "gare de Sélestat",
                        "equipments": [

                        ],
                        "id": "stop_point:OCE:SP:TrainTER-87214056",
                        "stop_area": {
                            "codes": [
                                {
                                    "type": "CR-CI-CH",
                                    "value": "0087-214056-00"
                                },
                                {
                                    "type": "external_code",
                                    "value": "OCE87214056"
                                }
                            ],
                            "name": "gare de Sélestat",
                            "links": [

                            ],
                            "coord": {
                                "lat": "48.259942",
                                "lon": "7.443167"
                            },
                            "label": "gare de Sélestat",
                            "timezone": "Europe/Paris",
                            "id": "stop_area:OCE:SA:87214056"
                        }
                    }
                },
                {
                    "utc_arrival_time": "155100",
                    "utc_departure_time": "155300",
                    "journey_pattern_point": {
                        "id": "OCE:Train TER-85000109-87212027-1721:OCE:SP:Train TER-87182014:2"
                    },
                    "headsign": "96231",
                    "stop_point": {
                        "codes": [
                            {
                                "type": "external_code",
                                "value": "OCETrain TER-87182014"
                            }
                        ],
                        "name": "gare de Colmar",
                        "links": [

                        ],
                        "coord": {
                            "lat": "48.072345",
                            "lon": "7.34703"
                        },
                        "label": "gare de Colmar",
                        "equipments": [

                        ],
                        "id": "stop_point:OCE:SP:TrainTER-87182014",
                        "stop_area": {
                            "codes": [
                                {
                                    "type": "CR-CI-CH",
                                    "value": "0087-182014-BV"
                                },
                                {
                                    "type": "external_code",
                                    "value": "OCE87182014"
                                }
                            ],
                            "name": "gare de Colmar",
                            "links": [

                            ],
                            "coord": {
                                "lat": "48.072345",
                                "lon": "7.34703"
                            },
                            "label": "gare de Colmar",
                            "timezone": "Europe/Paris",
                            "id": "stop_area:OCE:SA:87182014"
                        }
                    }
                },
                {
                    "utc_arrival_time": "161400",
                    "utc_departure_time": "161600",
                    "journey_pattern_point": {
                        "id": "OCE:Train TER-85000109-87212027-1721:OCE:SP:Train TER-87182063:3"
                    },
                    "headsign": "96231",
                    "stop_point": {
                        "codes": [
                            {
                                "type": "external_code",
                                "value": "OCETrain TER-87182063"
                            }
                        ],
                        "name": "gare de Mulhouse",
                        "links": [

                        ],
                        "coord": {
                            "lat": "47.742295",
                            "lon": "7.342306"
                        },
                        "label": "gare de Mulhouse",
                        "equipments": [

                        ],
                        "id": "stop_point:OCE:SP:TrainTER-87182063",
                        "stop_area": {
                            "codes": [
                                {
                                    "type": "CR-CI-CH",
                                    "value": "0087-182063-BV"
                                },
                                {
                                    "type": "external_code",
                                    "value": "OCE87182063"
                                }
                            ],
                            "name": "gare de Mulhouse",
                            "links": [

                            ],
                            "coord": {
                                "lat": "47.742295",
                                "lon": "7.342306"
                            },
                            "label": "gare de Mulhouse",
                            "timezone": "Europe/Paris",
                            "id": "stop_area:OCE:SA:87182063"
                        }
                    }
                },
                {
                    "utc_arrival_time": "163000",
                    "utc_departure_time": "163100",
                    "journey_pattern_point": {
                        "id": "OCE:Train TER-85000109-87212027-1721:OCE:SP:Train TER-87182139:4"
                    },
                    "headsign": "96231",
                    "stop_point": {
                        "codes": [
                            {
                                "type": "external_code",
                                "value": "OCETrain TER-87182139"
                            }
                        ],
                        "name": "gare de St-Louis (Haut-Rhin)",
                        "links": [

                        ],
                        "coord": {
                            "lat": "47.590479",
                            "lon": "7.556179"
                        },
                        "label": "gare de St-Louis (Haut-Rhin)",
                        "equipments": [

                        ],
                        "id": "stop_point:OCE:SP:TrainTER-87182139",
                        "stop_area": {
                            "codes": [
                                {
                                    "type": "CR-CI-CH",
                                    "value": "0087-182139-BV"
                                },
                                {
                                    "type": "external_code",
                                    "value": "OCE87182139"
                                }
                            ],
                            "name": "gare de St-Louis (Haut-Rhin)",
                            "links": [

                            ],
                            "coord": {
                                "lat": "47.590479",
                                "lon": "7.556179"
                            },
                            "label": "gare de St-Louis (Haut-Rhin)",
                            "timezone": "Europe/Paris",
                            "id": "stop_area:OCE:SA:87182139"
                        }
                    }
                },
                {
                    "utc_arrival_time": "163900",
                    "utc_departure_time": "163900",
                    "journey_pattern_point": {
                        "id": "OCE:Train TER-85000109-87212027-1721:OCE:SP:Train TER-85000109:5"
                    },
                    "headsign": "96231",
                    "stop_point": {
                        "codes": [
                            {
                                "type": "external_code",
                                "value": "OCETrain TER-85000109"
                            }
                        ],
                        "name": "gare de Basel-SBB",
                        "links": [

                        ],
                        "coord": {
                            "lat": "47.547029",
                            "lon": "7.589551"
                        },
                        "label": "gare de Basel-SBB",
                        "equipments": [

                        ],
                        "id": "stop_point:OCE:SP:TrainTER-85000109",
                        "stop_area": {
                            "codes": [
                                {
                                    "type": "CR-CI-CH",
                                    "value": "0087-187914-WS"
                                },
                                {
                                    "type": "external_code",
                                    "value": "OCE85000109"
                                }
                            ],
                            "name": "gare de Basel-SBB",
                            "links": [

                            ],
                            "coord": {
                                "lat": "47.547029",
                                "lon": "7.589551"
                            },
                            "label": "gare de Basel-SBB",
                            "timezone": "Europe/Paris",
                            "id": "stop_area:OCE:SA:85000109"
                        }
                    }
                }
            ],
            "validity_pattern": {
                "beginning_date": "20150908",
                "days": "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000011111001111100111110011111001110"
            },
            "id": "vehicle_journey:OCETrainTER-87212027-85000109-3:11859",
            "trip": {"id": "trip:OCETrainTER-87212027-85000109-3:11859"}
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
            "href": "http://localhost:5000/v1/coverage/default/routes/{route.id}",
            "type": "route",
            "rel": "routes",
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
            "href": "http://localhost:5000/v1/coverage/default/vehicle_journeys",
            "type": "first",
            "templated": false
        }
    ],
    "feed_publishers": [
        {
            "url": "",
            "id": "PaysDeLaLoire",
            "license": "",
            "name": ""
        }
    ]
}"""
