# Data Cleaning Rules

## Missing Values
- Missing station names are replaced with "Unknown Station".
- Missing station IDs are replaced with "Unknown_ID".
- Rows with missing coordinates are removed.

## Duplicate Handling
- Fully duplicated rows are removed.
- Duplicate ride_id values are removed while keeping the first occurrence.

## Text Cleaning
- Leading and trailing spaces are removed.
- Multiple spaces are replaced with a single space.
- Text values are converted to lowercase.

## Member Type Validation
Allowed values:
- member
- casual

Rows containing invalid member types are removed.

## Invalid Trip Removal
Trips are removed if:
- End datetime is earlier than start datetime.
- Trip duration is zero.
- Trip duration is negative.

## Outputs
The cleaning stage generates:
- cleaned_tripdata.csv
- cleaning_report.json