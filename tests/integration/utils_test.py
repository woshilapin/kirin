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
from kirin import db, app
from kirin.utils import make_rt_update, str_to_date
from kirin.core.model import VehicleJourney, TripUpdate, StopTimeUpdate, Contributor
import datetime


def test_valid_date():
    res = str_to_date("20151210")
    assert res == datetime.date(2015, 12, 10)


def test_invalid_date():
    res = str_to_date("aaaa")
    assert res == None


# def create_trip_update(vj_id, trip_id, circulation_date, contributor_id=COTS_CONTRIBUTOR_ID):
def create_trip_update(vj_id, trip_id, circulation_date, contributor_id):
    vj = VehicleJourney(
        {
            "trip": {"id": trip_id},
            "stop_times": [
                {"utc_arrival_time": datetime.time(8, 0), "stop_point": {"stop_area": {"timezone": "UTC"}}}
            ],
        },
        datetime.datetime.combine(circulation_date, datetime.time(7, 0)),
        datetime.datetime.combine(circulation_date, datetime.time(9, 0)),
    )
    vj.id = vj_id
    trip_update = TripUpdate(vj=vj, contributor_id=contributor_id)

    db.session.add(vj)
    db.session.add(trip_update)
    return trip_update


def create_rt_update_and_trip_update(id, contributor_id, connector_type, vj_id, trip_id, circulation_date):
    rtu = make_rt_update("", connector_type, contributor_id=contributor_id)
    rtu.id = id
    trip_update = create_trip_update(vj_id, trip_id, circulation_date, contributor_id)
    trip_update.contributor_id = contributor_id
    rtu.trip_updates.append(trip_update)
