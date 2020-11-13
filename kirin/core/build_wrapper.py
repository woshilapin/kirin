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
import socket
from collections import namedtuple

import six

import kirin
from kirin import gtfs_realtime_pb2
from kirin.core.model import TripUpdate
from kirin.core.populate_pb import convert_to_gtfsrt
from kirin.exceptions import MessageNotPublished, KirinException
from kirin.new_relic import (
    record_custom_parameter,
    is_only_warning_exception,
    is_reprocess_allowed,
)
from kirin.utils import set_rtu_status_ko, allow_reprocess_same_data, record_call, db_commit

TimeDelayTuple = namedtuple("TimeDelayTuple", ["time", "delay"])


def check_consistency(trip_update):
    """
    returns False if trip update is inconsistent
    """
    logger = logging.getLogger(__name__)
    for current_order, stu in enumerate(trip_update.stop_time_updates):
        if stu.order != current_order:
            logger.warning(
                "TripUpdate on navitia vj {nav_id} on {date} rejected: "
                "order problem [STU index ({stu_index}) != kirin index ({kirin_index})]".format(
                    nav_id=trip_update.vj.navitia_trip_id,
                    date=trip_update.vj.get_circulation_date(),
                    stu_index=stu.order,
                    kirin_index=current_order,
                )
            )
            return False
    return True


def publish(feed, contributor_id):
    """
    send RT feed to navitia
    """
    try:
        kirin.rmq_handler.publish(feed, contributor_id)

    except socket.error:
        logging.getLogger(__name__).exception(
            "impossible to publish in rabbitmq", extra={str("contributor"): contributor_id}
        )
        raise MessageNotPublished()


def handle(builder, real_time_update, trip_updates):
    """
    Receive a RealTimeUpdate with at least one TripUpdate filled with the data received
    by the connector.
    Each TripUpdate is associated with the base-schedule VehicleJourney, complete/merge realtime is done using builder
    Then persist in db, publish for Navitia
    Returns real_time_update and the log_dict
    """
    if not real_time_update:
        raise TypeError()
    id_timestamp_tuples = [(tu.vj.navitia_trip_id, tu.vj.start_timestamp) for tu in trip_updates]
    old_trip_updates = TripUpdate.find_by_dated_vjs(id_timestamp_tuples)
    for trip_update in trip_updates:
        # find if there is already a row in db
        old = next(
            (
                tu
                for tu in old_trip_updates
                if tu.vj.navitia_trip_id == trip_update.vj.navitia_trip_id
                and tu.vj.start_timestamp == trip_update.vj.start_timestamp
            ),
            None,
        )
        # merge the base schedule, the current realtime, and the new realtime
        current_trip_update = builder.merge_trip_updates(trip_update.vj.navitia_vj, old, trip_update)

        # manage and adjust consistency if possible
        if current_trip_update is not None and check_consistency(current_trip_update):
            # we have to link the current_vj_update with the new real_time_update
            # this link is done quite late to avoid too soon persistence of trip_update by sqlalchemy
            current_trip_update.real_time_updates.append(real_time_update)

    db_commit(real_time_update)

    feed = convert_to_gtfsrt(real_time_update.trip_updates, gtfs_realtime_pb2.FeedHeader.DIFFERENTIAL)
    feed_str = feed.SerializeToString()
    publish(feed_str, builder.contributor.id)

    data_time = datetime.datetime.utcfromtimestamp(feed.header.timestamp)
    log_dict = {
        "contributor": builder.contributor.id,
        "timestamp": data_time,
        "trip_update_count": len(feed.entity),
        "size": len(feed_str),
    }
    # After merging trip_updates information of connector realtime, navitia and kirin database, if there is no new
    # information destined to navitia, update real_time_update with status = 'KO' and a proper error message.
    if not real_time_update.trip_updates and real_time_update.status == "OK":
        msg = "No new information destined to navitia for this {}".format(real_time_update.connector)
        set_rtu_status_ko(real_time_update, msg, is_reprocess_same_data_allowed=False)
        logging.getLogger(__name__).warning(
            "RealTimeUpdate id={}: {}".format(real_time_update.id, msg), extra=log_dict
        )
        db_commit(real_time_update)

    return real_time_update, log_dict


def wrap_build(builder, input_raw):
    """
    Function wrapping the processing of realtime information of an external feed
    This manages errors/logger/newrelic
    :param builder: the KirinModelBuilder to be called (must inherit from abstract_builder.AbstractKirinModelBuilder)
    :param input_raw: the feed to process
    """
    contributor = builder.contributor
    start_datetime = datetime.datetime.utcnow()
    rt_update = None
    log_dict = {"contributor": contributor.id}
    record_custom_parameter("contributor", contributor.id)
    status = "OK"

    try:
        # create a raw rt_update obj, save the raw_input into the db
        rt_update, rtu_log_dict = builder.build_rt_update(input_raw)
        log_dict.update(rtu_log_dict)

        # raw_input is interpreted
        trip_updates, tu_log_dict = builder.build_trip_updates(rt_update)
        log_dict.update(tu_log_dict)

        # finally confront to previously existing information (base_schedule, previous real-time)
        _, handler_log_dict = handle(builder, rt_update, trip_updates)
        log_dict.update(handler_log_dict)

    except Exception as e:
        status = "warning" if is_only_warning_exception(e) else "failure"
        allow_reprocess = is_reprocess_allowed(e)

        if rt_update is not None:
            error = e.data["error"] if (isinstance(e, KirinException) and "error" in e.data) else e.message
            set_rtu_status_ko(rt_update, error, is_reprocess_same_data_allowed=allow_reprocess)
            db_commit(rt_update)
        else:
            # rt_update is not built, make sure reprocess is allowed
            allow_reprocess_same_data(contributor.id)

        log_dict.update({"exc_summary": six.text_type(e), "reason": e})

        record_custom_parameter("reason", e)  # using __str__() here to have complete details
        raise  # filters later for errors in newrelic's summary (auto for flask)

    finally:
        log_dict.update({"duration": (datetime.datetime.utcnow() - start_datetime).total_seconds()})
        record_call(status, **log_dict)
        if status == "OK":
            logging.getLogger(__name__).info(status, extra=log_dict)
        elif status == "warning":
            logging.getLogger(__name__).warning(status, extra=log_dict)
        else:
            logging.getLogger(__name__).error(status, extra=log_dict)
