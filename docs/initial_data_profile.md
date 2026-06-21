# Initial Data Profile

## Project Name

Urban Transit ETL Pipeline

## Dataset Name

NYC Citi Bike Trip Data - January 2024

## Profiling Tool

The initial profiling was performed using Python and Polars inside the following notebook:

```text
notebooks/01_data_collection_and_profiling.ipynb
```

## Dataset Overview

| Item                       |     Value |
| -------------------------- | --------: |
| Number of CSV files        |         2 |
| Number of rows             | 1,888,085 |
| Number of columns          |        13 |
| Duplicate rows             |         0 |
| Duplicate `ride_id` values |         0 |

## Raw Files

The following files were found and read successfully:

* `202401-citibike-tripdata_1.csv`
* `202401-citibike-tripdata_2.csv`

## Column List

The dataset contains the following 13 columns:

1. `ride_id`
2. `rideable_type`
3. `started_at`
4. `ended_at`
5. `start_station_name`
6. `start_station_id`
7. `end_station_name`
8. `end_station_id`
9. `start_lat`
10. `start_lng`
11. `end_lat`
12. `end_lng`
13. `member_casual`

## Detected Schema

| Column Name          | Detected Data Type |
| -------------------- | ------------------ |
| `ride_id`            | String             |
| `rideable_type`      | String             |
| `started_at`         | Datetime           |
| `ended_at`           | Datetime           |
| `start_station_name` | String             |
| `start_station_id`   | String             |
| `end_station_name`   | String             |
| `end_station_id`     | String             |
| `start_lat`          | Float64            |
| `start_lng`          | Float64            |
| `end_lat`            | Float64            |
| `end_lng`            | Float64            |
| `member_casual`      | String             |

## Missing Values Summary

| Column Name          | Missing Count | Missing Percentage |
| -------------------- | ------------: | -----------------: |
| `ride_id`            |             0 |              0.00% |
| `rideable_type`      |             0 |              0.00% |
| `started_at`         |             0 |              0.00% |
| `ended_at`           |             0 |              0.00% |
| `start_station_name` |         1,160 |              0.06% |
| `start_station_id`   |         1,160 |              0.06% |
| `end_station_name`   |         5,505 |              0.29% |
| `end_station_id`     |         5,505 |              0.29% |
| `start_lat`          |         1,160 |              0.06% |
| `start_lng`          |         1,160 |              0.06% |
| `end_lat`            |         5,486 |              0.29% |
| `end_lng`            |         5,486 |              0.29% |
| `member_casual`      |             0 |              0.00% |

## Duplicate Checks

| Check                      | Result |
| -------------------------- | -----: |
| Duplicate full rows        |      0 |
| Duplicate `ride_id` values |      0 |

## Date Range

| Field                | Value                   |
| -------------------- | ----------------------- |
| Minimum `started_at` | 2023-12-31 02:36:55.648 |
| Maximum `started_at` | 2024-01-31 23:58:30.270 |
| Minimum `ended_at`   | 2024-01-01 00:00:08.272 |
| Maximum `ended_at`   | 2024-01-31 23:59:56.370 |

## Initial Findings

The dataset was successfully loaded using Polars from two CSV files. The two files have the same structure and were combined into one dataframe for profiling.

The dataset contains 1,888,085 rows and 13 columns, which makes it suitable for demonstrating a realistic batch ETL pipeline.

No duplicate rows were found, and no duplicate `ride_id` values were detected. This indicates that `ride_id` can be used as a unique trip identifier.

Some missing values were found in station and coordinate-related columns. The missing percentages are low, ranging from 0.06% to 0.29%. These missing values will be handled later in the cleaning stage according to predefined business rules.

The date range mostly covers January 2024. One `started_at` value appears on 2023-12-31, while the corresponding trip ended on 2024-01-01. This is acceptable because some trips may start before midnight and end in the target month.

## Data Quality Issues Identified

The initial profiling identified the following data quality issues:

* Missing start station names and IDs
* Missing end station names and IDs
* Missing start coordinates in some records
* Missing end coordinates in some records
* Trips that may cross from the previous day into January 2024

These issues will be handled in the next ETL stages through schema validation, cleaning, and transformation.

## Decision

The dataset is suitable for the Urban Transit ETL Pipeline project.

It supports all required Data Engineering stages, including:

* Data ingestion from raw CSV files
* Schema validation
* Data cleaning
* Data transformation
* Post-transformation validation
* Conversion to Apache Parquet
* Loading into Google BigQuery
* SQL analytics
* Logging and monitoring
* Final documentation and presentation