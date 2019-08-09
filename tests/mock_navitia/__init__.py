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
import json
from tests.mock_navitia import (
    vj_john,
    vj_6111,
    vj_6112,
    vj_6113,
    vj_6114,
    vj_8837,
    vj_96231,
    vj_870154,
    vj_840426,
    vj_R_vj1,
    vj_R_vj2,
    vj_pass_midnight,
    vj_pass_midnight_utc,
    vj_lollipop,
    vj_bad_order,
    vj_start_midnight,
    vj_start_midnight_utc,
    st_713065,
    st_713666,
    company_1187,
    empty_company_1180,
    company_OCETH,
    st_0087_318964_BV,
    st_0087_319012_00,
    st_0087_683573_BV,
    st_0087_686667_BV,
    st_0087_751008_BV,
    physical_mode_LongDistanceTrain,
    physical_mode_Coach,
    st_0087_543009_BV,
    st_0087_215632_00,
    vj_9580,
    st_0087_191981_WL,
    vj_unknown_object,
)
import logging


mocks = [
    vj_john.response,
    vj_6111.response,
    vj_6112.response,
    vj_6113.response,
    vj_6114.response,
    vj_8837.response,
    vj_96231.response,
    vj_870154.response,
    vj_840426.response,
    vj_R_vj1.response,
    vj_R_vj2.response,
    vj_pass_midnight.response,
    vj_pass_midnight_utc.response,
    vj_lollipop.response,
    vj_bad_order.response,
    vj_start_midnight.response,
    vj_start_midnight_utc.response,
    st_713065.response,
    st_713666.response,
    company_1187.response,
    empty_company_1180.response,
    company_OCETH.response,
    st_0087_751008_BV.response,
    st_0087_686667_BV.response,
    st_0087_683573_BV.response,
    st_0087_319012_00.response,
    st_0087_318964_BV.response,
    physical_mode_LongDistanceTrain.response,
    st_0087_543009_BV.response,
    st_0087_215632_00.response,
    physical_mode_Coach.response,
    vj_unknown_object.response,
    vj_9580.response,
    st_0087_191981_WL.response,
]
_mock_navitia_call = {}
for r in mocks:
    map(lambda q: _mock_navitia_call.update({q: r}), r.queries)  # type: ignore


def mock_navitia_query(self, query, q=None):
    """
    mock the call to navitia wrapper.

    a file with the query name is looked for in the tests/fixtures dir
    """
    query_str = query
    if q:
        query_str += "?"
        sep = ""
        for param_name, param_value in q.iteritems():
            query_str += sep + param_name + "=" + param_value
            sep = "&"

    try:
        mock = _mock_navitia_call[query_str]
    except:
        logging.getLogger(__name__).error("cannot find mock for query : {}".format(query_str))
        raise

    return json.loads(mock.json_response), mock.response_code


def mock_publication_date(self):
    return "20171115T195211.961411"
