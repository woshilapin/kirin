# coding=utf-8

# Copyright (c) 2001-2015, Canal TP and/or its affiliates. All rights reserved.
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
from pytz import utc

from tests.check_utils import api_get
from kirin.core import model
from kirin import app
from datetime import datetime, time
import pytest


def test_end_point():
    resp = api_get("/")
    assert "status" in resp
    assert "cots" in resp
    assert "contributors" in resp


def test_status(setup_database):
    resp = api_get("/status")

    assert "version" in resp
    assert "db_pool_status" in resp
    assert "db_version" in resp
    assert "navitia_url" in resp
    assert "last_update" in resp
    assert "realtime.cots" in resp["last_update"]
    assert "realtime.sherbrooke" in resp["last_update"]

    assert "2015-11-04T07:32:00Z" in resp["last_update"]["realtime.cots"]
    assert "2015-11-04T07:52:00Z" in resp["last_update"]["realtime.sherbrooke"]

    assert "realtime.sherbrooke" in resp["last_update_error"]
    assert "2015-11-04T07:32:00Z" in resp["last_valid_update"]["realtime.cots"]
    assert "2015-11-04T07:42:00Z" in resp["last_valid_update"]["realtime.sherbrooke"]


@pytest.fixture()
def setup_database():
    """
    we create two realtime_updates with the same vj but for different date
    and return a vj for navitia
    """
    with app.app_context():
        vj1 = model.VehicleJourney(
            {
                "trip": {"id": "vj:1"},
                "stop_times": [
                    {"utc_arrival_time": time(9, 0), "stop_point": {"stop_area": {"timezone": "Europe/Paris"}}}
                ],
            },
            utc.localize(datetime(2015, 11, 4, 8, 0, 0)),
            utc.localize(datetime(2015, 11, 4, 10, 0, 0)),
        )
        vj2 = model.VehicleJourney(
            {
                "trip": {"id": "vj:2"},
                "stop_times": [
                    {"utc_arrival_time": time(9, 0), "stop_point": {"stop_area": {"timezone": "Europe/Paris"}}}
                ],
            },
            utc.localize(datetime(2015, 11, 4, 8, 0, 0)),
            utc.localize(datetime(2015, 11, 4, 10, 0, 0)),
        )
        vj3 = model.VehicleJourney(
            {
                "trip": {"id": "vj:3"},
                "stop_times": [
                    {"utc_arrival_time": time(9, 0), "stop_point": {"stop_area": {"timezone": "Europe/Paris"}}}
                ],
            },
            utc.localize(datetime(2015, 11, 4, 8, 0, 0)),
            utc.localize(datetime(2015, 11, 4, 10, 0, 0)),
        )
        tu1 = model.TripUpdate(vj1, contributor="realtime.cots")
        tu2 = model.TripUpdate(vj2, contributor="realtime.cots")
        tu3 = model.TripUpdate(vj3, contributor="realtime.sherbrooke")
        rtu1 = model.RealTimeUpdate(None, "cots", "realtime.cots")
        rtu1.created_at = datetime(2015, 11, 4, 6, 32)
        rtu1.trip_updates.append(tu1)
        model.db.session.add(rtu1)
        rtu2 = model.RealTimeUpdate(None, "cots", contributor="realtime.cots")
        rtu2.created_at = datetime(2015, 11, 4, 7, 32)
        rtu2.trip_updates.append(tu2)
        model.db.session.add(rtu2)

        rtu3 = model.RealTimeUpdate(None, "gtfs-rt", contributor="realtime.sherbrooke")
        rtu3.created_at = datetime(2015, 11, 4, 7, 42)
        rtu3.trip_updates.append(tu3)
        model.db.session.add(rtu3)

        rtu4 = model.RealTimeUpdate(
            None,
            connector="gtfs-rt",
            contributor="realtime.sherbrooke",
            status="KO",
            error="No new information destinated to navitia for this gtfs-rt",
        )
        rtu4.created_at = datetime(2015, 11, 4, 7, 52)
        model.db.session.add(rtu4)
        model.db.session.commit()
