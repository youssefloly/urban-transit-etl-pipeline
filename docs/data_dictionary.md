# Data Dictionary

## Dataset Name

NYC Citi Bike Trip Data - January 2024

## Description

This data dictionary describes the raw columns included in the Citi Bike trip dataset used in the Urban Transit ETL Pipeline project.

| Column Name          | Description                                | Detected Type | Expected Type | Required | Notes                                                     |
| -------------------- | ------------------------------------------ | ------------- | ------------- | -------- | --------------------------------------------------------- |
| `ride_id`            | Unique identifier for each bike trip       | String        | String        | Yes      | Primary key candidate                                     |
| `rideable_type`      | Type of bike used in the trip              | String        | String        | Yes      | Example values may include electric bike and classic bike |
| `started_at`         | Timestamp when the trip started            | Datetime      | Timestamp     | Yes      | Used for date and time analysis                           |
| `ended_at`           | Timestamp when the trip ended              | Datetime      | Timestamp     | Yes      | Used to calculate trip duration                           |
| `start_station_name` | Name of the station where the trip started | String        | String        | No       | May contain missing values                                |
| `start_station_id`   | Identifier of the starting station         | String        | String        | No       | Used for station dimension                                |
| `end_station_name`   | Name of the station where the trip ended   | String        | String        | No       | May contain missing values                                |
| `end_station_id`     | Identifier of the ending station           | String        | String        | No       | Used for station dimension                                |
| `start_lat`          | Latitude of the trip start location        | Float64       | Float         | No       | Used for location validation                              |
| `start_lng`          | Longitude of the trip start location       | Float64       | Float         | No       | Used for location validation                              |
| `end_lat`            | Latitude of the trip end location          | Float64       | Float         | No       | May contain missing values                                |
| `end_lng`            | Longitude of the trip end location         | Float64       | Float         | No       | May contain missing values                                |
| `member_casual`      | Rider membership type                      | String        | String        | Yes      | Expected values: member or casual                         |

## Important Columns for Validation

The most important columns for schema validation are:

* `ride_id`
* `rideable_type`
* `started_at`
* `ended_at`
* `start_station_name`
* `start_station_id`
* `end_station_name`
* `end_station_id`
* `start_lat`
* `start_lng`
* `end_lat`
* `end_lng`
* `member_casual`

## Candidate Primary Key

The column `ride_id` can be used as a candidate primary key because the initial profiling showed that there are no duplicate `ride_id` values.

## Columns Used for Time Analysis

The following columns will be used to create date and time-based derived fields:

* `started_at`
* `ended_at`

Possible derived fields:

* trip date
* trip hour
* day of week
* month
* trip duration in minutes

## Columns Used for Station Analysis

The following columns will be used for station-related analysis:

* `start_station_name`
* `start_station_id`
* `end_station_name`
* `end_station_id`

## Columns Used for Location Validation

The following columns will be used to validate geographic coordinates:

* `start_lat`
* `start_lng`
* `end_lat`
* `end_lng`

## Columns Used for Rider Analysis

The following column will be used to analyze rider categories:

* `member_casual`

This column can be used to compare member trips and casual rider trips.