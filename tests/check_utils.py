# Copyright (c) 2001-2015, Canal TP and/or its affiliates. All rights reserved.
#
# This file is part of Navitia,
#     the software to build cool stuff with public transport.
#
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

from kirin import app
import json


def api_get(url, display=False, *args, **kwargs):
    """
    call api, check response status code, and return json as dict
    """
    tester = app.test_client()
    resp = tester.get(url, *args, **kwargs)

    assert resp.status_code == 200
    return _to_json(resp.data, display)


def api_post(url, display=False, check=True, *args, **kwargs):
    """
    call api, check response status code, and return json as dict
    """
    tester = app.test_client()
    resp = tester.post(url, *args, **kwargs)

    if check:
        assert resp.status_code == 200
        return _to_json(resp.data, display)
    else:
        return _to_json(resp.data, display), resp.status_code


def _to_json(data, display):
    assert data
    json_response = json.loads(data)

    return json_response
