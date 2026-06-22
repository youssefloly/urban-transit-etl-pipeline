from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json
import re
from typing import Any

import polars as pl


INGESTED_FILE = Path("data/interim/ingested_tripdata.csv")
SCHEMA_REPORT_PATH = Path("logs/schema_validation_report.json")

EXPECTED_COLUMNS = [
    "ride_id",
    "rideable_type",
    "start_date",
    "start_time",
    "end_date",
    "end_time",
    "start_station_name",
    "start_station_id",
    "end_station_name",
    "end_station_id",
    "start_lat",
    "start_lng",
    "end_lat",
    "end_lng",
    "member_casual",
    "source_file",
]

STRING_COLUMNS = [
    "ride_id",
    "rideable_type",
    "start_station_name",
    "start_station_id",
    "end_station_name",
    "end_station_id",
    "member_casual",
    "source_file",
]

FLOAT_COLUMNS = ["start_lat", "start_lng", "end_lat", "end_lng"]
DATE_COLUMNS = ["start_date", "end_date"]
TIME_COLUMNS = ["start_time", "end_time"]

EXPECTED_CATEGORICAL_VALUES = {
    "rideable_type": {"classic_bike", "electric_bike", "docked_bike"},
    "member_casual": {"member", "casual"},
}

SCHEMA_OVERRIDES = {
    "ride_id": pl.Utf8,
    "rideable_type": pl.Utf8,
    "start_date": pl.Utf8,
    "start_time": pl.Utf8,
    "end_date": pl.Utf8,
    "end_time": pl.Utf8,
    "start_station_name": pl.Utf8,
    "start_station_id": pl.Utf8,
    "end_station_name": pl.Utf8,
    "end_station_id": pl.Utf8,
    "start_lat": pl.Float64,
    "start_lng": pl.Float64,
    "end_lat": pl.Float64,
    "end_lng": pl.Float64,
    "member_casual": pl.Utf8,
    "source_file": pl.Utf8,
}

TIME_PATTERN = re.compile(r"^(0[1-9]|1[0-2]):[0-5][0-9]:[0-5][0-9] (AM|PM)$")


def read_ingested_data(input_file: Path = INGESTED_FILE) -> pl.DataFrame:
    """Read the ingested CSV output produced by the ingestion stage."""
    if not input_file.exists():
        raise FileNotFoundError(f"Ingested file not found: {input_file}")

    return pl.read_csv(
        input_file,
        schema_overrides=SCHEMA_OVERRIDES,
        try_parse_dates=False,
        null_values=["", "NULL", "null", "None"],
    )


def create_report_template(df: pl.DataFrame) -> dict[str, Any]:
    actual_columns = df.columns
    missing_columns = [col for col in EXPECTED_COLUMNS if col not in actual_columns]
    extra_columns = [col for col in actual_columns if col not in EXPECTED_COLUMNS]

    return {
        "validation_time": datetime.now().isoformat(timespec="seconds"),
        "schema_valid": True,
        "row_count": df.height,
        "column_count": len(actual_columns),
        "expected_columns_count": len(EXPECTED_COLUMNS),
        "expected_columns": EXPECTED_COLUMNS,
        "actual_columns": actual_columns,
        "missing_columns": missing_columns,
        "extra_columns": extra_columns,
        "dtype_checks": {},
        "date_checks": {},
        "time_checks": {},
        "categorical_checks": {},
        "uniqueness_checks": {},
        "warnings": [],
        "errors": [],
    }


def validate_required_structure(df: pl.DataFrame, report: dict[str, Any]) -> None:
    if df.height == 0:
        report["schema_valid"] = False
        report["errors"].append("The ingested dataframe is empty.")

    if report["missing_columns"]:
        report["schema_valid"] = False
        report["errors"].append(
            f"Missing required columns: {report['missing_columns']}"
        )

    if report["extra_columns"]:
        report["warnings"].append(
            f"Extra columns found: {report['extra_columns']}"
        )


def validate_string_columns(df: pl.DataFrame, report: dict[str, Any]) -> None:
    for column in STRING_COLUMNS:
        if column not in df.columns:
            continue

        dtype = df[column].dtype
        null_count = df[column].null_count()
        report["dtype_checks"][column] = {
            "expected": "String/Utf8",
            "actual": str(dtype),
            "null_count": null_count,
        }

        if dtype != pl.Utf8:
            report["schema_valid"] = False
            report["errors"].append(
                f"{column} must be String/Utf8, found {dtype}."
            )


