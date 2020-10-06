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
import datetime
import logging

import six
from google.protobuf.text_format import Parse as ParseProtoText, ParseError
from google.protobuf.message import DecodeError

from kirin import gtfs_realtime_pb2
from kirin.core import model
from kirin.core.abstract_builder import AbstractKirinModelBuilder
from kirin.core.types import ModificationType, get_higher_status, get_effect_by_stop_time_status, ConnectorType
from kirin.exceptions import InternalException, InvalidArguments
from kirin.utils import make_rt_update, floor_datetime, to_navitia_utc_str, set_rtu_status_ko, manage_db_error
from kirin.utils import record_internal_failure
from kirin import app
import itertools
import calendar


class KirinModelBuilder(AbstractKirinModelBuilder):
    def __init__(self, contributor):
        super(KirinModelBuilder, self).__init__(contributor, is_new_complete=False)
        self.log = logging.LoggerAdapter(logging.getLogger(__name__), extra={"contributor": self.contributor.id})
        self.period_filter_tolerance = datetime.timedelta(hours=3)  # TODO better period handling
        self.stop_code_key = "source"  # TODO conf
        self.instance_data_pub_date = self.navitia.get_publication_date()

    def build_rt_update(self, input_raw):
        # create a raw gtfs-rt obj, save the raw protobuf into the db
        proto = gtfs_realtime_pb2.FeedMessage()
        log_dict = {}
        try:
            proto.ParseFromString(input_raw)
        except DecodeError:
            # We save the non-decodable flux gtfs-rt
            rt_update = manage_db_error(
                input_raw.encode("string_escape", "ignore"),  # protect for PostgreSQL "Text" type
                ConnectorType.gtfs_rt.value,
                contributor_id=self.contributor.id,
                error="invalid protobuf",
                is_reprocess_same_data_allowed=False,
            )
            return rt_update, log_dict

        feed = six.binary_type(proto)  # temp, for the moment, we save the protobuf as text
        rt_update = make_rt_update(
            feed, connector_type=self.contributor.connector_type, contributor_id=self.contributor.id
        )
        rt_update.proto = proto

        return rt_update, log_dict

    def build_trip_updates(self, rt_update):
        """
        parse the gtfs-rt protobuf stored in the rt_update object (in Kirin db)
        and return a list of trip updates

        The TripUpdates are not associated with the RealTimeUpdate at this point
        """
        log_dict = {}

        if not hasattr(rt_update, "proto"):
            # GOTCHA: should match error message from build_rt_update(), as it will override it.
            # It allows manage_db_error() to work as expected.
            # TODO: improve that, but things are quite intricate for error/log management here.
            raise InvalidArguments("invalid protobuf")

        proto = rt_update.proto

        input_data_time = datetime.datetime.utcfromtimestamp(proto.header.timestamp)
        log_dict.update({"input_timestamp": input_data_time})

        self.log.debug(
            "Start processing GTFS-rt: timestamp = {} ({})".format(proto.header.timestamp, input_data_time)
        )

        trip_updates = []

        for entity in proto.entity:
            if not entity.trip_update:
                continue
            tu = self._make_trip_updates(entity.trip_update, input_data_time=input_data_time)
            trip_updates.extend(tu)

        if not trip_updates:
            msg = "No information for this gtfs-rt with timestamp: {}".format(proto.header.timestamp)
            set_rtu_status_ko(rt_update, msg, is_reprocess_same_data_allowed=False)
            self.log.warning(msg)

        log_dict = {}
        return trip_updates, log_dict

    def _get_stop_code(self, nav_stop):
        for c in nav_stop.get("codes", []):
            if c["type"] == self.stop_code_key:
                return c["value"]

    def _make_trip_updates(self, input_trip_update, input_data_time):
        """
        If trip_update.stop_time_updates is not a strict ending subset of vj.stop_times we reject the trip update
        On the other hand:
        1. For the stop point present in trip_update.stop_time_updates we create a trip_update merging
        informations with that of navitia stop
        2. For the first stop point absent in trip_update.stop_time_updates we create a stop_time_update
        with no delay for that stop
        """
        vjs = self._get_navitia_vjs(input_trip_update.trip, input_data_time=input_data_time)
        trip_updates = []
        for vj in vjs:
            trip_update = model.TripUpdate(vj=vj, contributor_id=self.contributor.id)
            highest_st_status = ModificationType.none.name

            is_tu_valid = True
            vj_stop_order = len(vj.navitia_vj.get("stop_times", [])) - 1
            for vj_stop, tu_stop in itertools.izip_longest(
                reversed(vj.navitia_vj.get("stop_times", [])), reversed(input_trip_update.stop_time_update)
            ):
                if vj_stop is None:
                    is_tu_valid = False
                    break

                vj_stop_point = vj_stop.get("stop_point")
                if vj_stop_point is None:
                    is_tu_valid = False
                    break

                if tu_stop is not None:
                    if self._get_stop_code(vj_stop_point) != tu_stop.stop_id:
                        is_tu_valid = False
                        break

                    tu_stop.stop_sequence = vj_stop_order
                    st_update = _make_stoptime_update(tu_stop, vj_stop_point)
                    if st_update is not None:
                        trip_update.stop_time_updates.append(st_update)
                else:
                    # Initialize stops absent in trip_updates but present in vj
                    st_update = _init_stop_update(vj_stop_point, vj_stop_order)
                    if st_update is not None:
                        trip_update.stop_time_updates.append(st_update)

                for status in [st_update.departure_status, st_update.arrival_status]:
                    highest_st_status = get_higher_status(highest_st_status, status)
                vj_stop_order -= 1

            if is_tu_valid:
                # Since vj.stop_times are managed in reversed order, we re sort stop_time_updates by order.
                trip_update.stop_time_updates.sort(cmp=lambda x, y: cmp(x.order, y.order))
                trip_update.effect = get_effect_by_stop_time_status(highest_st_status)
                trip_updates.append(trip_update)
            else:
                self.log.warning(
                    "stop_time_update do not match with stops in navitia for trip : {} timestamp: {}".format(
                        input_trip_update.trip.trip_id, calendar.timegm(input_data_time.utctimetuple())
                    )
                )
                record_internal_failure(
                    "stop_time_update do not match with stops in navitia", contributor=self.contributor.id
                )
                del trip_update.stop_time_updates[:]

        return trip_updates

    def __repr__(self):
        """Allow this class to be cacheable"""
        return "{}.{}.{}".format(self.__class__, self.navitia.url, self.instance_data_pub_date)

    @app.cache.memoize(timeout=1200)
    def _make_db_vj(self, vj_source_code, since_dt, until_dt):
        """
        Search for navitia's vehicle journeys with given code, in the period provided
        :param vj_source_code: the code to search for
        :param since_dt: naive UTC datetime that starts the search period.
            Typically the supposed datetime of first base-schedule stop_time.
        :param until_dt: naive UTC datetime that ends the search period.
            Typically the supposed datetime of last base-schedule stop_time.
        """
        if since_dt.tzinfo is not None or until_dt.tzinfo is not None:
            raise InternalException("Invalid datetime provided: must be naive (and UTC)")
        navitia_vjs = self.navitia.vehicle_journeys(
            q={
                "filter": "vehicle_journey.has_code({}, {})".format(self.stop_code_key, vj_source_code),
                "since": to_navitia_utc_str(since_dt),
                "until": to_navitia_utc_str(until_dt),
                "depth": "2",  # we need this depth to get the stoptime's stop_area
            }
        )

        if not navitia_vjs:
            self.log.info(
                "impossible to find vj {t} on [{s}, {u}]".format(t=vj_source_code, s=since_dt, u=until_dt)
            )
            record_internal_failure("missing vj", contributor=self.contributor.id)
            return []

        if len(navitia_vjs) > 1:
            vj_ids = [vj.get("id") for vj in navitia_vjs]
            self.log.info(
                "too many vjs found for {t} on [{s}, {u}]: {ids}".format(
                    t=vj_source_code, s=since_dt, u=until_dt, ids=vj_ids
                )
            )
            record_internal_failure("duplicate vjs", contributor=self.contributor.id)
            return []

        nav_vj = navitia_vjs[0]

        try:
            vj = model.VehicleJourney(nav_vj, since_dt, until_dt)
            return [vj]
        except Exception as e:
            self.log.exception("Error while creating kirin VJ of {}: {}".format(nav_vj.get("id"), e))
            record_internal_failure("Error while creating kirin VJ", contributor=self.contributor.id)
            return []

    def _get_navitia_vjs(self, trip, input_data_time):
        vj_source_code = trip.trip_id

        since_dt = floor_datetime(input_data_time - self.period_filter_tolerance)
        until_dt = floor_datetime(input_data_time + self.period_filter_tolerance + datetime.timedelta(hours=1))
        self.log.debug("searching for vj {} on [{}, {}] in navitia".format(vj_source_code, since_dt, until_dt))

        return self._make_db_vj(vj_source_code, since_dt, until_dt)


def _init_stop_update(nav_stop, stop_sequence):
    st_update = model.StopTimeUpdate(
        nav_stop,
        departure_delay=None,
        arrival_delay=None,
        dep_status="none",
        arr_status="none",
        order=stop_sequence,
    )
    return st_update


def _make_stoptime_update(input_st_update, nav_stop):
    # TODO handle delay uncertainty
    # TODO handle schedule_relationship
    def read_delay(st_event):
        if st_event and st_event.delay:
            return datetime.timedelta(seconds=st_event.delay)

    dep_delay = read_delay(input_st_update.departure)
    arr_delay = read_delay(input_st_update.arrival)
    dep_status = ModificationType.none.name if dep_delay is None else ModificationType.update.name
    arr_status = ModificationType.none.name if arr_delay is None else ModificationType.update.name
    st_update = model.StopTimeUpdate(
        nav_stop,
        departure_delay=dep_delay,
        arrival_delay=arr_delay,
        dep_status=dep_status,
        arr_status=arr_status,
        order=input_st_update.stop_sequence,
    )

    return st_update
