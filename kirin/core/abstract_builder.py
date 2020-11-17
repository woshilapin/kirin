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

from abc import ABCMeta
from typing import Tuple, List, Dict, Any

import navitia_wrapper
import six
from flask import current_app

from kirin import redis_client
from kirin.core.model import Contributor, RealTimeUpdate, TripUpdate


class AbstractKirinModelBuilder(six.with_metaclass(ABCMeta, object)):
    """
    Class expliciting what's expected and available for any KirinModelBuilder

    KirinModelBuilder are responsible for the creation of internal objects representing the realtime information
    from the feed received (before confrontation of this information with previous realtime know and base-schedule).

    This allows the KirinModelBuilder to be wrapped by wrap_build() function
    """

    def __init__(self, contributor):
        # type: (Contributor) -> None
        self.navitia = navitia_wrapper.Navitia(
            url=current_app.config.get(str("NAVITIA_URL")),
            token=contributor.navitia_token,
            timeout=current_app.config.get(str("NAVITIA_TIMEOUT"), 5),
            cache=redis_client,
            query_timeout=current_app.config.get(str("NAVITIA_QUERY_CACHE_TIMEOUT"), 600),
            pubdate_timeout=current_app.config.get(str("NAVITIA_PUBDATE_CACHE_TIMEOUT"), 600),
        ).instance(contributor.navitia_coverage)
        self.contributor = contributor

    def build_rt_update(self, input_raw):
        # type: (Any) -> Tuple[RealTimeUpdate, Dict[unicode, unicode]]
        """
        Create a wrapping object around the feed received to store it
        :return rt_update: RealTimeUpdate ORM object containing stored input_raw
        :return log_dict: dict of (k,v) to be displayed in logs and newrelic
        """
        raise NotImplementedError("Please implement this method")

    def build_trip_updates(self, rt_update):
        # type: (RealTimeUpdate) -> Tuple[List[TripUpdate], Dict[unicode, unicode]]
        """
        Convert realtime information into Kirin's internal model
        :return trip_updates: list of TripUpdates ORM objects obtained from the processing of given rt_update
        :return log_dict: dict of (k,v) to be displayed in logs and newrelic
        """
        raise NotImplementedError("Please implement this method")

    def merge_trip_updates(self, navitia_vj, db_trip_update, new_trip_update):
        # type: (Dict[unicode, Any], TripUpdate, TripUpdate) -> TripUpdate
        """
        Merges information from:
        * navitia_vj (base-schedule VJ - complete, maybe nonexistent)
        * db_trip_update (last known realtime VJ - complete, maybe nonexistent)
        * new_trip_update (VJ information extracted from incoming feed - maybe incomplete)
        Returns resulting TripUpdate:
        usually update of the last known realtime VJ, or completed version of new_trip_update
        """
        raise NotImplementedError("Please implement this method")
