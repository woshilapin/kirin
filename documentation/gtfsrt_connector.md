# GTFS-RT Connector

## Overview
This document describes how a [GTFS-RT](https://gtfs.org/reference/realtime/v2/) feed is read in Kirin.

Currently, the connector can only read TripUpdate messages with arrival/departure delays (no added/deleted trip/stop).

## Connector description
For the sake of simplicity, only the relevant input fields are described below.
The fields of the internal model that are managed by Kirin without reading input
are left aside.

### RealTimeUpdate
Kirin property | GTFS-RT object | Comment/Mapping rule
--- | --- | ---
connector |  | Fixed value `gtfs-rt`.
raw_data | _Readable complete received feed_ |
contributor_id |  | Id of the contributor producing the data.
trip_updates |  | List of trip updates information, see `TripUpdates` below.

### TripUpdate
Kirin property | GTFS-RT object | Comment/Mapping rule
--- | --- | ---
vj_id | trip_update.trip.trip_id (indirectly) | The id of the Navitia `VehicleJourney` being updated by the `TripUpdate`. See the mapping methode below.
status |  | Status is always set to `none` currently.
contributor_id |  | Id of the contributor producing the data.
stop_time_updates |  | List of arrival/departure time updates at stops for this trip, see `StopTimeUpdates` below.
effect |  | Effect is set to `SIGNIFICANT_DELAYS` if at least one of the trip's stops is updated and `UNKNOWN_EFFECT` otherwise.

### VehicleJourney
The right Navitia trip that is impacted by a given realtime update is retrieved 
through a call to Navitia. The call should search for the `VehicleJourney` that has 
a code of type `source` with a value matching the input trip_id.

The date used to narrow down the research of the right Navitia trip is defined by the date found in `header.timestamp`.

Kirin property | GTFS-RT object | Comment/Mapping rule
--- | --- | ---
navitia_trip_id | trip_update.trip.trip_id (indirectly) | `trip_id` of the `VehicleJourney` in Navitia. See above for the mapping rule.
start_timestamp | header.timestamp | Start datetime of the `VehicleJourney` in Navitia.

### StopTimeUpdate
Once the right Navitia trip is identified, the timing information for each `stop_time` is updated.
The whole resulting trip is stored, including the unchanged stop_times.

Kirin property | GTFS-RT object | Comment/Mapping rule
--- | --- | ---
order |  | `stop_time` order of this stop in the `VehicleJourney`. 
stop_id | trip_update.stop_time_update.stop_id (indirectly) | The id of the updated stop in Navitia that has a code of type `source` with a value matching the input stop_id.
departure |  | Realtime departure datetime for this stop (including delay). 
departure_delay | trip_update.stop_time_update.departure.delay | 
departure_status |  | Status is set to `none` if the departure delay is 0 or not provided, otherwise status is set to `update`.
arrival |  | Realtime arrival datetime for this stop (including delay).
arrival_delay | trip_update.stop_time_update.arrival.delay | 
arrival_status |  | Status is set to `none` if the arrival delay is 0 or not provided, otherwise status is set to `update`.
