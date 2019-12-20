# Kirin to Navitia Interface
## Overview
This document describes the realtime feed sent from Kirin to Navitia. The exchanged feed is derived from the [GTFS-RT](https://gtfs.org/reference/realtime/v2/) TripUpdate message with some extensions.

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
headsign | String | Extended field. The updated text for the vehicle journey to be displayed.

### TripDescriptor
Field | Type | Description
--- | --- | ---
trip_id | |
start_date | String |
schedule_relationship | Enum | The possible values are `SCHEDULED`, `ADDED`, `UNSCHEDULED`, `CANCELED`.
contributor | String | Extended field.
company_id | String | Extended field.

### VehicleDescriptor
Field | Type | Description
--- | --- | ---
physical_mode_id | String | Extended field. The physical mode of the vehicle journey.

### StopTimeUpdate
Field | Type | Description
--- | --- | ---
stop_sequence | String |
stop_id | String | 
arrival | StopTimeEvent |
departure | StopTimeEvent |
schedule_relationship | Enum | The possible values are `SCHEDULED`, `SKIPPED`, `NO_DATA`, `UNSCHEDULED`.
stoptime_message | String | Extended field.

### StopTimeEvent
Field | Type | Description
--- | --- | ---
time | unit64 |
stop_time_event_relationship | Enum | Extended field. The possible values are `SCHEDULED`, `SKIPPED`, `NO_DATA`, `UNSCHEDULED`.
stop_time_event_status | Enum | Extended field. The possible values are `SCHEDULED`, `DELETED`, `NO_DATA`, `ADDED`, `DELETED_FOR_DETOUR`, `ADDED_FOR_DETOUR`.

