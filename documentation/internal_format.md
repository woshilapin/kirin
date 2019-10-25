# Kirin internal format

## Overview
Kirin's internal model is derived from GTFS-realtime `Trip updates` (specifications)[http://gtfs.org/realtime/#message-tripupdate].
It is composed of several objects :
- VehicleJourney
- RealTimeUpdate
- TripUpdate
- StopTimeUpdate

## Model details
### Contributor
A contributor is the owner of a realtime service and contains configuration information.

Property | TYpe | Description
--- | --- | ---
id | UUID |
navitia_coverage | String, Required | Navitia coverage to be used while calling navitia to retrieve corresponding element
navitia_token | String, Required | Navitia token to be used while calling navitia to retrieve corresponding element
feed_url | String, Required | Url to retrieve the realtime information feed
connector_type | String, Required | Type of connector (cots, gtfs-rt)
is_active | Boolean, Required | Used to activate/deactivate the kirin service for the contributor

### RealTimeUpdate
Received raw data from a Real Time Update.

Property | TYpe | Description
--- | --- | ---
id | UUID |
received_at | DateTime, Required | Date and time of the reception of the data (UTC)
connector | Enum, Required | Source of the data. See below for an available source format.
status | Enum, Required | Processing status of the received data (Possible values are `OK`, `KO` or `pending`)
error | String, Optional | Description of the error (if any)
raw_data | String, Optional | Content of the received raw data
contributor | String, Optional | Identifier of the realtime connector. It must be known by Kraken (internal component of (navitia)[https://github.com/CanalTP/navitia].
trip_updates | List | List of `TripUpdate` provided by this bloc of data

**Connector field possible values**
The `connector` field is restricted to the following values:
- `ire`: realtime informations of the SNCF long distance trains
- `gtfs-rt`: realtime informations from the `TripUpdate` format of GTFS-realtime

### TripUpdate
Update information about a VehicleJourney.

Property | TYpe | Description
--- | --- | ---
id | UUID |
vj_id | UUID | id of the VehicleJourney being updated
status | Enum, Required | Modification type for this trip (Possible values are `add`, `delete`, `update` or `none`)
message | String, Optional | Text to be displayed in Navitia for the `VehicleJourney`
contributor | String, Optional | Identifier of the realtime connector. It must be known by Kraken.
company_id | String, Optional | Identifier of the transport operator found in Navitia for this trip.
stop_time_updates | List | List of `StopTimeUpdate` provided by this bloc of data
effect | Enum, optional | Effect to be displayed in navitia (Possible values are `NO_SERVICE`, `REDUCED_SERVICE`, `SIGNIFICANT_DELAYS`, `DETOUR`, `ADDITIONAL_SERVICE`, `MODIFIED_SERVICE`, `OTHER_EFFECT`, `UNKNOWN_EFFECT`, `STOP_MOVED`)
physical_mode_id | String, Optional | Identifier of the physical mode found in Navitia for this trip

### VehicleJourney
Property | TYpe | Description
--- | --- | ---
id | UUID | Unique identifier
navitia_trip_id | String, Required | Identifier of Navitia's trip_id
start_timestamp | DateTime, Required | Start date and time of the VehicleJourney (UTC) in base_schedule (ie. without any realtime info)

### StopTimeUpdate
Property | TYpe | Description
--- | --- | ---
id | UUID |
trip_update_id | UUID | id of the `TripUpdate` containing this `StopTimeUpdate`
order | Integer, Required | `StopTime` order in the `VehicleJourney`
stop_id | String, Required | id of the stop_point in navitia
message | String, Optional | Text to be displayed in Navitia for the `StopTime`
departure | DateTime, Optional | Base scheduled departure datetime of this StopTime
departure_delay | Integer, Optional | Delay for the departure at this StopTime (in minutes)
departure_status | Enum, Required | Modification type for the departure of the trip at this StopTime (Possible values are `add`, `delete`, `update` or `none`)
arrival | DateTime, Optional | Base scheduled arrival datetime of this StopTime
arrival_delay | Integer, Optional | Delay for the arrival at this StopTime (in minutes)
arrival_status | Enum, Required | Modification type for the arrival of the trip at this StopTime (Possible values are `add`, `delete`, `update` or `none`)