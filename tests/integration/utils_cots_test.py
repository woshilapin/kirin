# coding: utf8

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
import requests_mock
import json

mock_token_json_response = """{
    "access_token": "wonderful_token",
    "token_type": "Bearer"
}"""

mock_resource_json_response = """[
{
    "labelExt": "Régulation du trafic",
    "idExt": 124,
    "id": 24,
    "label": "Espacement/rétention",
    "validityDates": {
        "start": 82800000,
        "end": 1546210800000
    }
},
{
    "labelExt": "Défaut d'alimentation électrique",
    "idExt": 104,
    "label": "Défaut d'alimentation électrique",
    "id": 4,
    "validityDates": {
        "start": 82800000,
        "end": 1546210800000
    }
},
{
    "labelExt": "Affluence exceptionnelle de voyageurs",
    "idExt": 103,
    "label": "Affluence exceptionnelle de voyageurs",
    "id": 3,
    "validityDates": {
        "start": 82800000,
        "end": 1546210800000
    }
},
{
    "validityDates": {
        "end": 1546210800000,
        "start": 82800000
    },
    "labelExt": "Accident à un Passage à Niveau",
    "idExt": 101,
    "label": "Accident de personnes à un Passage à Niveau",
    "id": 1
}
]"""


def data_matcher(request):
    if not request:
        return False
    return (
        "client_id=tchoutchou_id" in request.text
        and "client_secret=tchoutchou_secret" in request.text
        and "grant_type=client_credentials" in request.text
    )


def requests_mock_cause_message(mock):
    """
    Mock all calls to message sub-service, matching test_settings
    """
    mock.post(
        "https://messages.service/token",
        json=json.loads(mock_token_json_response),
        request_headers={"X-API-Key": "tchoutchou_api_key"},
        additional_matcher=data_matcher,
        status_code=200,
    )
    mock.get(
        "https://messages.service/resource",
        json=json.loads(mock_resource_json_response),
        request_headers={"X-API-Key": "tchoutchou_api_key", "Authorization": "Bearer wonderful_token"},
        status_code=200,
    )
    return requests_mock
