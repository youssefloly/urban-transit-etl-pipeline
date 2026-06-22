from __future__ import annotations

from src.ingestion import OUTPUT_FILE, run_ingestion
from src.schema_validation import (
    SCHEMA_REPORT_PATH,
    save_validation_report,
    validate_schema,
)


def run_ingestion_validation():
    """
    Run the ingestion stage first, then validate the resulting dataframe schema.
    """
    files_list, dataframe = run_ingestion()

    validation_report = validate_schema(dataframe)
    validation_report["files_read"] = files_list
    validation_report["ingested_file"] = str(OUTPUT_FILE)

    save_validation_report(validation_report, SCHEMA_REPORT_PATH)

    if not validation_report["schema_valid"]:
        raise ValueError(
            f"Schema validation failed. Check report: {SCHEMA_REPORT_PATH}"
        )

    print("\nIngestion + Schema Validation completed successfully.")
    print(f"Files read: {len(files_list)}")
    print(f"Rows: {validation_report['row_count']}")
    print(f"Columns: {validation_report['column_count']}")
    print(f"Report: {SCHEMA_REPORT_PATH}")

    return dataframe, validation_report


if __name__ == "__main__":
    run_ingestion_validation()
