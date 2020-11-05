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
from sys import maxint

import jmespath
import ujson
from operator import itemgetter

from kirin.core import model
from kirin.core.abstract_builder import AbstractKirinModelBuilder
from kirin.core.types import ModificationType, TripEffect, get_higher_status, get_effect_by_stop_time_status
from kirin.exceptions import InvalidArguments, UnsupportedValue, ObjectNotFound
from kirin.utils import make_rt_update, get_value, as_utc_naive_dt, record_internal_failure, as_duration

# The default company for PIV is SNCF (code '1187')
DEFAULT_COMPANY_CODE = "1187"
DEFAULT_PHYSICAL_MODE_ID = "physical_mode:LongDistanceTrain"
TRIP_PIV_ID_FORMAT = "PIV:REALTIME:{}"

STATUS_MAP = {"arrivee": "arrival_status", "depart": "departure_status"}
DELAY_MAP = {"arrivee": "arrival_delay", "depart": "departure_delay"}
STOP_EVENT_DATETIME_MAP = {"arrivee": "arrival", "depart": "departure"}


trip_piv_status_to_effect = {
    "SUPPRESSION": TripEffect.NO_SERVICE,
    "CREATION": TripEffect.ADDITIONAL_SERVICE,
    "MODIFICATION_DETOURNEMENT": TripEffect.DETOUR,
    "MODIFICATION_DESSERTE_SUPPRIMEE": TripEffect.REDUCED_SERVICE,
    "MODIFICATION_LIMITATION": TripEffect.REDUCED_SERVICE,
    "MODIFICATION_DESSERTE_AJOUTEE": TripEffect.MODIFIED_SERVICE,
    "MODIFICATION_PROLONGATION": TripEffect.MODIFIED_SERVICE,
    "RETARD": TripEffect.SIGNIFICANT_DELAYS,
    "NORMAL": TripEffect.UNKNOWN_EFFECT,
    "UNDEFINED": TripEffect.UNDEFINED,
}

trip_effect_order = {
    TripEffect.ADDITIONAL_SERVICE: 0,
    TripEffect.NO_SERVICE: 1,
    TripEffect.DETOUR: 2,
    TripEffect.REDUCED_SERVICE: 3,
    TripEffect.MODIFIED_SERVICE: 4,
    TripEffect.SIGNIFICANT_DELAYS: 5,
    TripEffect.UNKNOWN_EFFECT: 6,
    TripEffect.UNDEFINED: maxint,
}

MANAGED_EVENTS = ["RETARD", "SUPPRESSION", "MODIFICATION_DESSERTE_SUPPRIMEE"]
MANAGED_STOP_EVENTS = ["RETARD_OBSERVE", "RETARD_PROJETE", "NORMAL", "SUPPRESSION_PARTIELLE"]


