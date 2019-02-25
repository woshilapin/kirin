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

from __future__ import absolute_import, print_function, division
import logging
from datetime import timedelta

import jmespath

from kirin.utils import record_internal_failure
from kirin.exceptions import ObjectNotFound
from abc import ABCMeta
import six
from kirin.core import model
from enum import Enum

TRAIN_ID_FORMAT = 'OCE:SN:{}'
SNCF_SEARCH_MARGIN = timedelta(hours=1)


class TripStatus(Enum):
    AJOUTEE = 1,
    SUPPRIMEE = 2,
    PERTURBEE = 3


def make_navitia_empty_vj(headsign):
    headsign = TRAIN_ID_FORMAT.format(headsign)
    return {"id": headsign, "trip": {"id": headsign}}


def to_navitia_str(dt):
    """
    format a datetime to a navitia-readable str
    """
    return dt.strftime("%Y%m%dT%H%M%S%z")


def headsigns(str_headsign):
    """
    we remove leading 0 for the headsigns and handle the train's parity.
    The parity is the number after the '/', it gives an alternative train number.

    >>> headsigns('2038')
    ['2038']
    >>> headsigns('002038')
    ['2038']
    >>> headsigns('002038/12')
    ['2038', '2012']
    >>> headsigns('2038/3')
    ['2038', '2033']
    >>> headsigns('2038/123')
    ['2038', '2123']
    >>> headsigns('2038/12345')
    ['2038', '12345']

    """
    h = str_headsign.lstrip('0')
    if '/' not in h:
        return [h]
    signs = h.split('/', 1)
    alternative_headsign = signs[0][:-len(signs[1])] + signs[1]
    return [signs[0], alternative_headsign]


def get_navitia_stop_time_sncf(cr, ci, ch, nav_vj):
    nav_external_code = "{cr}-{ci}-{ch}".format(cr=cr, ci=ci, ch=ch)

    nav_stop_times = jmespath.search(
        'stop_times[? stop_point.stop_area.codes[? value==`{nav_ext_code}` && type==`CR-CI-CH`]]'.format(
            nav_ext_code=nav_external_code),
        nav_vj)

    log_dict = None
    if not nav_stop_times:
        log_dict = {'log': 'missing stop point', 'stop_point_code': nav_external_code}
        return None, log_dict

    if len(nav_stop_times) > 1:
        log_dict = {'log': 'duplicate stops', 'stop_point_code': nav_external_code}

    return nav_stop_times[0], log_dict


class AbstractSNCFKirinModelBuilder(six.with_metaclass(ABCMeta, object)):

    def __init__(self, nav, contributor=None):
        self.navitia = nav
        self.contributor = contributor

    def _get_navitia_vjs(self, headsign_str, utc_since_dt, utc_until_dt, is_added_trip=False):
        """
        Search for navitia's vehicle journeys with given headsigns, in the period provided
        :param utc_since_dt: UTC datetime that starts the search period.
            Typically the supposed datetime of first base-schedule stop_time.
        :param utc_until_dt: UTC datetime that ends the search period.
            Typically the supposed datetime of last base-schedule stop_time.
        """
        log = logging.getLogger(__name__)

        vjs = {}
        # to get the date of the vj we use the start/end of the vj + some tolerance
        # since the SNCF data and navitia data might not be synchronized
        extended_since_dt = utc_since_dt - SNCF_SEARCH_MARGIN
        extended_until_dt = utc_until_dt + SNCF_SEARCH_MARGIN

        # using a set to deduplicate
        # one headsign_str (ex: "96320/1") can lead to multiple headsigns (ex: ["96320", "96321"])
        # but most of the time (if not always) they refer to the same VJ
        # (the VJ switches headsign along the way).
        # So we do one VJ search for each headsign to ensure we get it, then deduplicate VJs
        for train_number in headsigns(headsign_str):

            log.debug('searching for vj {} during period [{} - {}] in navitia'.format(
                            train_number, extended_since_dt, extended_until_dt))
            # Don't call navitia for an added trip ("statutOperationnel" == "AJOUTEE")
            if not is_added_trip:
                navitia_vjs = self.navitia.vehicle_journeys(q={
                    'headsign': train_number,
                    'since': to_navitia_str(extended_since_dt),
                    'until': to_navitia_str(extended_until_dt),
                    'depth': '2',  # we need this depth to get the stoptime's stop_area
                    'show_codes': 'true'  # we need the stop_points CRCICH codes
                })

                if not navitia_vjs:
                    logging.getLogger(__name__).info('impossible to find train {t} on [{s}, {u}['
                                                     .format(t=train_number,
                                                             s=extended_since_dt,
                                                             u=extended_until_dt))
                    record_internal_failure('missing train', contributor=self.contributor)
            else:
                navitia_vjs = [make_navitia_empty_vj(train_number)]

            for nav_vj in navitia_vjs:

                try:
                    vj = model.VehicleJourney(nav_vj, extended_since_dt, extended_until_dt, vj_start_dt=utc_since_dt)
                    vjs[nav_vj['id']] = vj
                except Exception as e:
                    logging.getLogger(__name__).exception(
                        'Error while creating kirin VJ of {}: {}'.format(nav_vj.get('id'), e))
                    record_internal_failure('Error while creating kirin VJ', contributor=self.contributor)

        if not vjs:
            raise ObjectNotFound('no train found for headsign(s) {}'.format(headsign_str))

        return vjs.values()
