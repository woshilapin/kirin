# Kirin to Navitia Interface
## Overview
This document describes the realtime feed sent from Kirin to Navitia.  
The exchanged feed is derived from the [GTFS-RT](https://gtfs.org/reference/realtime/v2/) TripUpdate message with some extensions.

## Message description
The realtime feed is defined with relation to the existing static schedule in Navitia.

Each feed provides realtime information for the complete vehicle journey and
overwrites all previous realtime information for this vehicle journey.  
No information about a vehicle journey means it stays the same (previous realtime information stays valid).

In the following, the optional fields that are not provided in the output feed are not specified.  
Required fields not specified are unused, so filled with any format-valid value.

NB: Every time (date, timestamp, datetime, hour of day) field is expressed in UTC.

### FeedHeader
Field | Type | Description
--- | --- | ---
gtfs_realtime_version | String | Fixed value `1`.
timestamp | unit64 | The UTC POSIX time when the feed destined to Navitia is created in Kirin.

### FeedEntity
Field | Type | Description
--- | --- | ---
id | UUID | This is an auto-generated id, stable along different updates of the same Navitia vehicle journey for the same date.
trip_update | TripUpdate | The `TripUpdate` message with the realtime data for the vehicle journey.

### TripUpdate
Field | Type | Description
--- | --- | ---
trip | TripDescriptor | The `TripDescriptor` that identifies the vehicle journey.
vehicle | VehicleDescriptor | The `VehicleDescriptor` that provides additional information about the vehicle journey.
stop_time_update | List of StopTimeUpdates | The `StopTimeUpdates` of the vehicle journey.
trip_message | String | Extended field. The information for the vehicle journey to be displayed (if specified).
effect | Enum | Extended field. The effect of the affected vehicle journey to be displayed. It follows the [effect](https://gtfs.org/reference/realtime/v2/#enum-effect) of an Alert message as it is specified in GTFS-RT. The possible values are `NO_SERVICE`, `REDUCED_SERVICE`, `SIGNIFICANT_DELAYS`, `DETOUR`, `ADDITIONAL_SERVICE`, `MODIFIED_SERVICE`, `UNKNOWN_EFFECT`.
headsign | String | Extended field. The trip headsign of the vehicle journey as it is found in Navitia.

### TripDescriptor
Field | Type | Description
--- | --- | ---
trip_id | String | Navitia's id of the vehicle journey being updated.
start_date | String | The start date in UTC of the static schedule vehicle journey to be updated as it is found in Navitia.
schedule_relationship | Enum | The relation between the vehicle journey being updated and the static schedule. The possible values are `SCHEDULED`, `ADDED`, `CANCELED`. This field is deprecated in favor of the more detailed `TripUpdate.effect`.
contributor | String | Extended field. The identifier of the realtime contributor.
company_id | String | Extended field. The transport operator of the vehicle journey as it is found in Navitia.

### VehicleDescriptor
Field | Type | Description
--- | --- | ---
physical_mode_id | String | Extended field. The physical mode of the vehicle journey as it is found in Navitia.

### StopTimeUpdate
Field | Type | Description
--- | --- | ---
stop_id | String | The identifier of the stop_point as it is found in Navitia.
arrival | StopTimeEvent | The timing information at the arrival of the given stop_point.
departure | StopTimeEvent | The timing information at the departure of this stop_point.
stoptime_message | String | Extended field. The text to be displayed for the given stop_point.

### StopTimeEvent
Field | Type | Description
--- | --- | ---
time | unit64 | Updated time in UTC POSIX time for the StopTime.
delay | String | Delay in seconds of the update at the StopTime. The default value is `0`. This field is only used to determine the StopTime status and `time` always takes precedence over `delay`.
stop_time_event_relationship | Enum | Extended field. The type of the update of the StopTime in relation with the static schedule. The possible values are `SCHEDULED`, `SKIPPED`. This field is deprecated in favor of `stop_time_event_status`.
stop_time_event_status | Enum | Extended field. The possible values are `SCHEDULED`, `DELETED`, `ADDED`, `DELETED_FOR_DETOUR`, `ADDED_FOR_DETOUR`.

