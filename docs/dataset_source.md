# Dataset Source

## Project Name

Urban Transit ETL Pipeline

## Dataset Name

NYC Citi Bike Trip Data - January 2024

## Domain

Urban Transit / Bike Sharing

## Source

NYC Citi Bike System Data

Official source page:
https://citibikenyc.com/system-data

Direct data index:
https://s3.amazonaws.com/tripdata/index.html

## Source Type

Public open dataset

## Raw Files Used

The dataset was downloaded as a compressed ZIP file and extracted into two CSV files.

Raw files used in this project:

* `202401-citibike-tripdata.zip`
* `202401-citibike-tripdata_1.csv`
* `202401-citibike-tripdata_2.csv`

## File Format

CSV files extracted from a ZIP archive.

## Storage Location

The raw dataset files are stored in the following project directory:

```text
data/raw/
```

The raw files should not be edited manually. All data cleaning and transformation steps must be performed through Python code to keep the pipeline reproducible.

## Dataset Size

| Item                |     Value |
| ------------------- | --------: |
| Number of CSV files |         2 |
| Number of rows      | 1,888,085 |
| Number of columns   |        13 |

## Reason for Dataset Selection

This dataset was selected because it contains real trip-level urban mobility data from a bike-sharing transit system. It includes important fields such as trip identifier, bike type, start and end timestamps, station information, geographic coordinates, and rider type.

The dataset is suitable for a Data Engineering ETL pipeline because it supports:

* Raw CSV ingestion
* Schema validation
* Missing value detection
* Duplicate checking
* Timestamp transformation
* Trip duration calculation
* Data cleaning and standardization
* Parquet conversion
* BigQuery loading
* SQL-based analytics
* Dashboard or reporting support

## Expected Use in the ETL Pipeline

The dataset will be used as the raw input for the batch ETL pipeline. The pipeline will read the CSV files, validate the schema, clean and transform the data, convert the processed output to Apache Parquet format, and load the final dataset into Google BigQuery for analysis.

## Expected Analytics

After processing and loading the data into BigQuery, the dataset can support analytical queries such as:

* Total trips by day
* Total trips by hour
* Top start stations
* Top end stations
* Average trip duration
* Member vs casual rider distribution
* Bike type usage distribution
* Data quality checks
* Station activity analysis