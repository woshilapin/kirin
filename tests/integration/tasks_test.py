from __future__ import absolute_import, print_function, unicode_literals, division
from kirin import db, app
from kirin.core.model import (
    db,
    RealTimeUpdate,
    TripUpdate,
    StopTimeUpdate,
    VehicleJourney,
    DEFAULT_DAYS_TO_KEEP_TRIP_UPDATE,
    DEFAULT_DAYS_TO_KEEP_RT_UPDATE,
)
from kirin.core.types import ConnectorType
from kirin.tasks import purge_trip_update, purge_rt_update
from tests.integration.utils_test import create_rt_update_and_trip_update
from tests.integration.conftest import COTS_CONTRIBUTOR_ID
from datetime import date, timedelta

VJ_ID = "70866ce8-0638-4fa1-8556-1ddfa22d09d3"
TRIP_ID = "trip:1"


def test_purge_trip_and_rt(mock_rabbitmq):
    with app.app_context():
        create_rt_update_and_trip_update(
            "70866ce8-0638-4fa1-8556-1ddfa22d09d3",
            COTS_CONTRIBUTOR_ID,
            ConnectorType.gtfs_rt.value,
            VJ_ID,
            TRIP_ID,
            date.today() - timedelta(days=DEFAULT_DAYS_TO_KEEP_RT_UPDATE + 1),
        )
        db.session.commit()

        # Check there's really something before purge
        assert TripUpdate.query.count() == 1
        assert RealTimeUpdate.query.count() == 1

        config = {
            "contributor": COTS_CONTRIBUTOR_ID,
            "nb_days_to_keep": DEFAULT_DAYS_TO_KEEP_TRIP_UPDATE,
        }
        purge_trip_update(config)

        assert TripUpdate.query.count() == 0
        assert VehicleJourney.query.count() == 0
        assert StopTimeUpdate.query.count() == 0
        assert db.session.execute("select * from associate_realtimeupdate_tripupdate").rowcount == 0
        assert RealTimeUpdate.query.count() == 1

        config["nb_days_to_keep"] = DEFAULT_DAYS_TO_KEEP_RT_UPDATE
        RealTimeUpdate.query.first().created_at = date.today() - timedelta(
            days=DEFAULT_DAYS_TO_KEEP_RT_UPDATE + 1
        )
        purge_rt_update(config)

        assert TripUpdate.query.count() == 0
        assert VehicleJourney.query.count() == 0
        assert StopTimeUpdate.query.count() == 0
        assert db.session.execute("select * from associate_realtimeupdate_tripupdate").rowcount == 0
        assert RealTimeUpdate.query.count() == 0


def test_purge_trip_only(mock_rabbitmq):
    with app.app_context():
        create_rt_update_and_trip_update(
            "70866ce8-0638-4fa1-8556-1ddfa22d09d3",
            COTS_CONTRIBUTOR_ID,
            ConnectorType.gtfs_rt.value,
            VJ_ID,
            TRIP_ID,
            date.today() - timedelta(days=DEFAULT_DAYS_TO_KEEP_TRIP_UPDATE + 1),
        )
        db.session.commit()

        # Check there's really something before purge
        assert TripUpdate.query.count() == 1
        assert RealTimeUpdate.query.count() == 1

        config = {
            "contributor": COTS_CONTRIBUTOR_ID,
            "nb_days_to_keep": DEFAULT_DAYS_TO_KEEP_TRIP_UPDATE,
        }
        purge_trip_update(config)

        assert TripUpdate.query.count() == 0
        assert VehicleJourney.query.count() == 0
        assert StopTimeUpdate.query.count() == 0
        assert db.session.execute("select * from associate_realtimeupdate_tripupdate").rowcount == 0
        assert RealTimeUpdate.query.count() == 1

        config["nb_days_to_keep"] = DEFAULT_DAYS_TO_KEEP_RT_UPDATE

        # Put a realistic date to RealTimeUpdate object, but just outside the limit where it should be purged
        RealTimeUpdate.query.first().created_at = date.today() - timedelta(days=DEFAULT_DAYS_TO_KEEP_RT_UPDATE)
        purge_rt_update(config)

        assert TripUpdate.query.count() == 0
        assert VehicleJourney.query.count() == 0
        assert StopTimeUpdate.query.count() == 0
        assert db.session.execute("select * from associate_realtimeupdate_tripupdate").rowcount == 0
        assert RealTimeUpdate.query.count() == 1


def test_no_purge_different_contributor(mock_rabbitmq):
    with app.app_context():
        create_rt_update_and_trip_update(
            "70866ce8-0638-4fa1-8556-1ddfa22d09d3",
            COTS_CONTRIBUTOR_ID,
            ConnectorType.gtfs_rt.value,
            VJ_ID,
            TRIP_ID,
            date.today() - timedelta(days=DEFAULT_DAYS_TO_KEEP_RT_UPDATE + 1),
        )
        db.session.commit()

        # Check there's really something before purge
        assert TripUpdate.query.count() == 1
        assert RealTimeUpdate.query.count() == 1

        config = {
            "contributor": "another_contributor",
            "nb_days_to_keep": DEFAULT_DAYS_TO_KEEP_TRIP_UPDATE,
        }
        purge_trip_update(config)

        assert TripUpdate.query.count() == 1
        assert VehicleJourney.query.count() == 1
        assert db.session.execute("select * from associate_realtimeupdate_tripupdate").rowcount == 1
        assert RealTimeUpdate.query.count() == 1

        config["nb_days_to_keep"] = DEFAULT_DAYS_TO_KEEP_RT_UPDATE
        RealTimeUpdate.query.first().created_at = date.today() - timedelta(
            days=DEFAULT_DAYS_TO_KEEP_RT_UPDATE + 1
        )
        purge_rt_update(config)

        assert TripUpdate.query.count() == 1
        assert VehicleJourney.query.count() == 1
        assert db.session.execute("select * from associate_realtimeupdate_tripupdate").rowcount == 1
        assert RealTimeUpdate.query.count() == 1


def test_no_purge(mock_rabbitmq):
    with app.app_context():
        date_all_purge = date.today() - timedelta(days=DEFAULT_DAYS_TO_KEEP_RT_UPDATE + 1)
        create_rt_update_and_trip_update(
            "70866ce8-0638-4fa1-8556-1ddfa22d09d3",
            COTS_CONTRIBUTOR_ID,
            ConnectorType.gtfs_rt.value,
            VJ_ID,
            TRIP_ID,
            date_all_purge,
        )
        db.session.commit()

        # Check there's really something before purge
        assert TripUpdate.query.count() == 1
        assert RealTimeUpdate.query.count() == 1

        config = {
            "contributor": "another_contributor",
            "nb_days_to_keep": 0,
        }

        purge_trip_update(config)
        RealTimeUpdate.query.first().created_at = date_all_purge
        purge_rt_update(config)

        assert TripUpdate.query.count() == 1
        assert VehicleJourney.query.count() == 1
        assert db.session.execute("select * from associate_realtimeupdate_tripupdate").rowcount == 1
        assert RealTimeUpdate.query.count() == 1