def _get_trip_effect_order_from_piv_status(status):
    return trip_effect_order.get(trip_piv_status_to_effect.get(status, TripEffect.UNDEFINED), maxint)


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
        # * if a stop_time only has departure time, travelers can only hop in, but if they are able to
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
    # In base_schedule trip, searching for a stop_time at stop_point belonging to the right stop_area
    # stop_areas bear UIC8 code, while stop_point match one stop_area and one mode currently.
    nav_stop_times = jmespath.search(
        "stop_times[? stop_point.stop_area.codes[? value=='{uic8}' && type=='source']]".format(uic8=uic8),
        nav_vj,
    )

    log_dict = {}
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

    if not (previous_rt_stop_time_dep <= rt_arrival <= rt_departure):
        raise InvalidArguments("invalid feed: stop_point's({}) time is not consistent".format(uic8))


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
        try:
            json = ujson.loads(rt_update.raw_data)
        except ValueError as e:
            raise InvalidArguments("invalid json: {}".format(e.message))

        dict_objects = get_value(json, "objects")
        json_train = get_value(dict_objects[0], "object")  # TODO: can we get more than 1 relevant in objects[]?
        piv_disruptions = get_value(json_train, "evenement", nullable=True)
        plan_transport_source = get_value(json_train, "planTransportSource", nullable=True)

        if not piv_disruptions and not plan_transport_source:
            raise InvalidArguments('No object "evenement" or "planTransportSource" available in feed provided')

        higher_disruption = ujson.loads('{"type": "UNDEFINED", "texte": ""}')
        if piv_disruptions:
            for piv_disruption in piv_disruptions:
                piv_disruption_type = get_value(piv_disruption, "type", nullable=True)
                if (
                    piv_disruption_type
                    and piv_disruption_type in trip_piv_status_to_effect
                    and piv_disruption_type in MANAGED_EVENTS
                ):
                    higher_disruption = (
                        piv_disruption
                        if _get_trip_effect_order_from_piv_status(piv_disruption_type)
                        < _get_trip_effect_order_from_piv_status(get_value(higher_disruption, "type"))
                        else higher_disruption
                    )
            if trip_piv_status_to_effect[higher_disruption.get("type")] == TripEffect.UNDEFINED:
                raise UnsupportedValue("None of the disruption-types {} are supported".format(piv_disruptions))
        elif plan_transport_source and plan_transport_source not in ["PTP", "OPE"]:
            raise UnsupportedValue("planTransportSource {} is not supported".format(plan_transport_source))

        json_train["evenement"] = higher_disruption
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
        # replace by cleaned and sorted version of stoptimes list.
        json_train["listeArretsDesserte"]["arret"] = ads

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
            # Last PIV information is always right, so if the VJ doesn't exist, it's an ADD (no matter feed content)
            navitia_vjs = [_make_navitia_empty_vj(piv_key)]

        vj = None
        if len(navitia_vjs) != 1:
            log.info("Can not match a unique train for key {}".format(piv_key))
            record_internal_failure("no unique train", contributor=self.contributor.id)
        else:
            navitia_vj = navitia_vjs[0]
            try:
                base_vs_rt_error_margin = timedelta(hours=1)
                vj_base_start = _get_first_stop_base_datetime(ads, "depart", skip_fully_added_stops=True)
                vj = model.VehicleJourney(
                    navitia_vj,
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
        trip_update.headsign = json_train.get("numero")
        company_id = json_train.get("operateur").get("codeOperateur")
        trip_update.company_id = self._get_navitia_company_id(company_id)
        physical_mode = json_train.get("modeTransport").get("typeMode")
        trip_update.physical_mode_id = self._get_navitia_physical_mode_id(physical_mode)
        trip_status_type = trip_piv_status_to_effect[json_train.get("evenement").get("type")]
        trip_update.message = json_train.get("evenement").get("texte")
        trip_update.effect = trip_status_type.name

        # TODO: handle status/effect for creation, detour, back-to-normal
        if trip_status_type == TripEffect.NO_SERVICE:
            # the whole trip is deleted
            trip_update.status = ModificationType.delete.name
            trip_update.stop_time_updates = []
            return trip_update

        trip_update.status = ModificationType.update.name

        highest_st_status = ModificationType.none.name
        ads = get_value(get_value(json_train, "listeArretsDesserte"), "arret")

        # this variable is used to memoize the last stop_time's departure in order to check the stop_time consistency
        # ex. stop_time[i].arrival/departure must be greater than stop_time[i-1].departure
        previous_rt_stop_time_dep = None

        for arret in ads:
            # retrieve navitia's stop_point corresponding to the current PIV ad
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

                if not piv_event_status or piv_event_status in MANAGED_STOP_EVENTS:
                    piv_event_datetime = get_value(event, "dateHeureReelle", nullable=True)
                    event_datetime = as_utc_naive_dt(piv_event_datetime) if piv_event_datetime else None
                    if event_datetime:
                        rt_stop_time[event_toggle] = event_datetime
                        setattr(st_update, STOP_EVENT_DATETIME_MAP[event_toggle], event_datetime)
                    if piv_disruption:
                        piv_delay = get_value(piv_disruption, "retard", nullable=True)
                        if piv_delay:
                            piv_event_delay = get_value(piv_delay, "duree", nullable=True) or 0
                            setattr(st_update, STATUS_MAP[event_toggle], ModificationType.update.name)
                            setattr(
                                st_update, DELAY_MAP[event_toggle], as_duration(piv_event_delay * 60)
                            )  # minutes
                        piv_stop_time_status = get_value(piv_disruption, "type", nullable=True)
                        if piv_stop_time_status and piv_stop_time_status == "SUPPRESSION_PARTIELLE":
                            setattr(st_update, STATUS_MAP[event_toggle], ModificationType.delete.name)

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

    def _get_navitia_company_id(self, code):
        """
        Get a navitia company for the given code
        """
        company = self._request_navitia_company(code)
        if not company:
            company = self._request_navitia_company(DEFAULT_COMPANY_CODE)
            if not company:
                raise ObjectNotFound(
                    "no company found for key {}, nor for the default company {}".format(
                        code, DEFAULT_COMPANY_CODE
                    )
                )
        return company.get("id", None) if company else None

    def _request_navitia_company(self, code):
        companies = self.navitia.companies(
            q={"filter": 'company.has_code("source", "{}")'.format(code), "count": "1"}
        )
        return companies[0] if companies else None

    def _get_navitia_physical_mode_id(self, indicator=None):
        """
        Get a navitia physical_mode for the codes present in PIV (FERRE / ROUTIER)
        """
        uri = {
            "FERRE": "physical_mode:LongDistanceTrain",
            "ROUTIER": "physical_mode:Coach",
        }.get(indicator, DEFAULT_PHYSICAL_MODE_ID)
        physical_mode = self._request_navitia_physical_mode(uri)
        return physical_mode.get("id", None) if physical_mode else None

    def _request_navitia_physical_mode(self, uri):
        physical_modes = self.navitia.physical_modes(uri=uri)
        physical_modes[0] if physical_modes else None

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
            nav_stop, req_log_dict = self._request_navitia_stop_point(uic8)
            log_dict.update(req_log_dict)
        else:
            nav_stop = nav_st.get("stop_point", None)
        return nav_stop, log_dict

    def _request_navitia_stop_point(self, uic8):
        stop_points = self.navitia.stop_points(
            q={"filter": 'stop_area.has_code("source", "{}")'.format(uic8), "count": "1"}
        )
        if stop_points:
            return stop_points[0], {}

        return None, {"log": "No stop point found", "stop_point_code": uic8}
