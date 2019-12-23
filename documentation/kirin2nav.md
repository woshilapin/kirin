# Kirin to Navitia Interface
## Overview
This document describes the realtime feed sent from Kirin to Navitia. The exchanged
feed is derived from the [GTFS-RT](https://gtfs.org/reference/realtime/v2/) TripUpdate message with some extensions.

## Message description
The realtime feed is defined with relation to the existing static schedule in navitia.
Each feed provides realtime information for the complete vehicle journey and
overwrites all previous realtime information.
In the following, the optional fields that are not provided in the output feed are not specified.

### FeedHeader
Field | Type | Description
--- | --- | ---
gtfs_realtime_version | String | Fixed value `1`.
incrementality | Enum | Fixed value `FULL_DATASET`.
timestamp | unit64 | The UTC time when the feed is created given in POSIX time.

### FeedEntity
Field | Type | Description
--- | --- | ---
id | String | The id of the navitia vehicle journey being updated.
trip_update | TripUpdate | The `TripUpdate` message with the realtime data for the vehicle journey.

### TripUpdate
Field | Type | Description
--- | --- | ---
trip | TripDescriptor | The `TripDescriptor` that identifies the vehicle journey.
vehicle | VehicleDescriptor | The `VehicleDescriptor` that provides the physical mode of the vehicle journey.
stop_time_update | List of StopTimeUpdates | The `StopTimeUpdates` of the vehicle journey.
trip_message | String | Extended field. The information for the vehicle journey to be displayed (if specified).
effect | Enum | Extended field. The effect of the affected vehicle journey to be displayed. The possible values are `NO_SERVICE`, `REDUCED_SERVICE`, `SIGNIFICANT_DELAYS`, `DETOUR`, `ADDITIONAL_SERVICE`, `MODIFIED_SERVICE`, `OTHER_EFFECT`, `UNKNOWN_EFFECT`, `STOP_MOVED`.
headsign | String | Extended field. The destination of the updated vehicle journey to be displayed.

### TripDescriptor
Field | Type | Description
--- | --- | ---
trip_id | String | The id of the navitia vehicle journey being updated.
start_date | String | The start date in UTC of the static schedule vehicle journey as it is found in navitia.
schedule_relationship | Enum | The relation between the vehicle journey being updated and the static schedule. The possible values are `SCHEDULED`, `ADDED`, `UNSCHEDULED`, `CANCELED`.
contributor | String | Extended field. The identifier of the realtime contributor.
company_id | String | Extended field. The transport operator of the vehicle journey as it is found in navitia.

### VehicleDescriptor
Field | Type | Description
--- | --- | ---
physical_mode_id | String | Extended field. The physical mode of the vehicle journey as it is found in navitia.

### StopTimeUpdate
Field | Type | Description
--- | --- | ---
stop_sequence | String | The order of the given stop for the updated vehicle journey in navitia.
stop_id | String | The identifier of the stop_point as it is found in navitia.
arrival | StopTimeEvent | The timing information at the arrival of the given stop_point.
departure | StopTimeEvent | The timing information at the departure of this stop_point.
schedule_relationship | Enum | The possible values are `SCHEDULED`, `SKIPPED`, `NO_DATA`, `UNSCHEDULED`.
stoptime_message | String | Extended field. The text to be displayed for the given stop_point.

### StopTimeEvent
Field | Type | Description
--- | --- | ---
time | unit64 | Updated time in POSIX time for the StopTime.
delay | String | Delay in seconds of the update at the StopTime. The default value is `0`.
stop_time_event_relationship | Enum | Extended field. The type of the update of the StopTime in relation with the static schedule. The possible values are `SCHEDULED`, `SKIPPED`, `NO_DATA`, `UNSCHEDULED`.
stop_time_event_status | Enum | Extended field. The possible values are `SCHEDULED`, `DELETED`, `NO_DATA`, `ADDED`, `DELETED_FOR_DETOUR`, `ADDED_FOR_DETOUR`.

