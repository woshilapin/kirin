# coding=utf-8

# Copyright (c) 2001, Canal TP and/or its affiliates. All rights reserved.
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

from kirin.core.types import ConnectorType
from kirin.utils import make_rt_update, save_rt_data_with_error
from tests.check_utils import api_get
from kirin.core import model
from kirin import app
from datetime import datetime, time
from tests.integration.conftest import (
    COTS_CONTRIBUTOR_ID,
    PIV_CONTRIBUTOR_ID,
    COTS_CONTRIBUTOR_DB_ID,
    GTFS_CONTRIBUTOR_ID,
    PIV_CONTRIBUTOR_DB_ID,
    GTFS_CONTRIBUTOR_DB_ID,
)
import pytest
import requests_mock
import kirin


def test_end_point():
    resp = api_get("/")
    assert "status" in resp
    assert "cots" in resp
    assert "contributors" in resp
    assert "health" in resp
    assert "piv" in resp

    # test that the contributors endpoints are listed in piv POST endpoint
    resp = api_get("/piv")
    assert "/piv/{}".format(PIV_CONTRIBUTOR_ID) in resp[PIV_CONTRIBUTOR_ID]["href"]
    assert "/piv/{}".format(PIV_CONTRIBUTOR_DB_ID) in resp[PIV_CONTRIBUTOR_DB_ID]["href"]


def test_status(setup_database):
    resp = api_get("/status")

    assert "version" in resp
    assert "db_pool_status" in resp
    assert "db_version" in resp
    assert "navitia_url" in resp
    assert "last_update" in resp
    assert resp["navitia_connection"] == "KO"
    assert resp["db_connection"] == "OK"
    assert COTS_CONTRIBUTOR_ID in resp["last_update"]
    assert GTFS_CONTRIBUTOR_ID in resp["last_update"]
    assert PIV_CONTRIBUTOR_ID in resp["last_update"]

    assert "2015-11-04T07:32:00Z" in resp["last_update"][COTS_CONTRIBUTOR_ID]
    assert "2015-11-04T07:52:00Z" in resp["last_update"][GTFS_CONTRIBUTOR_ID]
    assert "2015-11-04T08:17:00Z" in resp["last_update"][PIV_CONTRIBUTOR_ID]

    assert GTFS_CONTRIBUTOR_ID in resp["last_update_error"]
    assert "2015-11-04T07:32:00Z" in resp["last_valid_update"][COTS_CONTRIBUTOR_ID]
    assert "2015-11-04T07:42:00Z" in resp["last_valid_update"][GTFS_CONTRIBUTOR_ID]

    assert "rabbitmq_info" in resp
    assert "password" not in resp["rabbitmq_info"]


def test_status_from_db(setup_database):
    """
    Check that contributors are read from db and returned in /status
    """
    # Set "GTFS_RT_CONTRIBUTOR" to None to read contributor from db
    app.config["GTFS_RT_CONTRIBUTOR"] = None
    resp = api_get("/status")
    assert "version" in resp
    assert "db_pool_status" in resp
    assert "db_version" in resp
    assert "navitia_url" in resp
    assert "last_update" in resp
    assert GTFS_CONTRIBUTOR_DB_ID in resp["last_update"]
    assert "2015-11-04T08:02:00Z" in resp["last_update"][GTFS_CONTRIBUTOR_DB_ID]
    assert COTS_CONTRIBUTOR_DB_ID in resp["last_update"]  # config does not affect status anymore
    assert PIV_CONTRIBUTOR_ID in resp["last_update"]

    # Set "GTFS_RT_CONTRIBUTOR" to "rt.vroumvroum" to read contributor from file
    # Contributor GTFS_CONTRIBUTOR_DB should also be present
    app.config["GTFS_RT_CONTRIBUTOR"] = "rt.vroumvroum"
    # Set "COTS_CONTRIBUTOR" to None to read contributor from db
    app.config["COTS_CONTRIBUTOR"] = None
    resp = api_get("/status")
    assert "last_update" in resp
    assert COTS_CONTRIBUTOR_DB_ID in resp["last_update"]
    assert "2015-11-04T08:12:00Z" in resp["last_update"][COTS_CONTRIBUTOR_DB_ID]
    assert GTFS_CONTRIBUTOR_DB_ID in resp["last_update"]
    assert "2015-11-04T08:02:00Z" in resp["last_update"][GTFS_CONTRIBUTOR_DB_ID]
    assert GTFS_CONTRIBUTOR_ID in resp["last_update"]
    assert "2015-11-04T07:52:00Z" in resp["last_update"][GTFS_CONTRIBUTOR_ID]
    assert PIV_CONTRIBUTOR_ID in resp["last_update"]
    assert "2015-11-04T08:17:00Z" in resp["last_update"][PIV_CONTRIBUTOR_ID]


