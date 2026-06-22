# Schema Validation

## Purpose

This stage validates the ingested Citi Bike trip dataset before the cleaning stage.

The ingestion stage produces the following intermediate file:

```text
data/interim/ingested_tripdata.csv
```

## Expected Columns

Because the ingestion stage splits `started_at` and `ended_at`, the validation stage expects these columns:

```text
ride_id
rideable_type
start_date
start_time
end_date
end_time
start_station_name
start_station_id
end_station_name
end_station_id
start_lat
start_lng
end_lat
end_lng
member_casual
source_file
```

## Validation Rules

- The ingested dataframe must not be empty.
- All expected columns must exist.
- `ride_id`, station IDs, station names, bike type, rider type, and `source_file` must be strings.
- Latitude and longitude columns must be numeric.
- `start_date` and `end_date` must follow `YYYY-MM-DD` format.
- `start_time` and `end_time` must follow `HH:MM:SS AM/PM` format.
- `member_casual` must contain only `member` or `casual`.
- `rideable_type` must contain expected bike categories.
- Duplicate `ride_id` values are reported as warnings.

## Output

The validation stage generates this report:

```text
logs/schema_validation_report.json
```

## Run Command

From the project root:

```bash
python -m src.run_ingestion_validation
```
