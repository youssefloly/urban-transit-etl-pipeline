# Urban Transit ETL Pipeline

## Project Overview

Urban Transit ETL Pipeline is a Data Engineering graduation project developed as part of the Digital Egypt Pioneers Initiative (DEPI / Roa'd Masr El Rakameya).

The project aims to build a modern batch ETL pipeline for urban transit open data. The pipeline ingests raw CSV files, validates the schema, cleans and transforms the data using Python, stores the processed output in Apache Parquet format, loads the final data into Google BigQuery, and runs SQL queries for basic analytics.

This project is designed as an educational and practical Data Engineering portfolio project.

---

## Team

This project was developed by Team 4.

Team members:

* Ahmed Ayman Soliman
* Mohammed Khaled Ahmed
* Mohammed Ezzat Mohammed
* Rokaya Mohammed Elsaid Ahmed
* May Mohammed Massoud
* Yousef Loley Abdelrahman

---

## Project Goal

The goal of this project is to demonstrate the full Data Engineering lifecycle using a practical urban transit dataset.

The pipeline covers:

* Data collection
* Data ingestion
* Data profiling
* Schema validation
* Data cleaning
* Data transformation
* Post-transformation validation
* Parquet conversion
* BigQuery loading
* SQL analytics
* Automation and scheduling
* Logging and monitoring
* Technical documentation
* Final presentation and demo

---

## Dataset

The dataset used in this project is:

**NYC Citi Bike Trip Data - January 2024**

This dataset contains trip-level bike-sharing records, including trip IDs, bike types, start and end timestamps, station information, geographic coordinates, and rider type.

### Dataset Source

Official source page:

```text
https://citibikenyc.com/system-data
```

Direct data index:

```text
https://s3.amazonaws.com/tripdata/index.html
```

### Raw File Used

```text
202401-citibike-tripdata.zip
```

After extraction, the dataset contains two CSV files:

```text
202401-citibike-tripdata_1.csv
202401-citibike-tripdata_2.csv
```

> Note: Raw data files are not uploaded to GitHub because they are large. The dataset can be downloaded from the official source links above.

---

## Initial Data Profile

The initial profiling was performed using Python and Polars.

### Dataset Summary

| Metric              |     Value |
| ------------------- | --------: |
| Number of CSV files |         2 |
| Number of rows      | 1,888,085 |
| Number of columns   |        13 |
| Duplicate rows      |         0 |
| Duplicate ride IDs  |         0 |

### Columns

The dataset contains the following columns:

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

### Missing Values Summary

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

### Date Range

| Field                | Value                   |
| -------------------- | ----------------------- |
| Minimum `started_at` | 2023-12-31 02:36:55.648 |
| Maximum `started_at` | 2024-01-31 23:58:30.270 |
| Minimum `ended_at`   | 2024-01-01 00:00:08.272 |
| Maximum `ended_at`   | 2024-01-31 23:59:56.370 |

---

## Expected Pipeline Flow

```text
Raw CSV Data
→ Data Ingestion
→ Schema Validation
→ Data Cleaning
→ Data Transformation
→ Post-Transformation Validation
→ Convert to Parquet
→ Load to BigQuery
→ SQL Queries / Basic Analytics
→ Automation / Scheduling
→ Logging & Monitoring
→ Documentation
→ Final Presentation & Demo
```

---

## Technologies Used

* Python 3.x
* Polars
* Pandas
* Apache Parquet
* Google BigQuery
* Cron or Apache Airflow
* GitHub
* Markdown documentation
* Jupyter Notebook

---

## Project Structure

```text
urban-transit-etl-pipeline/
│
├── data/
│   ├── raw/
│   │   └── .gitkeep
│   ├── interim/
│   │   └── .gitkeep
│   └── processed/
│       └── .gitkeep
│
├── docs/
│   ├── dataset_source.md
│   ├── data_dictionary.md
│   └── initial_data_profile.md
│
├── notebooks/
│   └── 01_data_collection_and_profiling.ipynb
│
├── src/
│
├── logs/
│   └── .gitkeep
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Completed Work

### 1. Data Collection

The dataset was selected from a public and reputable urban transit data source. The raw ZIP file was downloaded and extracted locally.

### 2. Initial Data Profiling

The raw CSV files were loaded using Polars. The dataset structure, column names, data types, missing values, duplicate rows, duplicate ride IDs, and date range were inspected.

### 3. Documentation

The following documentation files were created:

* `docs/dataset_source.md`
* `docs/data_dictionary.md`
* `docs/initial_data_profile.md`

---

## Current Status

The project is currently in the Data Collection and Initial Profiling stage.

The dataset has been confirmed as suitable for the ETL pipeline because it:

* Contains real urban transit trip-level data
* Has a clear and consistent schema
* Contains more than 1.8 million records
* Includes useful fields for analytics
* Contains some missing values for cleaning practice
* Has no duplicate full rows
* Has no duplicate ride IDs

---

## Next Steps

The next development stages are:

1. Build a reusable data ingestion module
2. Define the expected schema
3. Implement schema validation
4. Clean missing and invalid values
5. Transform the dataset into analytics-ready tables
6. Convert processed data to Parquet
7. Load the processed data into Google BigQuery
8. Write BigQuery SQL analytics queries
9. Add automation, logging, and monitoring
10. Prepare the final report and presentation

---

## Notes

Raw dataset files are excluded from this repository because of their large file size.

To reproduce the project:

1. Download the dataset from the official Citi Bike source.
2. Place the ZIP and extracted CSV files inside:

```text
data/raw/
```

3. Run the notebook:

```text
notebooks/01_data_collection_and_profiling.ipynb
```

---

## Project Type

Educational Data Engineering graduation project.

## Deadline

17 July 2026.