# coding=utf-8

# Copyright (c) 2001-2018, Canal TP and/or its affiliates. All rights reserved.
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
import flask
from flask.globals import current_app
import navitia_wrapper
import logging

from kirin.abstract_sncf_resource import AbstractSNCFResource
from kirin.cots import KirinModelBuilder
from kirin.exceptions import InvalidArguments
from kirin.core import model
from kirin.core.types import ConnectorType


def get_cots(req):
    """
    get COTS stream, for the moment, it's the raw json
    """
    if not req.data:
        raise InvalidArguments("no COTS data provided")
    return req.data


class Cots(AbstractSNCFResource):
    def __init__(self):

        url = current_app.config[str("NAVITIA_URL")]

        # TODO :
        #  remove config from file
        if "NAVITIA_INSTANCE" in current_app.config and current_app.config[str("NAVITIA_INSTANCE")]:
            instance = current_app.config[str("NAVITIA_INSTANCE")]
            token = current_app.config[str("NAVITIA_TOKEN")]
            contributor_id = current_app.config[str("COTS_CONTRIBUTOR")]
        else:
            contributor = model.Contributor.find_by_connector_type(ConnectorType.cots.value)
            if len(contributor) > 1:
                logging.getLogger(__name__).warning(
                    "{n} COTS contributors found in db - {id} taken into account ".format(
                        n=len(contributor), id=contributor[0].id
                    )
                )
            instance = contributor[0].navitia_coverage
            token = contributor[0].navitia_token
            contributor_id = contributor[0].id

        super(Cots, self).__init__(
            navitia_wrapper.Navitia(url=url, token=token).instance(instance),
            current_app.config.get(str("NAVITIA_TIMEOUT"), 5),
            contributor_id,
            KirinModelBuilder,
        )

    def post(self):
        raw_json = get_cots(flask.globals.request)
        return self.process_post(raw_json, "cots", is_new_complete=True)
