# coding=utf-8
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
import navitia_response
from __future__ import absolute_import, print_function, unicode_literals, division

response = navitia_response.NavitiaResponse()

response.queries = [
    "vehicle_journeys/?depth=2&since=20181102T085400+0000&headsign=870154&show_codes=true&until=20181102T131500+0000"
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
         "href":"http:\/\/navitia2-ws.ctp.customer.canaltp.fr\/v1\/coverage\/sncf\/stop_points\/{stop_point.id}",
         "type":"stop_point",
         "rel":"stop_points",
         "templated":true
      },
      {
         "href":"http:\/\/navitia2-ws.ctp.customer.canaltp.fr\/v1\/coverage\/sncf\/stop_areas\/{stop_area.id}",
         "type":"stop_area",
         "rel":"stop_areas",
         "templated":true
      },
      {
         "href":"http:\/\/navitia2-ws.ctp.customer.canaltp.fr\/v1\/coverage\/sncf\/journey_patterns\/{journey_pattern.id}",
         "type":"journey_pattern",
         "rel":"journey_patterns",
         "templated":true
      },
      {
         "href":"http:\/\/navitia2-ws.ctp.customer.canaltp.fr\/v1\/coverage\/sncf\/routes\/{route.id}",
         "type":"route",
         "rel":"routes",
         "templated":true
      },
      {
         "href":"http:\/\/navitia2-ws.ctp.customer.canaltp.fr\/v1\/coverage\/sncf\/journey_pattern_points\/{journey_pattern_point.id}",
         "type":"journey_pattern_point",
         "rel":"journey_pattern_points",
         "templated":true
      },
      {
         "href":"http:\/\/navitia2-ws.ctp.customer.canaltp.fr\/v1\/coverage\/sncf\/vehicle_journeys\/{vehicle_journeys.id}",
         "type":"vehicle_journeys",
         "rel":"vehicle_journeys",
         "templated":true
      },
      {
         "href":"http:\/\/navitia2-ws.ctp.customer.canaltp.fr\/v1\/coverage\/sncf\/trips\/{trip.id}",
         "type":"trip",
         "rel":"trips",
         "templated":true
      },
      {
         "href":"http:\/\/navitia2-ws.ctp.customer.canaltp.fr\/v1\/coverage\/sncf\/vehicle_journeys?depth=2&since=20181102T095400&until=20181102T141500&headsign=870154",
         "type":"first",
         "templated":false
      }
   ],
   "disruptions":[

   ],
   "feed_publishers":[

   ],
   "context":{
      "timezone":"Europe\/Paris",
      "current_datetime":"20181010T163752"
   },
   "vehicle_journeys":[
      {
         "codes":[

         ],
         "name":"870154",
         "journey_pattern":{
            "route":{
               "direction":{
                  "embedded_type":"stop_area",
                  "stop_area":{
                     "codes":[
                        {
                           "type":"CR-CI-CH",
                           "value":"0087-594002-BV"
                        },
                        {
                           "type":"UIC8",
                           "value":"87594002"
                        },
                        {
                           "type":"external_code",
                           "value":"OCE87594002"
                        }
                     ],
                     "name":"Brive-la-Gaillarde",
                     "links":[

                     ],
                     "coord":{
                        "lat":"45.152554",
                        "lon":"1.528616"
                     },
                     "label":"Brive-la-Gaillarde (Brive-la-Gaillarde)",
                     "timezone":"Europe\/Paris",
                     "id":"stop_area:OCE:SA:87594002"
                  },
                  "quality":0,
                  "name":"Brive-la-Gaillarde (Brive-la-Gaillarde)",
                  "id":"stop_area:OCE:SA:87594002"
               },
               "name":"Rodez vers Brive-la-Gaillarde (Train TER)",
               "links":[

               ],
               "is_frequence":"False",
               "geojson":{
                  "type":"MultiLineString",
                  "coordinates":[

                  ]
               },
               "direction_type":"backward",
               "id":"route:OCE:4623-TrainTER-87613422-87594002"
            },
            "id":"journey_pattern:1204",
            "name":"journey_pattern:1204"
         },
         "disruptions":[

         ],
         "calendars":[
            {
               "active_periods":[
                  {
                     "begin":"20181102",
                     "end":"20181201"
                  }
               ],
               "week_pattern":{
                  "monday":true,
                  "tuesday":true,
                  "friday":true,
                  "wednesday":true,
                  "thursday":true,
                  "sunday":false,
                  "saturday":false
               }
            }
         ],
         "stop_times":[
            {
               "stop_point":{
                  "name":"Rodez",
                  "links":[

                  ],
                  "coord":{
                     "lat":"44.362645",
                     "lon":"2.580254"
                  },
                  "label":"Rodez (Rodez)",
                  "equipments":[

                  ],
                  "administrative_regions":[
                     {
                        "insee":"12202",
                        "name":"Rodez",
                        "level":8,
                        "coord":{
                           "lat":"44.351002",
                           "lon":"2.5733"
                        },
                        "label":"Rodez (12000)",
                        "id":"admin:fr:12202",
                        "zip_code":"12000"
                     }
                  ],
                  "fare_zone":{
                     "name":"0"
                  },
                  "id":"stop_point:OCE:SP:TrainTER-87613422",
                  "stop_area":{
                     "codes":[
                        {
                           "type":"CR-CI-CH",
                           "value":"0087-613422-BV"
                        },
                        {
                           "type":"UIC8",
                           "value":"87613422"
                        },
                        {
                           "type":"external_code",
                           "value":"OCE87613422"
                        }
                     ],
                     "name":"Rodez",
                     "links":[

                     ],
                     "coord":{
                        "lat":"44.362645",
                        "lon":"2.580254"
                     },
                     "label":"Rodez (Rodez)",
                     "timezone":"Europe\/Paris",
                     "id":"stop_area:OCE:SA:87613422"
                  }
               },
               "utc_arrival_time":"095400",
               "utc_departure_time":"095400",
               "headsign":"870154",
               "arrival_time":"105400",
               "journey_pattern_point":{
                  "id":"journey_pattern_point:9786"
               },
               "departure_time":"105400"
            },
            {
               "stop_point":{
                  "name":"St-Christophe",
                  "links":[

                  ],
                  "coord":{
                     "lat":"44.464679",
                     "lon":"2.407487"
                  },
                  "label":"St-Christophe (Saint-Christophe-Vallon)",
                  "equipments":[

                  ],
                  "administrative_regions":[
                     {
                        "insee":"12215",
                        "name":"Saint-Christophe-Vallon",
                        "level":8,
                        "coord":{
                           "lat":"44.4702",
                           "lon":"2.409979"
                        },
                        "label":"Saint-Christophe-Vallon (12330)",
                        "id":"admin:fr:12215",
                        "zip_code":"12330"
                     }
                  ],
                  "fare_zone":{
                     "name":"0"
                  },
                  "id":"stop_point:OCE:SP:TrainTER-87613257",
                  "stop_area":{
                     "codes":[
                        {
                           "type":"CR-CI-CH",
                           "value":"0087-613257-00"
                        },
                        {
                           "type":"UIC8",
                           "value":"87613257"
                        },
                        {
                           "type":"external_code",
                           "value":"OCE87613257"
                        }
                     ],
                     "name":"St-Christophe",
                     "links":[

                     ],
                     "coord":{
                        "lat":"44.464679",
                        "lon":"2.407487"
                     },
                     "label":"St-Christophe (Saint-Christophe-Vallon)",
                     "timezone":"Europe\/Paris",
                     "id":"stop_area:OCE:SA:87613257"
                  }
               },
               "utc_arrival_time":"101700",
               "utc_departure_time":"101800",
               "headsign":"870154",
               "arrival_time":"111700",
               "journey_pattern_point":{
                  "id":"journey_pattern_point:9787"
               },
               "departure_time":"111800"
            },
            {
               "stop_point":{
                  "name":"Cransac",
                  "links":[

                  ],
                  "coord":{
                     "lat":"44.523054",
                     "lon":"2.270766"
                  },
                  "label":"Cransac (Cransac)",
                  "equipments":[

                  ],
                  "administrative_regions":[
                     {
                        "insee":"12083",
                        "name":"Cransac",
                        "level":8,
                        "coord":{
                           "lat":"44.524727",
                           "lon":"2.281037"
                        },
                        "label":"Cransac (12110)",
                        "id":"admin:fr:12083",
                        "zip_code":"12110"
                     }
                  ],
                  "fare_zone":{
                     "name":"0"
                  },
                  "id":"stop_point:OCE:SP:TrainTER-87613232",
                  "stop_area":{
                     "codes":[
                        {
                           "type":"CR-CI-CH",
                           "value":"0087-613232-00"
                        },
                        {
                           "type":"UIC8",
                           "value":"87613232"
                        },
                        {
                           "type":"external_code",
                           "value":"OCE87613232"
                        }
                     ],
                     "name":"Cransac",
                     "links":[

                     ],
                     "coord":{
                        "lat":"44.523054",
                        "lon":"2.270766"
                     },
                     "label":"Cransac (Cransac)",
                     "timezone":"Europe\/Paris",
                     "id":"stop_area:OCE:SA:87613232"
                  }
               },
               "utc_arrival_time":"102900",
               "utc_departure_time":"103000",
               "headsign":"870154",
               "arrival_time":"112900",
               "journey_pattern_point":{
                  "id":"journey_pattern_point:9788"
               },
               "departure_time":"113000"
            },
            {
               "stop_point":{
                  "name":"Aubin",
                  "links":[

                  ],
                  "coord":{
                     "lat":"44.527347",
                     "lon":"2.239558"
                  },
                  "label":"Aubin (Aubin)",
                  "equipments":[

                  ],
                  "administrative_regions":[
                     {
                        "insee":"12013",
                        "name":"Aubin",
                        "level":8,
                        "coord":{
                           "lat":"44.527306",
                           "lon":"2.243437"
                        },
                        "label":"Aubin (12110)",
                        "id":"admin:fr:12013",
                        "zip_code":"12110"
                     }
                  ],
                  "fare_zone":{
                     "name":"0"
                  },
                  "id":"stop_point:OCE:SP:TrainTER-87613224",
                  "stop_area":{
                     "codes":[
                        {
                           "type":"CR-CI-CH",
                           "value":"0087-613224-00"
                        },
                        {
                           "type":"UIC8",
                           "value":"87613224"
                        },
                        {
                           "type":"external_code",
                           "value":"OCE87613224"
                        }
                     ],
                     "name":"Aubin",
                     "links":[

                     ],
                     "coord":{
                        "lat":"44.527347",
                        "lon":"2.239558"
                     },
                     "label":"Aubin (Aubin)",
                     "timezone":"Europe\/Paris",
                     "id":"stop_area:OCE:SA:87613224"
                  }
               },
               "utc_arrival_time":"103300",
               "utc_departure_time":"103400",
               "headsign":"870154",
               "arrival_time":"113300",
               "journey_pattern_point":{
                  "id":"journey_pattern_point:9789"
               },
               "departure_time":"113400"
            },
            {
               "stop_point":{
                  "name":"Viviez-Decazeville",
                  "links":[

                  ],
                  "coord":{
                     "lat":"44.55703",
                     "lon":"2.218023"
                  },
                  "label":"Viviez-Decazeville (Viviez)",
                  "equipments":[

                  ],
                  "administrative_regions":[
                     {
                        "insee":"12305",
                        "name":"Viviez",
                        "level":8,
                        "coord":{
                           "lat":"44.555798",
                           "lon":"2.215909"
                        },
                        "label":"Viviez (12110)",
                        "id":"admin:fr:12305",
                        "zip_code":"12110"
                     }
                  ],
                  "fare_zone":{
                     "name":"0"
                  },
                  "id":"stop_point:OCE:SP:TrainTER-87613661",
                  "stop_area":{
                     "codes":[
                        {
                           "type":"CR-CI-CH",
                           "value":"0087-613661-BV"
                        },
                        {
                           "type":"UIC8",
                           "value":"87613661"
                        },
                        {
                           "type":"external_code",
                           "value":"OCE87613661"
                        }
                     ],
                     "name":"Viviez-Decazeville",
                     "links":[

                     ],
                     "coord":{
                        "lat":"44.55703",
                        "lon":"2.218023"
                     },
                     "label":"Viviez-Decazeville (Viviez)",
                     "timezone":"Europe\/Paris",
                     "id":"stop_area:OCE:SA:87613661"
                  }
               },
               "utc_arrival_time":"103800",
               "utc_departure_time":"103900",
               "headsign":"870154",
               "arrival_time":"113800",
               "journey_pattern_point":{
                  "id":"journey_pattern_point:9790"
               },
               "departure_time":"113900"
            },
            {
               "stop_point":{
                  "name":"Capdenac",
                  "links":[

                  ],
                  "coord":{
                     "lat":"44.577647",
                     "lon":"2.0789"
                  },
                  "label":"Capdenac (Capdenac-Gare)",
                  "equipments":[

                  ],
                  "administrative_regions":[
                     {
                        "insee":"12052",
                        "name":"Capdenac-Gare",
                        "level":8,
                        "coord":{
                           "lat":"44.574112",
                           "lon":"2.080516"
                        },
                        "label":"Capdenac-Gare (12700)",
                        "id":"admin:fr:12052",
                        "zip_code":"12700"
                     }
                  ],
                  "fare_zone":{
                     "name":"0"
                  },
                  "id":"stop_point:OCE:SP:TrainTER-87613109",
                  "stop_area":{
                     "codes":[
                        {
                           "type":"CR-CI-CH",
                           "value":"0087-613109-BV"
                        },
                        {
                           "type":"UIC8",
                           "value":"87613109"
                        },
                        {
                           "type":"external_code",
                           "value":"OCE87613109"
                        }
                     ],
                     "name":"Capdenac",
                     "links":[

                     ],
                     "coord":{
                        "lat":"44.577647",
                        "lon":"2.0789"
                     },
                     "label":"Capdenac (Capdenac-Gare)",
                     "timezone":"Europe\/Paris",
                     "id":"stop_area:OCE:SA:87613109"
                  }
               },
               "utc_arrival_time":"105300",
               "utc_departure_time":"105500",
               "headsign":"870154",
               "arrival_time":"115300",
               "journey_pattern_point":{
                  "id":"journey_pattern_point:9791"
               },
               "departure_time":"115500"
            },
            {
               "stop_point":{
                  "name":"Figeac",
                  "links":[

                  ],
                  "coord":{
                     "lat":"44.603505",
                     "lon":"2.037074"
                  },
                  "label":"Figeac (Figeac)",
                  "equipments":[

                  ],
                  "administrative_regions":[
                     {
                        "insee":"46102",
                        "name":"Figeac",
                        "level":8,
                        "coord":{
                           "lat":"44.609234",
                           "lon":"2.032432"
                        },
                        "label":"Figeac (46100)",
                        "id":"admin:fr:46102",
                        "zip_code":"46100"
                     }
                  ],
                  "fare_zone":{
                     "name":"0"
                  },
                  "id":"stop_point:OCE:SP:TrainTER-87613091",
                  "stop_area":{
                     "codes":[
                        {
                           "type":"CR-CI-CH",
                           "value":"0087-613091-BV"
                        },
                        {
                           "type":"UIC8",
                           "value":"87613091"
                        },
                        {
                           "type":"external_code",
                           "value":"OCE87613091"
                        }
                     ],
                     "name":"Figeac",
                     "links":[

                     ],
                     "coord":{
                        "lat":"44.603505",
                        "lon":"2.037074"
                     },
                     "label":"Figeac (Figeac)",
                     "timezone":"Europe\/Paris",
                     "id":"stop_area:OCE:SA:87613091"
                  }
               },
               "utc_arrival_time":"110100",
               "utc_departure_time":"110200",
               "headsign":"870154",
               "arrival_time":"120100",
               "journey_pattern_point":{
                  "id":"journey_pattern_point:9792"
               },
               "departure_time":"120200"
            },
            {
               "stop_point":{
                  "name":"Assier",
                  "links":[

                  ],
                  "coord":{
                     "lat":"44.674584",
                     "lon":"1.869744"
                  },
                  "label":"Assier (Assier)",
                  "equipments":[

                  ],
                  "administrative_regions":[
                     {
                        "insee":"46009",
                        "name":"Assier",
                        "level":8,
                        "coord":{
                           "lat":"44.675301",
                           "lon":"1.876286"
                        },
                        "label":"Assier (46320)",
                        "id":"admin:fr:46009",
                        "zip_code":"46320"
                     }
                  ],
                  "fare_zone":{
                     "name":"0"
                  },
                  "id":"stop_point:OCE:SP:TrainTER-87613075",
                  "stop_area":{
                     "codes":[
                        {
                           "type":"CR-CI-CH",
                           "value":"0087-613075-00"
                        },
                        {
                           "type":"UIC8",
                           "value":"87613075"
                        },
                        {
                           "type":"external_code",
                           "value":"OCE87613075"
                        }
                     ],
                     "name":"Assier",
                     "links":[

                     ],
                     "coord":{
                        "lat":"44.674584",
                        "lon":"1.869744"
                     },
                     "label":"Assier (Assier)",
                     "timezone":"Europe\/Paris",
                     "id":"stop_area:OCE:SA:87613075"
                  }
               },
               "utc_arrival_time":"111700",
               "utc_departure_time":"111800",
               "headsign":"870154",
               "arrival_time":"121700",
               "journey_pattern_point":{
                  "id":"journey_pattern_point:9793"
               },
               "departure_time":"121800"
            },
            {
               "stop_point":{
                  "name":"Gramat",
                  "links":[

                  ],
                  "coord":{
                     "lat":"44.77348",
                     "lon":"1.722367"
                  },
                  "label":"Gramat (Gramat)",
                  "equipments":[

                  ],
                  "administrative_regions":[
                     {
                        "insee":"46128",
                        "name":"Gramat",
                        "level":8,
                        "coord":{
                           "lat":"44.778996",
                           "lon":"1.723394"
                        },
                        "label":"Gramat (46500)",
                        "id":"admin:fr:46128",
                        "zip_code":"46500"
                     }
                  ],
                  "fare_zone":{
                     "name":"0"
                  },
                  "id":"stop_point:OCE:SP:TrainTER-87613059",
                  "stop_area":{
                     "codes":[
                        {
                           "type":"CR-CI-CH",
                           "value":"0087-613059-BV"
                        },
                        {
                           "type":"UIC8",
                           "value":"87613059"
                        },
                        {
                           "type":"external_code",
                           "value":"OCE87613059"
                        }
                     ],
                     "name":"Gramat",
                     "links":[

                     ],
                     "coord":{
                        "lat":"44.77348",
                        "lon":"1.722367"
                     },
                     "label":"Gramat (Gramat)",
                     "timezone":"Europe\/Paris",
                     "id":"stop_area:OCE:SA:87613059"
                  }
               },
               "utc_arrival_time":"112900",
               "utc_departure_time":"113000",
               "headsign":"870154",
               "arrival_time":"122900",
               "journey_pattern_point":{
                  "id":"journey_pattern_point:9794"
               },
               "departure_time":"123000"
            },
            {
               "stop_point":{
                  "name":"Rocamadour-Padirac",
                  "links":[

                  ],
                  "coord":{
                     "lat":"44.817902",
                     "lon":"1.657441"
                  },
                  "label":"Rocamadour-Padirac (Rocamadour)",
                  "equipments":[

                  ],
                  "administrative_regions":[
                     {
                        "insee":"46240",
                        "name":"Rocamadour",
                        "level":8,
                        "coord":{
                           "lat":"44.799187",
                           "lon":"1.618352"
                        },
                        "label":"Rocamadour (46500)",
                        "id":"admin:fr:46240",
                        "zip_code":"46500"
                     }
                  ],
                  "fare_zone":{
                     "name":"0"
                  },
                  "id":"stop_point:OCE:SP:TrainTER-87613042",
                  "stop_area":{
                     "codes":[
                        {
                           "type":"CR-CI-CH",
                           "value":"0087-613042-BV"
                        },
                        {
                           "type":"UIC8",
                           "value":"87613042"
                        },
                        {
                           "type":"external_code",
                           "value":"OCE87613042"
                        }
                     ],
                     "name":"Rocamadour-Padirac",
                     "links":[

                     ],
                     "coord":{
                        "lat":"44.817902",
                        "lon":"1.657441"
                     },
                     "label":"Rocamadour-Padirac (Rocamadour)",
                     "timezone":"Europe\/Paris",
                     "id":"stop_area:OCE:SA:87613042"
                  }
               },
               "utc_arrival_time":"113600",
               "utc_departure_time":"113700",
               "headsign":"870154",
               "arrival_time":"123600",
               "journey_pattern_point":{
                  "id":"journey_pattern_point:9795"
               },
               "departure_time":"123700"
            },
            {
               "stop_point":{
                  "name":"St-Denis-pr\u00e8s-Martel",
                  "links":[

                  ],
                  "coord":{
                     "lat":"44.945783",
                     "lon":"1.666282"
                  },
                  "label":"St-Denis-pr\u00e8s-Martel (Saint-Denis-l\u00e8s-Martel)",
                  "equipments":[

                  ],
                  "administrative_regions":[
                     {
                        "insee":"46265",
                        "name":"Saint-Denis-l\u00e8s-Martel",
                        "level":8,
                        "coord":{
                           "lat":"44.940029",
                           "lon":"1.661536"
                        },
                        "label":"Saint-Denis-l\u00e8s-Martel (46600)",
                        "id":"admin:fr:46265",
                        "zip_code":"46600"
                     }
                  ],
                  "fare_zone":{
                     "name":"0"
                  },
                  "id":"stop_point:OCE:SP:TrainTER-87594572",
                  "stop_area":{
                     "codes":[
                        {
                           "type":"CR-CI-CH",
                           "value":"0087-594572-00"
                        },
                        {
                           "type":"UIC8",
                           "value":"87594572"
                        },
                        {
                           "type":"external_code",
                           "value":"OCE87594572"
                        }
                     ],
                     "name":"St-Denis-pr\u00e8s-Martel",
                     "links":[

                     ],
                     "coord":{
                        "lat":"44.945783",
                        "lon":"1.666282"
                     },
                     "label":"St-Denis-pr\u00e8s-Martel (Saint-Denis-l\u00e8s-Martel)",
                     "timezone":"Europe\/Paris",
                     "id":"stop_area:OCE:SA:87594572"
                  }
               },
               "utc_arrival_time":"115100",
               "utc_departure_time":"115200",
               "headsign":"870154",
               "arrival_time":"125100",
               "journey_pattern_point":{
                  "id":"journey_pattern_point:9796"
               },
               "departure_time":"125200"
            },
            {
               "stop_point":{
                  "name":"Brive-la-Gaillarde",
                  "links":[

                  ],
                  "coord":{
                     "lat":"45.152554",
                     "lon":"1.528616"
                  },
                  "label":"Brive-la-Gaillarde (Brive-la-Gaillarde)",
                  "equipments":[

                  ],
                  "administrative_regions":[
                     {
                        "insee":"19031",
                        "name":"Brive-la-Gaillarde",
                        "level":8,
                        "coord":{
                           "lat":"45.158497",
                           "lon":"1.533238"
                        },
                        "label":"Brive-la-Gaillarde (19100)",
                        "id":"admin:fr:19031",
                        "zip_code":"19100"
                     }
                  ],
                  "fare_zone":{
                     "name":"0"
                  },
                  "id":"stop_point:OCE:SP:TrainTER-87594002",
                  "stop_area":{
                     "codes":[
                        {
                           "type":"CR-CI-CH",
                           "value":"0087-594002-BV"
                        },
                        {
                           "type":"UIC8",
                           "value":"87594002"
                        },
                        {
                           "type":"external_code",
                           "value":"OCE87594002"
                        }
                     ],
                     "name":"Brive-la-Gaillarde",
                     "links":[

                     ],
                     "coord":{
                        "lat":"45.152554",
                        "lon":"1.528616"
                     },
                     "label":"Brive-la-Gaillarde (Brive-la-Gaillarde)",
                     "timezone":"Europe\/Paris",
                     "id":"stop_area:OCE:SA:87594002"
                  }
               },
               "utc_arrival_time":"121500",
               "utc_departure_time":"121500",
               "headsign":"870154",
               "arrival_time":"131500",
               "journey_pattern_point":{
                  "id":"journey_pattern_point:9797"
               },
               "departure_time":"131500"
            }
         ],
         "validity_pattern":{
            "beginning_date":"20181009",
            "days":"000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000011111001111100111110011111001000000000000000000000000"
         },
         "id":"vehicle_journey:OCE:SN870154F01001",
         "trip":{
            "id":"OCE:SN870154F01001",
            "name":"870154"
         }
      }
   ]
}
"""
