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
# IRC #navitia on freenode
# https://groups.google.com/d/forum/navitia
# www.navitia.io

from __future__ import absolute_import, print_function, unicode_literals, division

import logging
from datetime import timedelta, datetime

import jmespath
import ujson
from operator import itemgetter

from kirin.core import model
from kirin.core.abstract_builder import AbstractKirinModelBuilder
from kirin.core.types import ModificationType, TripEffect, get_higher_status, get_effect_by_stop_time_status
from kirin.exceptions import InvalidArguments, UnauthorizedValue, ObjectNotFound
from kirin.utils import make_rt_update, get_value, as_utc_naive_dt, record_internal_failure, as_duration

TRIP_PIV_ID_FORMAT = "PIV:{}"

STATUS_MAP = {"arrivee": "arrival_status", "depart": "departure_status"}
DELAY_MAP = {"arrivee": "arrival_delay", "depart": "departure_delay"}
STOP_EVENT_DATETIME_MAP = {"arrivee": "arrival", "depart": "departure"}


def _has_departure(stop):
    return get_value(stop, "depart", nullable=True) and not get_value(
        stop, "indicateurMonteeInterdite", nullable=True
    )


def _has_arrival(stop):
    return get_value(stop, "arrivee", nullable=True) and not get_value(
        stop, "indicateurDescenteInterdite", nullable=True
    )


def _retrieve_interesting_stops(list_ad):
    """
    Filter and sort "Arrets Desserte" (corresponding to stop_times in Navitia) to get only the relevant
    ones from a Navitia's perspective (stations, where travelers can hop on or hop off)
    :param list_ad: an array of "Arrets Desserte" (typically the one from the feed)
    :return: Filtered array
    Notes:  - written in a yield-fashion to switch implementation if possible, but we need random access for now
    """
    res = []
    picked_one = False
    sorted_list_stops = sorted(list_ad, key=itemgetter("rang"))
    for idx, stop in enumerate(sorted_list_stops):
        has_departure = _has_departure(stop)
        has_arrival = _has_arrival(stop)
        # At start, do not consume until there's a departure time (depart)
        if not picked_one and not has_departure:
            continue
        # exclude stop_times that have no departure nor arrival time (empty stop_times)
        if not has_departure and not has_arrival:
            continue
        # stop consuming once all following stop_times are missing arrival time
        # * if a stop_time only has departure time, travelers can only hop in, but if they are be able to
        #   hop off later because some stop_time has arrival time then the current stop_time is useful,
        #   so we keep current stop_time.
        # * if no stop_time has arrival time anymore, then stop_times are useless as traveler cannot
        #   hop off, so no point hopping in anymore, so we remove all the stop_times until the end
        #   (should not happen in practice).
        if not has_arrival:
            has_following_arrival = any(_has_arrival(follow_stop) for follow_stop in sorted_list_stops[idx:])
            if not has_following_arrival:
                break

        picked_one = True
        res.append(stop)
    return res


def _is_fully_added_stop(ad):
    """
    Check if an arretDesserte object has any event that was present in base-schedule
    (and return the opposite boolean)
    """
    for event_toggle in ["arrivee", "depart"]:
        event = get_value(ad, event_toggle, nullable=True)
        if event:
            if get_value(event, "planTransportSource", nullable=True) not in ["OPE", "PTP"]:
                return False
    return True


def _get_first_stop_base_datetime(list_ads, hour_obj_name, skip_fully_added_stops=True):
    if skip_fully_added_stops:
        s = next((s for s in list_ads if not _is_fully_added_stop(s)), None)
    else:
        s = next((s for s in list_ads), None)

    str_time = get_value(get_value(s, hour_obj_name), "dateHeure") if s else None
    return as_utc_naive_dt(str_time) if str_time else None


def _make_navitia_empty_vj(piv_key):
    trip_id = TRIP_PIV_ID_FORMAT.format(piv_key)
    return {"id": "vehicle_journey:{}".format(trip_id), "trip": {"id": trip_id}}


