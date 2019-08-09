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
from kirin.cots.model_maker import _retrieve_interesting_pdp


def test_retrieve_interesting_pdp():
    """
    In the example below:
    1st stop is probably just the garage (no time info) although it's a real station > NOT interesting
    2nd is a station and has a departure time > keeping it
    3rd is a station but has no departure nor arrival time > NOT interesting
    4th is a station (no typeArret is a station) and has departure/arrival times > keeping it
    5th is a station, doesn't have arrival time but we keep it as there is arrival time later in 7th
        (travelers are able to hop on, then hop off later) > keeping it
    6th is not a station > NOT interesting
    7th is a regular final traveler stop > keeping it
    8th is a station, doesn't have arrival time nor do the following stops > NOT interesting
    9th is in the same situation than 8th > NOT interesting

    This also tests that they are sorted according to 'rang':
    [2nd, 4th, 5th, 7th] are indexed [1, 3, 8, 5] initially
    """
    list_pdp = [
        {"@id": "1st", "rang": 1, "typeArret": "CD"},
        {
            "@id": "2nd",
            "rang": 2,
            "typeArret": "CH",
            "horaireVoyageurDepart": {"dateHeure": "2018-09-01T12:02:00+0000"},
        },
        {"@id": "3rd", "rang": 3, "typeArret": "FD"},
        {
            "@id": "4th",
            "rang": 4,
            "horaireVoyageurArrivee": {"dateHeure": "2018-09-01T12:04:00+0000"},
            "horaireVoyageurDepart": {"dateHeure": "2018-09-01T12:04:30+0000"},
        },
        {
            "@id": "6th",
            "rang": 6,
            "typeArret": "TOTO",
            "horaireVoyageurDepart": {"dateHeure": "2018-09-01T12:06:00+0000"},
        },
        {
            "@id": "7th",
            "rang": 7,
            "typeArret": "CD",
            "horaireVoyageurArrivee": {"dateHeure": "2018-09-01T12:07:00+0000"},
        },
        {
            "@id": "8th",
            "rang": 8,
            "typeArret": None,
            "horaireVoyageurDepart": {"dateHeure": "2018-09-01T12:08:00+0000"},
        },
        {"@id": "9th", "rang": 9, "typeArret": ""},
        {
            "@id": "5th",
            "rang": 5,
            "typeArret": "FH",
            "horaireVoyageurDepart": {"dateHeure": "2018-09-01T12:05:00+0000"},
        },
    ]
    assert _retrieve_interesting_pdp(list_pdp) == [list_pdp[1], list_pdp[3], list_pdp[8], list_pdp[5]]
