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
    "vehicle_journeys/?depth=2&since=20170318T120500Z&headsign=840427&show_codes=true&until=20170318T161600Z"
]

response.response_code = 200

response.json_response = """
{
    "links": [
        {
            "href": "https://api.sncf.com/v1/coverage/sncf/stop_points/{stop_point.id}",
            "rel": "stop_points",
            "templated": true,
            "type": "stop_point"
        },
        {
            "href": "https://api.sncf.com/v1/coverage/sncf/stop_areas/{stop_area.id}",
            "rel": "stop_areas",
            "templated": true,
            "type": "stop_area"
        },
        {
            "href": "https://api.sncf.com/v1/coverage/sncf/journey_patterns/{journey_pattern.id}",
            "rel": "journey_patterns",
            "templated": true,
            "type": "journey_pattern"
        },
        {
            "href": "https://api.sncf.com/v1/coverage/sncf/disruptions/{disruptions.id}",
            "rel": "disruptions",
            "templated": true,
            "type": "disruptions"
        },
        {
            "href": "https://api.sncf.com/v1/coverage/sncf/routes/{route.id}",
            "rel": "routes",
            "templated": true,
            "type": "route"
        },
        {
            "href": "https://api.sncf.com/v1/coverage/sncf/disruptions/{disruption.id}",
            "rel": "disruptions",
            "templated": true,
            "type": "disruption"
        },
        {
            "href": "https://api.sncf.com/v1/coverage/sncf/journey_pattern_points/{journey_pattern_point.id}",
            "rel": "journey_pattern_points",
            "templated": true,
            "type": "journey_pattern_point"
        },
        {
            "href": "https://api.sncf.com/v1/coverage/sncf/vehicle_journeys/{vehicle_journeys.id}",
            "rel": "vehicle_journeys",
            "templated": true,
            "type": "vehicle_journeys"
        },
        {
            "href": "https://api.sncf.com/v1/coverage/sncf/trips/{trip.id}",
            "rel": "trips",
            "templated": true,
            "type": "trip"
        },
        {
            "href": "https://api.sncf.com/v1/coverage/sncf/vehicle_journeys?depth=2&since=20170317T120000&until=20170320T220000&headsign=840426",
            "templated": false,
            "type": "first"
        }
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
                            "begin": "20170318",
                            "end": "20170326"
                        }
                    ],
                    "week_pattern": {
                        "friday": true,
                        "monday": true,
                        "saturday": true,
                        "sunday": true,
                        "thursday": true,
                        "tuesday": true,
                        "wednesday": true
                    }
                }
            ],
            "disruptions": [
                {
                    "id": "ec9eba78-882c-4cc0-a168-283c271830a1",
                    "internal": true,
                    "rel": "disruptions",
                    "templated": false,
                    "type": "disruption"
                },
                {
                    "id": "110e5ec5-a081-4174-ac79-fcabe513ffda",
                    "internal": true,
                    "rel": "disruptions",
                    "templated": false,
                    "type": "disruption"
                }
            ],
            "id": "vehicle_journey:OCE:SN840427F03001_dst_1",
            "journey_pattern": {
                "id": "journey_pattern:8882",
                "name": "journey_pattern:8882",
                "route": {
                    "direction": {
                        "embedded_type": "stop_area",
                        "id": "stop_area:OCE:SA:87118000",
                        "name": "Troyes (Troyes)",
                        "quality": 0,
                        "stop_area": {
                            "codes": [
                                {
                                    "type": "CR-CI-CH",
                                    "value": "0087-118000-BV"
                                }
                            ],
                            "coord": {
                                "lat": "48.295018",
                                "lon": "4.065398"
                            },
                            "id": "stop_area:OCE:SA:87118000",
                            "label": "Troyes (Troyes)",
                            "links": [],
                            "name": "Troyes",
                            "timezone": "Europe/Paris"
                        }
                    },
                    "direction_type": "",
                    "geojson": {
                        "coordinates": [],
                        "type": "MultiLineString"
                    },
                    "id": "route:OCE:SN-TrainTER-87713040-87118000",
                    "is_frequence": "False",
                    "links": [],
                    "name": "Dijon-Ville vers Troyes (Train TER)"
                }
            },
            "name": "840427",
            "stop_times": [
                {
                    "arrival_time": "140500",
                    "departure_time": "140500",
                    "utc_arrival_time": "130500",
                    "utc_departure_time": "130500",
                    "headsign": "840427",
                    "journey_pattern_point": {
                        "id": "journey_pattern_point:83888"
                    },
                    "stop_point": {
                        "administrative_regions": [
                            {
                                "coord": {
                                    "lat": "47.321579",
                                    "lon": "5.04147"
                                },
                                "id": "admin:fr:21231",
                                "insee": "21231",
                                "label": "Dijon (21000)",
                                "level": 8,
                                "name": "Dijon",
                                "zip_code": "21000"
                            }
                        ],
                        "coord": {
                            "lat": "47.323392",
                            "lon": "5.027278"
                        },
                        "equipments": [],
                        "id": "stop_point:OCE:SP:TrainTER-87713040",
                        "label": "Dijon-Ville (Dijon)",
                        "links": [],
                        "name": "Dijon-Ville",
                        "stop_area": {
                            "codes": [
                                {
                                    "type": "CR-CI-CH",
                                    "value": "0087-713040-BV"
                                }
                            ],
                            "coord": {
                                "lat": "47.323392",
                                "lon": "5.027278"
                            },
                            "id": "stop_area:OCE:SA:87713040",
                            "label": "Dijon-Ville (Dijon)",
                            "links": [],
                            "name": "Dijon-Ville",
                            "timezone": "Europe/Paris"
                        }
                    }
                },
                {
                    "arrival_time": "145100",
                    "departure_time": "145300",
                    "utc_arrival_time": "135100",
                    "utc_departure_time": "135300",
                    "headsign": "840426",
                    "journey_pattern_point": {
                        "id": "journey_pattern_point:83889"
                    },
                    "stop_point": {
                        "administrative_regions": [
                            {
                                "coord": {
                                    "lat": "47.820599",
                                    "lon": "5.439705"
                                },
                                "id": "admin:fr:52155",
                                "insee": "52155",
                                "label": "Culmont (52600)",
                                "level": 8,
                                "name": "Culmont",
                                "zip_code": "52600"
                            }
                        ],
                        "coord": {
                            "lat": "47.810217",
                            "lon": "5.443217"
                        },
                        "equipments": [],
                        "id": "stop_point:OCE:SP:TrainTER-87142125",
                        "label": "Culmont-Chalindrey (Culmont)",
                        "links": [],
                        "name": "Culmont-Chalindrey",
                        "stop_area": {
                            "codes": [
                                {
                                    "type": "CR-CI-CH",
                                    "value": "0087-142125-BV"
                                }
                            ],
                            "coord": {
                                "lat": "47.810217",
                                "lon": "5.443217"
                            },
                            "id": "stop_area:OCE:SA:87142125",
                            "label": "Culmont-Chalindrey (Culmont)",
                            "links": [],
                            "name": "Culmont-Chalindrey",
                            "timezone": "Europe/Paris"
                        }
                    }
                },
                {
                    "arrival_time": "150200",
                    "departure_time": "150300",
                    "utc_arrival_time": "140200",
                    "utc_departure_time": "140300",
                    "headsign": "840426",
                    "journey_pattern_point": {
                        "id": "journey_pattern_point:83890"
                    },
                    "stop_point": {
                        "administrative_regions": [
                            {
                                "coord": {
                                    "lat": "47.865562",
                                    "lon": "5.331416"
                                },
                                "id": "admin:fr:52269",
                                "insee": "52269",
                                "label": "Langres (52200)",
                                "level": 8,
                                "name": "Langres",
                                "zip_code": "52200"
                            },
                            {
                                "coord": {
                                    "lat": "47.865562",
                                    "lon": "5.331416"
                                },
                                "id": "admin:fr:52269",
                                "insee": "52269",
                                "label": "Langres (52200)",
                                "level": 8,
                                "name": "Langres",
                                "zip_code": "52200"
                            }
                        ],
                        "coord": {
                            "lat": "47.877239",
                            "lon": "5.344682"
                        },
                        "equipments": [],
                        "id": "stop_point:OCE:SP:TrainTER-87142091",
                        "label": "Langres (Langres) (Langres)",
                        "links": [],
                        "name": "Langres",
                        "stop_area": {
                            "codes": [
                                {
                                    "type": "CR-CI-CH",
                                    "value": "0087-142091-BV"
                                }
                            ],
                            "coord": {
                                "lat": "47.877239",
                                "lon": "5.344682"
                            },
                            "id": "stop_area:OCE:SA:87142091",
                            "label": "Langres (Langres)",
                            "links": [],
                            "name": "Langres",
                            "timezone": "Europe/Paris"
                        }
                    }
                },
                {
                    "arrival_time": "152200",
                    "departure_time": "152400",
                    "utc_arrival_time": "142200",
                    "utc_departure_time": "142400",
                    "headsign": "840426",
                    "journey_pattern_point": {
                        "id": "journey_pattern_point:83891"
                    },
                    "stop_point": {
                        "administrative_regions": [
                            {
                                "coord": {
                                    "lat": "48.111881",
                                    "lon": "5.13945"
                                },
                                "id": "admin:fr:52121",
                                "insee": "52121",
                                "label": "Chaumont (52000)",
                                "level": 8,
                                "name": "Chaumont",
                                "zip_code": "52000"
                            }
                        ],
                        "coord": {
                            "lat": "48.109437",
                            "lon": "5.13445"
                        },
                        "equipments": [],
                        "id": "stop_point:OCE:SP:TrainTER-87142000",
                        "label": "Chaumont (Chaumont)",
                        "links": [],
                        "name": "Chaumont",
                        "stop_area": {
                            "codes": [
                                {
                                    "type": "CR-CI-CH",
                                    "value": "0087-142000-BV"
                                }
                            ],
                            "coord": {
                                "lat": "48.109437",
                                "lon": "5.13445"
                            },
                            "id": "stop_area:OCE:SA:87142000",
                            "label": "Chaumont (Chaumont)",
                            "links": [],
                            "name": "Chaumont",
                            "timezone": "Europe/Paris"
                        }
                    }
                },
                {
                    "arrival_time": "154400",
                    "departure_time": "154500",
                    "utc_arrival_time": "144400",
                    "utc_departure_time": "144500",
                    "headsign": "840426",
                    "journey_pattern_point": {
                        "id": "journey_pattern_point:83892"
                    },
                    "stop_point": {
                        "administrative_regions": [
                            {
                                "coord": {
                                    "lat": "48.233204",
                                    "lon": "4.705833"
                                },
                                "id": "admin:fr:10033",
                                "insee": "10033",
                                "label": "Bar-sur-Aube (10200)",
                                "level": 8,
                                "name": "Bar-sur-Aube",
                                "zip_code": "10200"
                            }
                        ],
                        "coord": {
                            "lat": "48.238534",
                            "lon": "4.706847"
                        },
                        "equipments": [],
                        "id": "stop_point:OCE:SP:TrainTER-87118299",
                        "label": "Bar-sur-Aube (Bar-sur-Aube)",
                        "links": [],
                        "name": "Bar-sur-Aube",
                        "stop_area": {
                            "codes": [
                                {
                                    "type": "CR-CI-CH",
                                    "value": "0087-118299-BV"
                                }
                            ],
                            "coord": {
                                "lat": "48.238534",
                                "lon": "4.706847"
                            },
                            "id": "stop_area:OCE:SA:87118299",
                            "label": "Bar-sur-Aube (Bar-sur-Aube)",
                            "links": [],
                            "name": "Bar-sur-Aube",
                            "timezone": "Europe/Paris"
                        }
                    }
                },
                {
                    "arrival_time": "155800",
                    "departure_time": "155900",
                    "utc_arrival_time": "145800",
                    "utc_departure_time": "145900",
                    "headsign": "840426",
                    "journey_pattern_point": {
                        "id": "journey_pattern_point:83893"
                    },
                    "stop_point": {
                        "administrative_regions": [
                            {
                                "coord": {
                                    "lat": "48.238426",
                                    "lon": "4.46662"
                                },
                                "id": "admin:fr:10401",
                                "insee": "10401",
                                "label": "Vendeuvre-sur-Barse (10140)",
                                "level": 8,
                                "name": "Vendeuvre-sur-Barse",
                                "zip_code": "10140"
                            }
                        ],
                        "coord": {
                            "lat": "48.240322",
                            "lon": "4.467197"
                        },
                        "equipments": [],
                        "id": "stop_point:OCE:SP:TrainTER-87118257",
                        "label": "Vendeuvre (Aube) (Vendeuvre-sur-Barse)",
                        "links": [],
                        "name": "Vendeuvre (Aube)",
                        "stop_area": {
                            "codes": [
                                {
                                    "type": "CR-CI-CH",
                                    "value": "0087-118257-BV"
                                }
                            ],
                            "coord": {
                                "lat": "48.240322",
                                "lon": "4.467197"
                            },
                            "id": "stop_area:OCE:SA:87118257",
                            "label": "Vendeuvre (Aube) (Vendeuvre-sur-Barse)",
                            "links": [],
                            "name": "Vendeuvre (Aube)",
                            "timezone": "Europe/Paris"
                        }
                    }
                },
                {
                    "arrival_time": "161600",
                    "departure_time": "161600",
                    "utc_arrival_time": "151600",
                    "utc_departure_time": "151600",
                    "headsign": "840426",
                    "journey_pattern_point": {
                        "id": "journey_pattern_point:83894"
                    },
                    "stop_point": {
                        "administrative_regions": [
                            {
                                "coord": {
                                    "lat": "48.297161",
                                    "lon": "4.074625"
                                },
                                "id": "admin:fr:10387",
                                "insee": "10387",
                                "label": "Troyes (10000)",
                                "level": 8,
                                "name": "Troyes",
                                "zip_code": "10000"
                            }
                        ],
                        "coord": {
                            "lat": "48.295018",
                            "lon": "4.065398"
                        },
                        "equipments": [],
                        "id": "stop_point:OCE:SP:TrainTER-87118000",
                        "label": "Troyes (Troyes)",
                        "links": [],
                        "name": "Troyes",
                        "stop_area": {
                            "codes": [
                                {
                                    "type": "CR-CI-CH",
                                    "value": "0087-118000-BV"
                                }
                            ],
                            "coord": {
                                "lat": "48.295018",
                                "lon": "4.065398"
                            },
                            "id": "stop_area:OCE:SA:87118000",
                            "label": "Troyes (Troyes)",
                            "links": [],
                            "name": "Troyes",
                            "timezone": "Europe/Paris"
                        }
                    }
                }
            ],
            "trip": {
                "id": "OCE:SN840427F03001",
                "name": "840427"
            },
            "validity_pattern": {
                "beginning_date": "20170317",
                "days": "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000111111110"
            }
        }
    ]
}

"""