def _extract_navitia_stop_time(uic8, nav_vj):
    nav_stop_times = jmespath.search(
        "stop_times[? stop_point.stop_area.codes[? value=='{uic8}' && type=='source']]".format(uic8=uic8),
        nav_vj,
    )

    log_dict = None
    if not nav_stop_times:
        log_dict = {"log": "missing stop point", "stop_point_code": uic8}
        return None, log_dict

    if len(nav_stop_times) > 1:
        log_dict = {"log": "duplicate stops", "stop_point_code": uic8}

    return nav_stop_times[0], log_dict


def _check_stop_time_consistency(previous_rt_stop_time_dep, current_rt_stop_time, uic8):
    previous_rt_stop_time_dep = (
        previous_rt_stop_time_dep if previous_rt_stop_time_dep is not None else datetime.fromtimestamp(0)
    )

    rt_arrival = current_rt_stop_time.get("arrivee")
    rt_arrival = rt_arrival if rt_arrival is not None else previous_rt_stop_time_dep

    rt_departure = current_rt_stop_time.get("depart")
    rt_departure = rt_departure if rt_departure is not None else rt_arrival

    if not (rt_departure >= rt_arrival >= previous_rt_stop_time_dep):
        raise InvalidArguments("invalid cots: stop_point's({}) time is not consistent".format(uic8))


