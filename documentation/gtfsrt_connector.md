# GTFS-RT Connector

## Overview
This document describes how a [GTFS-RT](https://gtfs.org/reference/realtime/v2/) feed is read in Kirin.

Currently, the connector can only read TripUpdate messages with arrival/departure delays (no added/deleted trip/stop).

## Connector description
For the sake of simplicity, in the following only the input relevant fields are 
described, leaving aside the fields of the internal model that are managed by Kirin.

### RealTimeUpdate
Kirin property | GTFS-RT object | Comment/Mapping rule
--- | --- | ---
connector |  | Fixed value `gtfs-rt`.
raw_data | _Complete received feed_ |
contributor |  | Fixed value specified in the configuration of Kirin.
trip_updates |  | List of trip updates information, see `TripUpdates` below.

### TripUpdate
Kirin property | GTFS-RT object | Comment/Mapping rule
--- | --- | ---
vj_id | trip_id | The id of the Navitia `VehicleJourney` having a code of type `source` and a value that matches the input trip_id.
status |  | Status is set to `update` if at least one of the trip's stops is updated, otherwise status is set to `none`.
message | ?? | 
contributor |  | Fixed value specified in the configuration of Kirin.
stop_time_updates |  | List of arrival/departure time updates at stops for this trip, see `StopTimeUpdates` below.
effect |  | Effect is set to `SIGNIFICANT_DELAYS` when the trip status is `update` and `UNKNOWN_EFFECT` otherwise.

### VehicleJourney
Kirin property | Comment/Mapping rule
--- | ---
navitia_trip_id | `trip_id` of the VehicleJourney in Navitia. See above for the mapping rule.
start_timestamp | Start datetime of the `VehicleJourney` in Navitia.

### StopTimeUpdate
Kirin property | GTFS-RT object | Comment/Mapping rule
--- | --- | ---
order | ?? | `stop_time` order of this stop in the `VehicleJourney`. 
stop_id | stop_id | Id of the updated stop in Navitia
message | ?? | 
departure | ?? | Departure datetime of the `VehicleJourney` for this stop in Navitia. 
departure_delay | ?? | 
departure_status | ?? | 
arrival | ?? | Arrival datetime of the `VehicleJourney` for this stop in Navitia.
arrival_delay | ?? | 
arrival_status | ?? | 
