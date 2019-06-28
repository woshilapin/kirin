# coding=utf-8

#  Copyright (c) 2001-2015, Canal TP and/or its affiliates. All rights reserved.
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

from kirin import gtfs_realtime_pb2
import calendar
from datetime import datetime
import pytz

def unix_time(y, m, d, h, min, s):
    while min >= 60:
        h += 1
        min -= 60
    tz = pytz.timezone("Europe/Paris")
    d = datetime(y, m, d, h, min, s, 0, tz)
    return calendar.timegm(d.utctimetuple())

def make_96231_20150728_0():
    """gtfs rt feed corresponding to cots_train_96231_delayed.json"""

    message = gtfs_realtime_pb2.FeedMessage()

    message.header.incrementality = gtfs_realtime_pb2.FeedHeader.DIFFERENTIAL

    entity = message.entity.add()
    entity.id = "96231_2015-07-28_0"
    trip_update = entity.trip_update

    trip = trip_update.trip
    trip.trip_id = "vehicle_journey:OCETrainTER-87212027-85000109-3:15554"
    trip.start_date = "20150728"
    trip.schedule_relationship = gtfs_realtime_pb2.TripDescriptor.SCHEDULED

    # Strasbourg
    stop_time = trip_update.stop_time_update.add()
    stop_time.stop_id = "stop_point:OCE:SP:TrainTER-87212027"
    stop_time.arrival.time = unix_time(2015, 07, 28, 17, 21, 0)
    stop_time.departure.time = unix_time(2015, 07, 28, 17, 21, 0)
    stop_time.stop_sequence = 1

    # Sélestat
    stop_time = trip_update.stop_time_update.add()
    stop_time.stop_id = "stop_point:OCE:SP:TrainTER-87214056"
    stop_time.arrival.time = unix_time(2015, 07, 28, 17, 38, 0)
    stop_time.departure.time = unix_time(2015, 07, 28, 17, 40 + 15, 0)
    stop_time.stop_sequence = 2

    # Colmar
    stop_time = trip_update.stop_time_update.add()
    stop_time.stop_id = "stop_point:OCE:SP:TrainTER-87182014"
    stop_time.arrival.time = unix_time(2015, 07, 28, 17, 51 + 15, 0)
    stop_time.departure.time = unix_time(2015, 07, 28, 17, 53 + 15, 0)
    stop_time.stop_sequence = 3

    # Mulhouse
    stop_time = trip_update.stop_time_update.add()
    stop_time.stop_id = "stop_point:OCE:SP:TrainTER-87182063"
    stop_time.arrival.time = unix_time(2015, 07, 28, 18, 14 + 15, 0)
    stop_time.departure.time = unix_time(2015, 07, 28, 18, 16 + 15, 0)
    stop_time.stop_sequence = 4

    # St-Louis
    stop_time = trip_update.stop_time_update.add()
    stop_time.stop_id = "stop_point:OCE:SP:TrainTER-87182139"
    stop_time.arrival.time = unix_time(2015, 07, 28, 18, 30 + 15, 0)
    stop_time.departure.time = unix_time(2015, 07, 28, 18, 31 + 15, 0)
    stop_time.stop_sequence = 6

    # Basel-SBB
    stop_time = trip_update.stop_time_update.add()
    stop_time.stop_id = "stop_point:OCE:SP:TrainTER-85000109"
    stop_time.arrival.time = unix_time(2015, 07, 28, 18, 39 + 15, 0)
    stop_time.departure.time = unix_time(2015, 07, 28, 18, 39, 0)# ?
    stop_time.stop_sequence = 7

    return message