def test_health_ok(setup_database):
    with requests_mock.mock() as m:
        # Connection to navitia and database works
        kirin.app.config["NAVITIA_URL"] = "http://navitia"
        m.head("http://navitia", status_code=200)
        resp = api_get("/health")
        assert resp["message"] == "OK"


def test_health_navitia_ko(setup_database):
    with requests_mock.mock() as m:
        # Connection to navitia fails
        kirin.app.config["NAVITIA_URL"] = "http://navitia_on_error"
        m.head("http://navitia_on_error", status_code=400)
        resp, status = api_get("/health", check=False)
        assert resp["message"] == "KO"
        assert status == 503


def test_health_database_ko(setup_database):
    with requests_mock.mock() as m:
        kirin.app.config["NAVITIA_URL"] = "http://navitia"
        m.head("http://navitia", status_code=200)
        # Keep original database configuration for future
        db_config = kirin.app.config[str("SQLALCHEMY_DATABASE_URI")]
        kirin.app.config["SQLALCHEMY_DATABASE_URI"] = "database_on_error"
        resp, status = api_get("/health", check=False)
        assert resp["message"] == "KO"
        assert status == 503

        # We need to reassign original configuration for teardown
        # The heath check is back to normal
        kirin.app.config["SQLALCHEMY_DATABASE_URI"] = db_config
        kirin.app.config["NAVITIA_URL"] = "http://navitia"
        m.head("http://navitia", status_code=200)
        resp = api_get("/health")
        assert resp["message"] == "OK"


def test_status_with_navitia_ko(setup_database):
    with requests_mock.mock() as m:
        kirin.app.config["NAVITIA_URL"] = "http://navitia_on_error"
        m.head("http://navitia_on_error", status_code=400)
        resp, _ = api_get("/status", check=False)
        assert resp["navitia_connection"] == "KO"
        assert resp["db_connection"] == "OK"

        # All the other attributes are present as in the test "test_status()"
        assert "version" in resp
        assert "db_pool_status" in resp
        assert "db_version" in resp
        assert "navitia_url" in resp
        assert "last_update" in resp
        assert COTS_CONTRIBUTOR_ID in resp["last_update"]
        assert GTFS_CONTRIBUTOR_ID in resp["last_update"]
        assert "2015-11-04T07:32:00Z" in resp["last_update"][COTS_CONTRIBUTOR_ID]
        assert "2015-11-04T07:52:00Z" in resp["last_update"][GTFS_CONTRIBUTOR_ID]
        assert GTFS_CONTRIBUTOR_ID in resp["last_update_error"]
        assert "2015-11-04T07:32:00Z" in resp["last_valid_update"][COTS_CONTRIBUTOR_ID]
        assert "2015-11-04T07:42:00Z" in resp["last_valid_update"][GTFS_CONTRIBUTOR_ID]


def test_status_with_database_ko(setup_database):
    with requests_mock.mock() as m:
        kirin.app.config["NAVITIA_URL"] = "http://navitia"
        m.head("http://navitia", status_code=200)
        # Keep original database configuration for future
        db_config = kirin.app.config[str("SQLALCHEMY_DATABASE_URI")]
        kirin.app.config["SQLALCHEMY_DATABASE_URI"] = "database_on_error"
        resp, _ = api_get("/status", check=False)
        # We need to reassign original configuration for teardown
        kirin.app.config["SQLALCHEMY_DATABASE_URI"] = db_config
        assert resp["navitia_connection"] == "OK"
        assert resp["db_connection"] == "KO"

        assert "version" in resp
        assert len(resp["last_update"]) == 0
        assert len(resp["last_update_error"]) == 0
        assert len(resp["last_valid_update"]) == 0
        assert resp["db_pool_status"] is None
        assert resp["db_version"] is None
        assert "navitia_url" in resp