def validate_float_columns(df: pl.DataFrame, report: dict[str, Any]) -> None:
    for column in FLOAT_COLUMNS:
        if column not in df.columns:
            continue

        dtype = df[column].dtype
        null_count = df[column].null_count()
        report["dtype_checks"][column] = {
            "expected": "Float32 or Float64",
            "actual": str(dtype),
            "null_count": null_count,
        }

        if dtype not in [pl.Float32, pl.Float64]:
            report["schema_valid"] = False
            report["errors"].append(
                f"{column} must be Float32 or Float64, found {dtype}."
            )


def validate_date_columns(df: pl.DataFrame, report: dict[str, Any]) -> None:
    for column in DATE_COLUMNS:
        if column not in df.columns:
            continue

        if df[column].dtype == pl.Date:
            failed_parse_count = 0
        else:
            parsed = df.select(
                pl.col(column).str.strptime(pl.Date, "%Y-%m-%d", strict=False).alias("parsed_date")
            )
            failed_parse_count = df.filter(
                pl.col(column).is_not_null() & parsed["parsed_date"].is_null()
            ).height

        report["date_checks"][column] = {
            "expected": "YYYY-MM-DD date format",
            "failed_parse_count": failed_parse_count,
        }

        if failed_parse_count > 0:
            report["schema_valid"] = False
            report["errors"].append(
                f"{column} contains {failed_parse_count} values that cannot be parsed as a date."
            )


def validate_time_columns(df: pl.DataFrame, report: dict[str, Any]) -> None:
    for column in TIME_COLUMNS:
        if column not in df.columns:
            continue

        invalid_count = df.filter(
            pl.col(column).is_not_null()
            & ~pl.col(column).str.contains(TIME_PATTERN.pattern)
        ).height

        report["time_checks"][column] = {
            "expected": "12-hour time format: HH:MM:SS AM/PM",
            "failed_parse_count": invalid_count,
        }

        if invalid_count > 0:
            report["schema_valid"] = False
            report["errors"].append(
                f"{column} contains {invalid_count} values that do not match HH:MM:SS AM/PM format."
            )


def validate_categorical_columns(df: pl.DataFrame, report: dict[str, Any]) -> None:
    for column, allowed_values in EXPECTED_CATEGORICAL_VALUES.items():
        if column not in df.columns:
            continue

        actual_values = set(df[column].drop_nulls().unique().to_list())
        invalid_values = sorted(actual_values - allowed_values)

        report["categorical_checks"][column] = {
            "allowed_values": sorted(allowed_values),
            "invalid_values": invalid_values,
        }

        if invalid_values:
            report["schema_valid"] = False
            report["errors"].append(
                f"{column} contains unexpected values: {invalid_values}."
            )


def validate_unique_ride_id(df: pl.DataFrame, report: dict[str, Any]) -> None:
    if "ride_id" not in df.columns:
        return

    duplicate_ride_id_count = df.height - df.select("ride_id").unique().height
    report["uniqueness_checks"]["ride_id"] = {
        "duplicate_count": duplicate_ride_id_count,
    }

    if duplicate_ride_id_count > 0:
        report["warnings"].append(
            f"ride_id contains {duplicate_ride_id_count} duplicate values."
        )


def validate_schema(df: pl.DataFrame) -> dict[str, Any]:
    """Validate the ingested dataframe structure and return a JSON-ready report."""
    report = create_report_template(df)

    validate_required_structure(df, report)

    if report["missing_columns"]:
        return report

    validate_string_columns(df, report)
    validate_float_columns(df, report)
    validate_date_columns(df, report)
    validate_time_columns(df, report)
    validate_categorical_columns(df, report)
    validate_unique_ride_id(df, report)

    return report


def save_validation_report(
    report: dict[str, Any],
    output_path: Path = SCHEMA_REPORT_PATH,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, ensure_ascii=False)

    print(f"Schema validation report saved to: {output_path}")


def run_schema_validation(input_file: Path = INGESTED_FILE) -> dict[str, Any]:
    df = read_ingested_data(input_file)
    report = validate_schema(df)
    save_validation_report(report)

    if not report["schema_valid"]:
        raise ValueError(
            f"Schema validation failed. Check report: {SCHEMA_REPORT_PATH}"
        )

    print("Schema validation completed successfully.")
    print(f"Rows validated: {report['row_count']}")
    print(f"Columns validated: {report['column_count']}")

    return report


if __name__ == "__main__":
    run_schema_validation()
