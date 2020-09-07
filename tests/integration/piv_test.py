# coding: utf8
#
# Copyright (c) 2001-2020, Canal TP and/or its affiliates. All rights reserved.
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

import pytest

from kirin import app
from kirin.core.model import RealTimeUpdate, TripUpdate, StopTimeUpdate
from tests.check_utils import api_post
from tests import mock_navitia
from tests.integration.conftest import PIV_CONTRIBUTOR


@pytest.fixture(scope="function", autouse=True)
def navitia(monkeypatch):
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


def test_piv_post_wrong_data():
    """
    simple json post on the api
    """
    res, status = api_post("/piv/{}".format(PIV_CONTRIBUTOR), check=False, data="{}")

    # For now, no check on data
    # TODO xfail: check and change test
    assert status == 200
    assert "PIV feed processed" in res.get("message")


def test_piv_post_no_data():
    """
    Post with a missing id or missing data returns an error 400
    Post with an unknown id returns an error 404
    """

    def post_and_check(url, expected_status, expected_message, expected_error):
        resp, status = api_post(url, check=False)
        assert status == expected_status
        assert expected_message in resp.get("message")
        if expected_error:
            assert expected_error == resp.get("error")

        with app.app_context():
            assert len(RealTimeUpdate.query.all()) == 0
            assert len(TripUpdate.query.all()) == 0
            assert len(StopTimeUpdate.query.all()) == 0

    post_and_check("/piv/", 405, "The method is not allowed for the requested URL.", None)
    post_and_check("/piv/{}".format(PIV_CONTRIBUTOR), 400, "invalid arguments", "no piv data provided")
    post_and_check("/piv/unknown_id", 404, "Contributor 'unknown_id' not found", None)