class KirinModelBuilder(AbstractKirinModelBuilder):
    def __init__(self, contributor):
        super(KirinModelBuilder, self).__init__(contributor, is_new_complete=True)

    def build_rt_update(self, input_raw):
        rt_update = make_rt_update(
            input_raw, connector_type=self.contributor.connector_type, contributor_id=self.contributor.id
        )
        log_dict = {}
        return rt_update, log_dict

    def build_trip_updates(self, rt_update):
        """
        parse the PIV raw json stored in the rt_update object (in Kirin db)
        and return a list of trip updates

        The TripUpdates are not associated with the RealTimeUpdate at this point
        """
        # assuming UTF-8 encoding for all input
        rt_update.raw_data = rt_update.raw_data.encode("utf-8")

        try:
            json = ujson.loads(rt_update.raw_data)
        except ValueError as e:
            raise InvalidArguments("invalid json: {}".format(e.message))

        if "objects" not in json:
            raise InvalidArguments('No object "objects" available in feed provided')

        dict_objects = get_value(json, "objects")
        json_train = get_value(dict_objects[0], "object")  # TODO: can we get more than 1 relevant in objects[]?
        events = get_value(json_train, "evenement", nullable=True)
        plan_transport_source = get_value(json_train, "planTransportSource", nullable=True)

        if not events and not plan_transport_source:
            raise InvalidArguments('No object "evenement" or "planTransportSource" available in feed provided')

        if events:
            event_type = [get_value(event, "type") for event in events]
            if "RETARD" not in event_type:
                raise UnauthorizedValue("Event type {} is not supported".format(event_type))
        elif plan_transport_source and plan_transport_source not in ["PTP", "OPE"]:
            raise UnauthorizedValue("planTransportSource {} is not supported".format(plan_transport_source))

        train_date = get_value(json_train, "dateCirculation")
        train_numbers = get_value(json_train, "numero")
        train_company = get_value(get_value(json_train, "operateur"), "codeOperateur")
        mode_dict = get_value(json_train, "modeTransport")
        train_mode = get_value(mode_dict, "codeMode")
        train_submode = get_value(mode_dict, "codeSousMode")
        train_typemode = get_value(mode_dict, "typeMode")
        piv_key = "{d}:{n}:{c}:{m}:{s}:{t}".format(
            d=train_date, n=train_numbers, c=train_company, m=train_mode, s=train_submode, t=train_typemode
        )

        list_ads = get_value(json_train, "listeArretsDesserte")
        ads = _retrieve_interesting_stops(get_value(list_ads, "arret"))
        if len(ads) < 2:
            raise InvalidArguments(
                'invalid json, "listeArretsDesserte/arret" has less than 2 valid stop_times in '
                "json elt {elt}".format(elt=ujson.dumps(json_train))
            )

        vj = self._get_navitia_vj(piv_key, ads)
        trip_updates = [self._make_trip_update(json_train, vj)]

        log_dict = {}
        return trip_updates, log_dict

    def _get_navitia_vj(self, piv_key, ads):
        log = logging.LoggerAdapter(logging.getLogger(__name__), extra={"contributor": self.contributor.id})

        log.debug("searching for vj {} in navitia".format(piv_key))
        navitia_vjs = self.navitia.vehicle_journeys(
            q={
                "filter": 'vehicle_journey.has_code("rt_piv", "{}")'.format(piv_key),
                "depth": "2",  # we need this depth to get the stoptime's stop_area
                "show_codes": "true",  # we need the stop_areas codes
            }
        )

        if not navitia_vjs:
            # Last PIV is always right, so if the VJ doesn't exist, it's an ADD (no matter feed content)
            navitia_vjs = [_make_navitia_empty_vj(piv_key)]

        vj = None
        if len(navitia_vjs) != 1:
            log.info("Can not match a unique train for key {}".format(piv_key))
            record_internal_failure("no unique train", contributor=self.contributor.id)
        else:
            try:
                base_vs_rt_error_margin = timedelta(hours=1)
                vj_base_start = _get_first_stop_base_datetime(ads, "depart", skip_fully_added_stops=True)
                vj = model.VehicleJourney(
                    navitia_vjs[0],
                    vj_base_start - base_vs_rt_error_margin,
                    vj_base_start + base_vs_rt_error_margin,
                    vj_start_dt=vj_base_start,
                )
            except Exception as e:
                log.exception("Error while creating kirin VJ of {}: {}".format(navitia_vjs[0].get("id"), e))
                record_internal_failure("Error while creating kirin VJ", contributor=self.contributor.id)

        if not vj:
            raise ObjectNotFound("no train found for key {}".format(piv_key))
        return vj

    def _make_trip_update(self, json_train, vj):
        trip_update = model.TripUpdate(vj=vj, contributor_id=self.contributor.id)
        trip_update.headsign = get_value(json_train, "numero", nullable=True)
        company_id = get_value(get_value(json_train, "operateur"), "codeOperateur")
        trip_update.company_id = self._get_navitia_company(company_id)
        if not trip_update.company_id:
            raise ObjectNotFound("No company found from code {}".format(company_id))
        physical_mode = get_value(get_value(json_train, "modeTransport"), "typeMode")
        trip_update.physical_mode_id = self._get_navitia_physical_mode(physical_mode)

        # TODO: handle status/effect for creation, deletion, detour, back-to-normal
        trip_update.status = ModificationType.update.name
        trip_update.effect = TripEffect.MODIFIED_SERVICE.name

        highest_st_status = ModificationType.none.name
        ads = _retrieve_interesting_stops(get_value(get_value(json_train, "listeArretsDesserte"), "arret"))

        # this variable is used to memoize the last stop_time's departure in order to check the stop_time consistency
        # ex. stop_time[i].arrival/departure must be greater than stop_time[i-1].departure
        previous_rt_stop_time_dep = None

        for arret in ads:
            # retrieve navitia's stop_point corresponding to the current COTS pdp
            nav_stop, log_dict = self._get_navitia_stop_point(arret, vj.navitia_vj)
            rt_stop_time = {"arrivee": None, "depart": None}  # used to check consistency

            if log_dict:
                record_internal_failure(log_dict["log"], contributor=self.contributor.id)
                log_dict.update({"contributor": self.contributor.id})
                logging.getLogger(__name__).info("metrology", extra=log_dict)

            if nav_stop is None:
                continue  # simply skip stop_times at unknown stop areas

            st_update = model.StopTimeUpdate(nav_stop)
            trip_update.stop_time_updates.append(st_update)

            for event_toggle in ["arrivee", "depart"]:
                event = get_value(arret, event_toggle, nullable=True)
                if event is None:
                    continue

                piv_disruption = get_value(event, "evenement", nullable=True)

                piv_event_status = get_value(event, "statutModification", nullable=True)
                if not piv_event_status and piv_disruption:
                    piv_event_status = get_value(piv_disruption, "type")

                if not piv_event_status or piv_event_status in ["RETARD_OBSERVE", "RETARD_PROJETE", "NORMAL"]:
                    piv_event_datetime = get_value(event, "dateHeureReelle", nullable=True)
                    even_datetime = as_utc_naive_dt(piv_event_datetime) if piv_event_datetime else None
                    if even_datetime:
                        rt_stop_time[event_toggle] = even_datetime
                        setattr(st_update, STOP_EVENT_DATETIME_MAP[event_toggle], even_datetime)
                    piv_event_delay = 0
                    if piv_disruption:
                        piv_delay = get_value(piv_disruption, "retard", nullable=True)
                        if piv_delay:
                            piv_event_delay = get_value(piv_delay, "duree", nullable=True) or 0

                    if piv_event_delay:
                        setattr(st_update, STATUS_MAP[event_toggle], ModificationType.update.name)
                        setattr(st_update, DELAY_MAP[event_toggle], as_duration(piv_event_delay * 60))  # minutes
                    # otherwise let those be none

                else:
                    raise InvalidArguments(
                        "invalid value {s} for field {t}/statutModification or {t}/evenement/type".format(
                            s=piv_event_status, t=event_toggle
                        )
                    )

                event_status = getattr(st_update, STATUS_MAP[event_toggle], ModificationType.none.name)
                highest_st_status = get_higher_status(highest_st_status, event_status)

            _check_stop_time_consistency(
                previous_rt_stop_time_dep,
                rt_stop_time,
                uic8=get_value(get_value(arret, "emplacement"), "code"),
            )
            previous_rt_stop_time_dep = rt_stop_time["depart"]

        # Calculates effect from stop_time status list (this work is also done in kraken and has to be deleted there)
        if trip_update.effect == TripEffect.MODIFIED_SERVICE.name:
            trip_update.effect = get_effect_by_stop_time_status(highest_st_status)
        return trip_update

    def _get_navitia_company(self, code):
        """
        Get a navitia company for the given code
        """
        return self._request_navitia_company(code)

    def _request_navitia_company(self, code):
        companies = self.navitia.companies(
            # TODO: when data is OK, use q={"filter": 'company.has_code("source", "{}")'.format(code), "count": "1"}
            q={"count": "1"}
        )
        if companies:
            return companies[0].get("id", None)
        return None

    def _get_navitia_physical_mode(self, indicator=None):
        """
        Get a navitia physical_mode for the codes present in PIV (FERRE / ROUTIER)
        """
        uri = {
            "FERRE": "physical_mode:LongDistanceTrain",
            "ROUTIER": "physical_mode:Coach",
        }.get(indicator)
        return self._request_navitia_physical_mode(uri)  # confirm it exists

    def _request_navitia_physical_mode(self, uri):
        physical_modes = self.navitia.physical_modes(uri=uri)
        if physical_modes:
            return physical_modes[0].get("id", None)
        return None

    def _get_navitia_stop_point(self, arret, nav_vj):
        """
        Get a navitia stop point from the stop_time in a 'Point de Parcours' dict.
        The dict MUST contain cr, ci, ch tags.
        It searches in the vj's stops for a stop_area with the external code cr-ci-ch

        If the stop_time isn't found in the vj, in case of an additional stop_time,
        a request is made to Navitia.

        Error messages are also returned as 'missing stop point', 'duplicate stops'
        """
        uic8 = get_value(get_value(arret, "emplacement"), "code")
        nav_st, log_dict = _extract_navitia_stop_time(uic8, nav_vj)
        if not nav_st:
            nav_stop, log_dict = self._request_navitia_stop_point(uic8)
        else:
            nav_stop = nav_st.get("stop_point", None)
        return nav_stop, log_dict

    def _request_navitia_stop_point(self, uic8):
        stop_points = self.navitia.stop_points(
            q={"filter": 'stop_area.has_code("source", "{}")'.format(uic8), "count": "1"}
        )
        if stop_points:
            return stop_points[0], None

        return None, {"log": "No stop point found", "stop_point_code": uic8}
