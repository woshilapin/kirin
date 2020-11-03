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
    'vehicle_journeys/?filter=vehicle_journey.has_code("rt_piv", "2020-10-29:841252:1187:rail:regionalRail:FERRE")&depth=2&show_codes=true'
]

response.response_code = 200

response.json_response = """{
   "pagination":{
      "start_page":0,
      "items_on_page":1,
      "items_per_page":25,
      "total_result":1
   },
   "links":[
      {
         "href":"http:\/\/navitia2-ws.ctp.dev.canaltp.fr\/v1\/coverage\/sncf\/stop_points\/{stop_point.id}",
         "type":"stop_point",
         "rel":"stop_points",
         "templated":true
      },
      {
         "href":"http:\/\/navitia2-ws.ctp.dev.canaltp.fr\/v1\/coverage\/sncf\/stop_areas\/{stop_area.id}",
         "type":"stop_area",
         "rel":"stop_areas",
         "templated":true
      },
      {
         "href":"http:\/\/navitia2-ws.ctp.dev.canaltp.fr\/v1\/coverage\/sncf\/journey_patterns\/{journey_pattern.id}",
         "type":"journey_pattern",
         "rel":"journey_patterns",
         "templated":true
      },
      {
         "href":"http:\/\/navitia2-ws.ctp.dev.canaltp.fr\/v1\/coverage\/sncf\/routes\/{route.id}",
         "type":"route",
         "rel":"routes",
         "templated":true
      },
      {
         "href":"http:\/\/navitia2-ws.ctp.dev.canaltp.fr\/v1\/coverage\/sncf\/journey_pattern_points\/{journey_pattern_point.id}",
         "type":"journey_pattern_point",
         "rel":"journey_pattern_points",
         "templated":true
      },
      {
         "href":"http:\/\/navitia2-ws.ctp.dev.canaltp.fr\/v1\/coverage\/sncf\/vehicle_journeys\/{vehicle_journeys.id}",
         "type":"vehicle_journeys",
         "rel":"vehicle_journeys",
         "templated":true
      },
      {
         "href":"http:\/\/navitia2-ws.ctp.dev.canaltp.fr\/v1\/coverage\/sncf\/trips\/{trip.id}",
         "type":"trip",
         "rel":"trips",
         "templated":true
      },
      {
         "href":"http:\/\/navitia2-ws.ctp.dev.canaltp.fr\/v1\/coverage\/sncf\/vehicle_journeys?filter=vehicle_journey.has_code%28%22rt_piv%22%2C%222020-10-29%3A841252%3A1187%3Arail%3AregionalRail%3AFERRE%22%29&depth=2&show_codes=true",
         "type":"first",
         "templated":false
      }
   ],
   "disruptions":[

   ],
   "feed_publishers":[
      {
         "url":"",
         "id":"sncf",
         "license":"Private (unspecified)",
         "name":"PIV Pr\u00e9-prod"
      }
   ],
   "context":{
      "timezone":"Europe\/Paris",
      "current_datetime":"20201029T165920"
   },
   "vehicle_journeys":[
      {
         "codes":[
            {
               "type":"rt_piv",
               "value":"2020-10-29:841252:1187:rail:regionalRail:FERRE"
            },
            {
               "type":"source",
               "value":"ff4ffde8ee19ec1f024c2725ae603c2d"
            }
         ],
         "name":"841252",
         "journey_pattern":{
            "route":{
               "direction":{
                  "embedded_type":"stop_area",
                  "stop_area":{
                     "codes":[
                        {
                           "type":"source",
                           "value":"87343004"
                        }
                     ],
                     "name":"Valenciennes",
                     "links":[

                     ],
                     "coord":{
                        "lat":"50.363183",
                        "lon":"3.517128"
                     },
                     "label":"Valenciennes (Valenciennes)",
                     "timezone":"Europe\/Paris",
                     "id":"stop_area:PIVPP:87343004"
                  },
                  "quality":0,
                  "name":"Valenciennes (Valenciennes)",
                  "id":"stop_area:PIVPP:87343004"
               },
               "name":"Lille Flandres - Valenciennes",
               "links":[

               ],
               "is_frequence":"False",
               "geojson":{
                  "type":"MultiLineString",
                  "coordinates":[

                  ]
               },
               "direction_type":"forward",
               "id":"route:PIVPP:FR:Line::A7CE67FF-B9EA-48CF-9123-EBB30BD8D049:"
            },
            "id":"journey_pattern:2207",
            "name":"journey_pattern:2207"
         },
         "disruptions":[

         ],
         "calendars":[
            {
               "active_periods":[
                  {
                     "begin":"20201029",
                     "end":"20201030"
                  }
               ],
               "week_pattern":{
                  "monday":false,
                  "tuesday":false,
                  "friday":false,
                  "wednesday":false,
                  "thursday":true,
                  "sunday":false,
                  "saturday":false
               }
            }
         ],
         "stop_times":[
            {
               "stop_point":{
                  "name":"Valenciennes",
                  "links":[

                  ],
                  "coord":{
                     "lat":"50.363183",
                     "lon":"3.517128"
                  },
                  "label":"Valenciennes (Valenciennes)",
                  "equipments":[

                  ],
                  "administrative_regions":[
                     {
                        "insee":"59606",
                        "name":"Valenciennes",
                        "level":8,
                        "coord":{
                           "lat":"50.3579317",
                           "lon":"3.5234846"
                        },
                        "label":"Valenciennes (59300)",
                        "id":"admin:fr:59606",
                        "zip_code":"59300"
                     }
                  ],
                  "id":"stop_point:PIVPP:87343004:Train",
                  "stop_area":{
                     "codes":[
                        {
                           "type":"source",
                           "value":"87343004"
                        }
                     ],
                     "name":"Valenciennes",
                     "links":[

                     ],
                     "coord":{
                        "lat":"50.363183",
                        "lon":"3.517128"
                     },
                     "label":"Valenciennes (Valenciennes)",
                     "timezone":"Europe\/Paris",
                     "id":"stop_area:PIVPP:87343004"
                  }
               },
               "utc_arrival_time":"200500",
               "utc_departure_time":"200500",
               "headsign":"PIVPP:2020-10-29:841252:1187:Train",
               "arrival_time":"210500",
               "journey_pattern_point":{
                  "id":"journey_pattern_point:22550"
               },
               "drop_off_allowed":false,
               "pickup_allowed":true,
               "departure_time":"210500"
            },
            {
               "stop_point":{
                  "name":"St-Amand-les-Eaux",
                  "links":[

                  ],
                  "coord":{
                     "lat":"50.44323",
                     "lon":"3.419355"
                  },
                  "label":"St-Amand-les-Eaux (Saint-Amand-les-Eaux)",
                  "equipments":[

                  ],
                  "administrative_regions":[
                     {
                        "insee":"59526",
                        "name":"Saint-Amand-les-Eaux",
                        "level":8,
                        "coord":{
                           "lat":"50.4491519",
                           "lon":"3.4281142"
                        },
                        "label":"Saint-Amand-les-Eaux (59230)",
                        "id":"admin:fr:59526",
                        "zip_code":"59230"
                     }
                  ],
                  "id":"stop_point:PIVPP:87343103:Train",
                  "stop_area":{
                     "codes":[
                        {
                           "type":"source",
                           "value":"87343103"
                        }
                     ],
                     "name":"St-Amand-les-Eaux",
                     "links":[

                     ],
                     "coord":{
                        "lat":"50.44323",
                        "lon":"3.419355"
                     },
                     "label":"St-Amand-les-Eaux (Saint-Amand-les-Eaux)",
                     "timezone":"Europe\/Paris",
                     "id":"stop_area:PIVPP:87343103"
                  }
               },
               "utc_arrival_time":"201400",
               "utc_departure_time":"201500",
               "headsign":"PIVPP:2020-10-29:841252:1187:Train",
               "arrival_time":"211400",
               "journey_pattern_point":{
                  "id":"journey_pattern_point:22551"
               },
               "drop_off_allowed":true,
               "pickup_allowed":true,
               "departure_time":"211500"
            },
            {
               "stop_point":{
                  "name":"Rosult",
                  "links":[

                  ],
                  "coord":{
                     "lat":"50.456419",
                     "lon":"3.348858"
                  },
                  "label":"Rosult (Rosult)",
                  "equipments":[

                  ],
                  "administrative_regions":[
                     {
                        "insee":"59511",
                        "name":"Rosult",
                        "level":8,
                        "coord":{
                           "lat":"50.4506089",
                           "lon":"3.3648063"
                        },
                        "label":"Rosult (59230)",
                        "id":"admin:fr:59511",
                        "zip_code":"59230"
                     }
                  ],
                  "id":"stop_point:PIVPP:87286567:Train",
                  "stop_area":{
                     "codes":[
                        {
                           "type":"source",
                           "value":"87286567"
                        }
                     ],
                     "name":"Rosult",
                     "links":[

                     ],
                     "coord":{
                        "lat":"50.456419",
                        "lon":"3.348858"
                     },
                     "label":"Rosult (Rosult)",
                     "timezone":"Europe\/Paris",
                     "id":"stop_area:PIVPP:87286567"
                  }
               },
               "utc_arrival_time":"201900",
               "utc_departure_time":"202000",
               "headsign":"PIVPP:2020-10-29:841252:1187:Train",
               "arrival_time":"211900",
               "journey_pattern_point":{
                  "id":"journey_pattern_point:22552"
               },
               "drop_off_allowed":true,
               "pickup_allowed":true,
               "departure_time":"212000"
            },
            {
               "stop_point":{
                  "name":"Landas",
                  "links":[

                  ],
                  "coord":{
                     "lat":"50.468593",
                     "lon":"3.290592"
                  },
                  "label":"Landas (Landas)",
                  "equipments":[

                  ],
                  "administrative_regions":[
                     {
                        "insee":"59330",
                        "name":"Landas",
                        "level":8,
                        "coord":{
                           "lat":"50.4736312",
                           "lon":"3.3012971"
                        },
                        "label":"Landas (59310)",
                        "id":"admin:fr:59330",
                        "zip_code":"59310"
                     }
                  ],
                  "id":"stop_point:PIVPP:87286575:Train",
                  "stop_area":{
                     "codes":[
                        {
                           "type":"source",
                           "value":"87286575"
                        }
                     ],
                     "name":"Landas",
                     "links":[

                     ],
                     "coord":{
                        "lat":"50.468593",
                        "lon":"3.290592"
                     },
                     "label":"Landas (Landas)",
                     "timezone":"Europe\/Paris",
                     "id":"stop_area:PIVPP:87286575"
                  }
               },
               "utc_arrival_time":"202400",
               "utc_departure_time":"202500",
               "headsign":"PIVPP:2020-10-29:841252:1187:Train",
               "arrival_time":"212400",
               "journey_pattern_point":{
                  "id":"journey_pattern_point:22553"
               },
               "drop_off_allowed":true,
               "pickup_allowed":true,
               "departure_time":"212500"
            },
            {
               "stop_point":{
                  "name":"Orchies",
                  "links":[

                  ],
                  "coord":{
                     "lat":"50.477047",
                     "lon":"3.24888"
                  },
                  "label":"Orchies (Orchies)",
                  "equipments":[

                  ],
                  "administrative_regions":[
                     {
                        "insee":"59449",
                        "name":"Orchies",
                        "level":8,
                        "coord":{
                           "lat":"50.4745024",
                           "lon":"3.2425313"
                        },
                        "label":"Orchies (59310)",
                        "id":"admin:fr:59449",
                        "zip_code":"59310"
                     }
                  ],
                  "id":"stop_point:PIVPP:87286583:Train",
                  "stop_area":{
                     "codes":[
                        {
                           "type":"source",
                           "value":"87286583"
                        }
                     ],
                     "name":"Orchies",
                     "links":[

                     ],
                     "coord":{
                        "lat":"50.477047",
                        "lon":"3.24888"
                     },
                     "label":"Orchies (Orchies)",
                     "timezone":"Europe\/Paris",
                     "id":"stop_area:PIVPP:87286583"
                  }
               },
               "utc_arrival_time":"202730",
               "utc_departure_time":"202830",
               "headsign":"PIVPP:2020-10-29:841252:1187:Train",
               "arrival_time":"212730",
               "journey_pattern_point":{
                  "id":"journey_pattern_point:22554"
               },
               "drop_off_allowed":true,
               "pickup_allowed":true,
               "departure_time":"212830"
            },
            {
               "stop_point":{
                  "name":"Templeuve",
                  "links":[

                  ],
                  "coord":{
                     "lat":"50.528681",
                     "lon":"3.175601"
                  },
                  "label":"Templeuve (Templeuve-en-P\u00e9v\u00e8le)",
                  "equipments":[

                  ],
                  "administrative_regions":[
                     {
                        "insee":"59586",
                        "name":"Templeuve-en-P\u00e9v\u00e8le",
                        "level":8,
                        "coord":{
                           "lat":"50.5326276",
                           "lon":"3.1740541"
                        },
                        "label":"Templeuve-en-P\u00e9v\u00e8le (59242)",
                        "id":"admin:fr:59586",
                        "zip_code":"59242"
                     }
                  ],
                  "id":"stop_point:PIVPP:87286625:Train",
                  "stop_area":{
                     "codes":[
                        {
                           "type":"source",
                           "value":"87286625"
                        }
                     ],
                     "name":"Templeuve",
                     "links":[

                     ],
                     "coord":{
                        "lat":"50.528681",
                        "lon":"3.175601"
                     },
                     "label":"Templeuve (Templeuve-en-P\u00e9v\u00e8le)",
                     "timezone":"Europe\/Paris",
                     "id":"stop_area:PIVPP:87286625"
                  }
               },
               "utc_arrival_time":"203400",
               "utc_departure_time":"203500",
               "headsign":"PIVPP:2020-10-29:841252:1187:Train",
               "arrival_time":"213400",
               "journey_pattern_point":{
                  "id":"journey_pattern_point:22555"
               },
               "drop_off_allowed":true,
               "pickup_allowed":true,
               "departure_time":"213500"
            },
            {
               "stop_point":{
                  "name":"Fretin (Nord)",
                  "links":[

                  ],
                  "coord":{
                     "lat":"50.559844",
                     "lon":"3.149519"
                  },
                  "label":"Fretin (Nord) (Fretin)",
                  "equipments":[

                  ],
                  "administrative_regions":[
                     {
                        "insee":"59256",
                        "name":"Fretin",
                        "level":8,
                        "coord":{
                           "lat":"50.565",
                           "lon":"3.13244"
                        },
                        "label":"Fretin (59273)",
                        "id":"admin:fr:59256",
                        "zip_code":"59273"
                     }
                  ],
                  "id":"stop_point:PIVPP:87286641:Train",
                  "stop_area":{
                     "codes":[
                        {
                           "type":"source",
                           "value":"87286641"
                        }
                     ],
                     "name":"Fretin (Nord)",
                     "links":[

                     ],
                     "coord":{
                        "lat":"50.559844",
                        "lon":"3.149519"
                     },
                     "label":"Fretin (Nord) (Fretin)",
                     "timezone":"Europe\/Paris",
                     "id":"stop_area:PIVPP:87286641"
                  }
               },
               "utc_arrival_time":"203900",
               "utc_departure_time":"204000",
               "headsign":"PIVPP:2020-10-29:841252:1187:Train",
               "arrival_time":"213900",
               "journey_pattern_point":{
                  "id":"journey_pattern_point:22556"
               },
               "drop_off_allowed":true,
               "pickup_allowed":true,
               "departure_time":"214000"
            },
            {
               "stop_point":{
                  "name":"Lesquin",
                  "links":[

                  ],
                  "coord":{
                     "lat":"50.590703",
                     "lon":"3.117706"
                  },
                  "label":"Lesquin (Lesquin)",
                  "equipments":[

                  ],
                  "administrative_regions":[
                     {
                        "insee":"59343",
                        "name":"Lesquin",
                        "level":8,
                        "coord":{
                           "lat":"50.5888",
                           "lon":"3.10997"
                        },
                        "label":"Lesquin (59810)",
                        "id":"admin:fr:59343",
                        "zip_code":"59810"
                     }
                  ],
                  "id":"stop_point:PIVPP:87286849:Train",
                  "stop_area":{
                     "codes":[
                        {
                           "type":"source",
                           "value":"87286849"
                        }
                     ],
                     "name":"Lesquin",
                     "links":[

                     ],
                     "coord":{
                        "lat":"50.590703",
                        "lon":"3.117706"
                     },
                     "label":"Lesquin (Lesquin)",
                     "timezone":"Europe\/Paris",
                     "id":"stop_area:PIVPP:87286849"
                  }
               },
               "utc_arrival_time":"204300",
               "utc_departure_time":"204400",
               "headsign":"PIVPP:2020-10-29:841252:1187:Train",
               "arrival_time":"214300",
               "journey_pattern_point":{
                  "id":"journey_pattern_point:22557"
               },
               "drop_off_allowed":true,
               "pickup_allowed":true,
               "departure_time":"214400"
            },
            {
               "stop_point":{
                  "name":"Lille Flandres",
                  "links":[

                  ],
                  "coord":{
                     "lat":"50.636201",
                     "lon":"3.071023"
                  },
                  "label":"Lille Flandres (Lille)",
                  "equipments":[

                  ],
                  "administrative_regions":[
                     {
                        "insee":"59350",
                        "name":"Lille",
                        "level":8,
                        "coord":{
                           "lat":"50.6365654",
                           "lon":"3.0635282"
                        },
                        "label":"Lille (59000-59800)",
                        "id":"admin:fr:59350",
                        "zip_code":"59000;59800"
                     }
                  ],
                  "id":"stop_point:PIVPP:87286005:Train",
                  "stop_area":{
                     "codes":[
                        {
                           "type":"source",
                           "value":"87286005"
                        }
                     ],
                     "name":"Lille Flandres",
                     "links":[

                     ],
                     "coord":{
                        "lat":"50.636201",
                        "lon":"3.071023"
                     },
                     "label":"Lille Flandres (Lille)",
                     "timezone":"Europe\/Paris",
                     "id":"stop_area:PIVPP:87286005"
                  }
               },
               "utc_arrival_time":"205100",
               "utc_departure_time":"205100",
               "headsign":"PIVPP:2020-10-29:841252:1187:Train",
               "arrival_time":"215100",
               "journey_pattern_point":{
                  "id":"journey_pattern_point:22558"
               },
               "drop_off_allowed":true,
               "pickup_allowed":false,
               "departure_time":"215100"
            }
         ],
         "validity_pattern":{
            "beginning_date":"20201027",
            "days":"000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100"
         },
         "headsign":"PIVPP:2020-10-29:841252:1187:Train",
         "id":"vehicle_journey:PIVPP:2020-10-29:841252:1187:Train",
         "trip":{
            "id":"PIVPP:2020-10-29:841252:1187:Train",
            "name":"841252"
         }
      }
   ]
}"""