def test_status_with_database_and_navitia_ko(setup_database):
    with requests_mock.mock() as m:
        kirin.app.config["NAVITIA_URL"] = "http://navitia_on_error"
        m.head("http://navitia_on_error", status_code=400)
        # Keep original database configuration for future
        db_config = kirin.app.config[str("SQLALCHEMY_DATABASE_URI")]
        kirin.app.config["SQLALCHEMY_DATABASE_URI"] = "database_on_error"
        resp, _ = api_get("/status", check=False)
        # We need to reassign original configuration for teardown
        kirin.app.config["SQLALCHEMY_DATABASE_URI"] = db_config
        assert resp["navitia_connection"] == "KO"
        assert resp["db_connection"] == "KO"

        assert "version" in resp
        assert len(resp["last_update"]) == 0
        assert len(resp["last_update_error"]) == 0
        assert len(resp["last_valid_update"]) == 0
        assert resp["db_pool_status"] is None
        assert resp["db_version"] is None
        assert "navitia_url" in resp


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
            datetime(2015, 11, 4, 8, 0, 0),
            datetime(2015, 11, 4, 10, 0, 0),
        )
        vj2 = model.VehicleJourney(
            {
                "trip": {"id": "vj:2"},
                "stop_times": [
                    {"utc_arrival_time": time(9, 0), "stop_point": {"stop_area": {"timezone": "Europe/Paris"}}}
                ],
            },
            datetime(2015, 11, 4, 8, 0, 0),
            datetime(2015, 11, 4, 10, 0, 0),
        )
        vj3 = model.VehicleJourney(
            {
                "trip": {"id": "vj:3"},
                "stop_times": [
                    {"utc_arrival_time": time(9, 0), "stop_point": {"stop_area": {"timezone": "Europe/Paris"}}}
                ],
            },
            datetime(2015, 11, 4, 8, 0, 0),
            datetime(2015, 11, 4, 10, 0, 0),
        )
        tu1 = model.TripUpdate(vj1, contributor_id=COTS_CONTRIBUTOR_ID)
        tu2 = model.TripUpdate(vj2, contributor_id=COTS_CONTRIBUTOR_ID)
        tu3 = model.TripUpdate(vj3, contributor_id=GTFS_CONTRIBUTOR_ID)
        rtu1 = make_rt_update(None, ConnectorType.cots.value, COTS_CONTRIBUTOR_ID)
        rtu1.created_at = datetime(2015, 11, 4, 6, 32)
        rtu1.updated_at = datetime(2015, 11, 4, 6, 32)  # mock creation, no update done
        rtu1.trip_updates.append(tu1)
        model.db.session.add(rtu1)

        rtu2 = make_rt_update(None, ConnectorType.cots.value, contributor_id=COTS_CONTRIBUTOR_ID)
        rtu2.created_at = datetime(2015, 11, 4, 7, 32)
        rtu2.updated_at = datetime(2015, 11, 4, 7, 32)
        rtu2.trip_updates.append(tu2)
        model.db.session.add(rtu2)

        rtu3 = make_rt_update(None, ConnectorType.gtfs_rt.value, contributor_id=GTFS_CONTRIBUTOR_ID)
        rtu3.created_at = datetime(2015, 11, 4, 7, 42)
        rtu3.updated_at = datetime(2015, 11, 4, 7, 42)
        rtu3.trip_updates.append(tu3)
        model.db.session.add(rtu3)

        rtu4 = save_rt_data_with_error(
            None,
            connector_type=ConnectorType.gtfs_rt.value,
            contributor_id=GTFS_CONTRIBUTOR_ID,
            error="No new information destined to navitia for this gtfs-rt",
            is_reprocess_same_data_allowed=False,
        )
        rtu4.created_at = datetime(2015, 11, 4, 7, 52)
        rtu4.updated_at = datetime(2015, 11, 4, 7, 52)
        model.db.session.add(rtu4)

        rtu5 = make_rt_update(
            None, connector_type=ConnectorType.gtfs_rt.value, contributor_id=GTFS_CONTRIBUTOR_DB_ID
        )
        rtu5.created_at = datetime(2015, 11, 4, 8, 2)
        rtu5.updated_at = datetime(2015, 11, 4, 8, 2)
        model.db.session.add(rtu5)

        rtu6 = make_rt_update(
            None, connector_type=ConnectorType.cots.value, contributor_id=COTS_CONTRIBUTOR_DB_ID
        )
        rtu6.created_at = datetime(2015, 11, 4, 8, 12)
        rtu6.updated_at = datetime(2015, 11, 4, 8, 12)
        model.db.session.add(rtu6)

        rtu_piv = make_rt_update(None, connector_type=ConnectorType.piv.value, contributor_id=PIV_CONTRIBUTOR_ID)
        rtu_piv.created_at = datetime(2015, 11, 4, 8, 17)
        rtu_piv.updated_at = datetime(2015, 11, 4, 8, 17)
        model.db.session.add(rtu_piv)

        model.db.session.commit()
