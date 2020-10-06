# coding=utf-8

#  Copyright (c) 2001, Canal TP and/or its affiliates. All rights reserved.
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
    "vehicle_journeys/?depth=2&since=20150921T133000Z&headsign=JOHN&show_codes=true&until=20150921T173900Z"
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
            "name": "JOHN",
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
                    "arrival_time": "172100",
                    "utc_arrival_time": "152100",
                    "utc_departure_time": "152100",
                    "journey_pattern_point": {
                        "id": "OCE:Train TER-85000109-87212027-1721:OCE:SP:Train TER-87212027:0"
                    },
                    "headsign": "JOHN",
                    "departure_time": "172100",
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
                    "arrival_time": "173800",
                    "utc_arrival_time": "153800",
                    "utc_departure_time": "154000",
                    "journey_pattern_point": {
                        "id": "OCE:Train TER-85000109-87212027-1721:OCE:SP:Train TER-87214056:1"
                    },
                    "headsign": "JOHN",
                    "departure_time": "174000",
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
                    "arrival_time": "175100",
                    "utc_arrival_time": "155100",
                    "utc_departure_time": "155300",
                    "journey_pattern_point": {
                        "id": "OCE:Train TER-85000109-87212027-1721:OCE:SP:Train TER-87182014:2"
                    },
                    "headsign": "JOHN",
                    "departure_time": "175300",
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
                    "arrival_time": "181400",
                    "utc_arrival_time": "161400",
                    "utc_departure_time": "161600",
                    "journey_pattern_point": {
                        "id": "OCE:Train TER-85000109-87212027-1721:OCE:SP:Train TER-87182063:3"
                    },
                    "headsign": "JOHN",
                    "departure_time": "181600",
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
                    "arrival_time": "183000",
                    "utc_arrival_time": "163000",
                    "utc_departure_time": "163100",
                    "journey_pattern_point": {
                        "id": "OCE:Train TER-85000109-87212027-1721:OCE:SP:Train TER-87182139:4"
                    },
                    "headsign": "JOHN",
                    "departure_time": "183100",
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
                    "arrival_time": "183900",
                    "utc_arrival_time": "163900",
                    "utc_departure_time": "163900",
                    "journey_pattern_point": {
                        "id": "OCE:Train TER-85000109-87212027-1721:OCE:SP:Train TER-85000109:5"
                    },
                    "headsign": "JOHN",
                    "departure_time": "183900",
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
        },
        {
            "codes": [
                {
                    "type": "external_code",
                    "value": "OCESN006113F02009"
                }
            ],
            "name": "JOHNDOE",
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
                    "arrival_time": "153700",
                    "utc_arrival_time": "133700",
                    "utc_departure_time": "133700",
                    "journey_pattern_point": {
                        "id": "OCE:TGV-87751008-87686006-4066:OCE:SP:TGV-87686006:0"
                    },
                    "headsign": "JOHNDOE",
                    "departure_time": "153700",
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
                    "arrival_time": "182100",
                    "utc_arrival_time": "162100",
                    "utc_departure_time": "162400",
                    "journey_pattern_point": {
                        "id": "OCE:TGV-87751008-87686006-4066:OCE:SP:TGV-87318964:1"
                    },
                    "headsign": "JOHNDOE",
                    "departure_time": "182400",
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
                    "arrival_time": "184300",
                    "utc_arrival_time": "164300",
                    "utc_departure_time": "164600",
                    "journey_pattern_point": {
                        "id": "OCE:TGV-87751008-87686006-4066:OCE:SP:TGV-87319012:2"
                    },
                    "headsign": "JOHNDOE",
                    "departure_time": "184600",
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
                    "arrival_time": "190300",
                    "utc_arrival_time": "170300",
                    "utc_departure_time": "170300",
                    "journey_pattern_point": {
                        "id": "OCE:TGV-87751008-87686006-4066:OCE:SP:TGV-87751008:3"
                    },
                    "headsign": "JOHNDOE",
                    "departure_time": "190300",
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
        "items_on_page": 2,
        "items_per_page": 25,
        "total_result": 2
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
