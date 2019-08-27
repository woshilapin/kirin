# coding=utf-8

# Copyright (c) 2001-2019, Canal TP and/or its affiliates. All rights reserved.
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

from kirin import app, db
from kirin.core import model
from flask import json
import pytest


@pytest.yield_fixture
def test_client():
    app.testing = True
    with app.app_context(), app.test_client() as tester:
        yield tester


def test_get_contributor_end_point(test_client):
    assert test_client.get("/contributors").status_code == 200


@pytest.fixture
def with_contributors():
    db.session.add_all(
        [
            model.Contributor("realtime.sherbrook", "ca", "gtfs-rt", "my_token", "http://feed.url"),
            model.Contributor("realtime.paris", "idf", "gtfs-rt", "my_other_token", "http://otherfeed.url"),
        ]
    )
    db.session.commit()


def test_get_contributors(test_client, with_contributors):
    resp = test_client.get("/contributors")
    assert resp.status_code == 200

    contribs = json.loads(resp.data)
    assert len(contribs) == 2

    ids = [c["id"] for c in contribs]
    ids.sort()

    assert ids == ["realtime.paris", "realtime.sherbrook"]


def test_get_contributors_with_specific_id(test_client, with_contributors):
    resp = test_client.get("/contributors/realtime.paris")
    assert resp.status_code == 200

    contrib = json.loads(resp.data)
    assert len(contrib) == 1
    assert contrib[0]["id"] == "realtime.paris"
    assert contrib[0]["navitia_coverage"] == "idf"
    assert contrib[0]["connector_type"] == "gtfs-rt"
    assert contrib[0]["navitia_token"] == "my_other_token"
    assert contrib[0]["feed_url"] == "http://otherfeed.url"


def test_get_contributors_with_wrong_id(test_client, with_contributors):
    resp = test_client.get("/contributors/this_id_doesnt_exist")
    assert resp.status_code == 200

    contrib = json.loads(resp.data)
    assert len(contrib) == 0


def test_post_new_contributor(test_client):
    new_contrib = {
        "id": "realtime.tokyo",
        "navitia_coverage": "jp",
        "navitia_token": "blablablabla",
        "feed_url": "http://nihongo.jp",
        "connector_type": "gtfs-rt",
    }
    resp = test_client.post("/contributors", json=new_contrib)
    assert resp.status_code == 201

    contrib = db.session.query(model.Contributor).filter(model.Contributor.id == "realtime.tokyo").first()
    assert contrib.id == "realtime.tokyo"
    assert contrib.navitia_coverage == "jp"
    assert contrib.connector_type == "gtfs-rt"
    assert contrib.navitia_token == "blablablabla"
    assert contrib.feed_url == "http://nihongo.jp"


def test_post_new_partial_contributor(test_client):
    new_contrib = {"id": "realtime.tokyo", "navitia_coverage": "jp", "connector_type": "gtfs-rt"}
    resp = test_client.post("/contributors", json=new_contrib)
    assert resp.status_code == 201

    contrib = db.session.query(model.Contributor).filter(model.Contributor.id == "realtime.tokyo").first()
    assert contrib.id == "realtime.tokyo"
    assert contrib.navitia_coverage == "jp"
    assert contrib.connector_type == "gtfs-rt"
    assert contrib.navitia_token == None
    assert contrib.feed_url == None


def test_post_contributor_with_wrong_connector_type(test_client):
    new_contrib = {"id": "realtime.tokyo", "coverage": "jp", "connector_type": "THIS-TYPE-DOES-NOT-EXIST"}
    resp = test_client.post("/contributors", json=new_contrib)
    assert resp.status_code == 400


def test_post_2_contributors_with_same_id_should_fail(test_client):
    resp = test_client.post(
        "/contributors", json={"id": "realtime.test", "navitia_coverage": "jp", "connector_type": "gtfs-rt"}
    )
    resp = test_client.post(
        "/contributors", json={"id": "realtime.test", "navitia_coverage": "fr", "connector_type": "cots"}
    )
    assert resp.status_code == 400


def test_post_contributor_with_wrong_connector_type_should_fail(test_client):
    resp = test_client.post("/contributors", json={
        "id": "realtime.tokyo",
        "navitia_coverage": "jp",
        "connector_type": "THIS-TYPE-DOES-NOT-EXIST",
    })
    assert resp.status_code == 400


def test_post_new_valid_contributor_with_unknown_parameter_should_work(test_client):
    resp = test_client.post("/contributors", json={
        "UNKNOWN_PARAM": "gibberish",
        "id": "realtime.tokyo",
        "navitia_coverage": "jp",
        "connector_type": "gtfs-rt",
    })
    assert resp.status_code == 201

