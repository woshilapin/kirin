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
import os

import six

from kirin import app, db
from kirin.core import model
import pytest
import flask_migrate

from kirin.core.types import ConnectorType

COTS_CONTRIBUTOR_ID = "rt.tchoutchou"
PIV_CONTRIBUTOR_ID = "rt.piv"
GTFS_CONTRIBUTOR_ID = "rt.vroumvroum"
COTS_CONTRIBUTOR_DB_ID = "rt.tchoutchou_db"
PIV_CONTRIBUTOR_DB_ID = "rt.piv_db"
GTFS_CONTRIBUTOR_DB_ID = "rt.vroumvroum_db"


@pytest.yield_fixture(scope="module", autouse=True)
def bdd(init_flask_db):
    """
    All tests under this module will have a database
     with an up to date scheme

    At the end of the module the database scheme will be downgraded and upgraded again
    in the next module to test the database migrations
    """
    with app.app_context():
        flask_migrate.Migrate(app, db)
        migration_dir = os.path.join(os.path.dirname(__file__), "..", "..", "migrations")
        flask_migrate.upgrade(directory=migration_dir)

    yield

    with app.app_context():
        flask_migrate.downgrade(revision="base", directory=migration_dir)


def clean_db():
    """
    before all tests the database is cleared
    """
    with app.app_context():
        tables = [six.text_type(table) for table in db.metadata.sorted_tables]
        db.session.execute("TRUNCATE {} CASCADE;".format(", ".join(tables)))
        db.session.commit()

        # Add two contributors of each in the table
        db.session.add_all(
            [
                model.Contributor(
                    COTS_CONTRIBUTOR_ID,
                    "sncf",
                    ConnectorType.cots.value,
                    "cots_token",
                    "cots_feed_url",
                    10,
                    True,
                ),
                model.Contributor(
                    PIV_CONTRIBUTOR_ID,
                    "sncf_piv",
                    ConnectorType.piv.value,
                    "piv_token",
                    "piv_feed_url",
                    10,
                    True,
                ),
                model.Contributor(
                    GTFS_CONTRIBUTOR_ID,
                    "sherbrooke",
                    ConnectorType.gtfs_rt.value,
                    "gtfs-rt_token",
                    "gtfs-rt_feed_url",
                    1,
                    True,
                ),
                model.Contributor(
                    COTS_CONTRIBUTOR_DB_ID, "idfm", ConnectorType.cots.value, "cots_db_token", "cots_db_feed_url"
                ),
                model.Contributor(
                    PIV_CONTRIBUTOR_DB_ID, "tn", ConnectorType.piv.value, "piv_db_token", "piv_db_feed_url"
                ),
                model.Contributor(
                    GTFS_CONTRIBUTOR_DB_ID,
                    "laval",
                    ConnectorType.gtfs_rt.value,
                    "gtfs-rt_db_token",
                    "gtfs-rt_db_feed_url",
                    30,
                ),
            ]
        )
        db.session.commit()


@pytest.fixture(scope="function", autouse=True)
def clean_db_fixture():
    clean_db()


@pytest.fixture(scope="function")
def mock_navitia_fixture(monkeypatch):
    from .. import mock_navitia

    """
    Mock all calls to navitia for this fixture
    """
    monkeypatch.setattr("navitia_wrapper._NavitiaWrapper.query", mock_navitia.mock_navitia_query)


@pytest.fixture(scope="function")
def mock_rabbitmq(monkeypatch):
    """
    Mock all publishes to navitia for this fixture
    """
    from mock import MagicMock

    mock_amqp = MagicMock()
    monkeypatch.setattr("kombu.messaging.Producer.publish", mock_amqp)

    return mock_amqp
