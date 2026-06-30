import os
from pathlib import Path
import polars as pl

# Definition of dynamic relative paths
INTERIM_DIR = Path("data/interim")
INPUT_FILE = INTERIM_DIR / "ingested_tripdata.csv"
OUTPUT_FILE = INTERIM_DIR / "transformed_tripdata.csv"


def transform_data(df: pl.DataFrame) -> pl.DataFrame:
    """
    Performs all data transformation steps: duration calculation,
    feature engineering, business rules application, and filtering.
    """
    print("Calculating trip duration...")
    # Reconstruct timestamps temporarily using pl.datetime() to calculate accurate duration
    df = df.with_columns([
        pl.datetime(
            pl.col("start_date").dt.year(),
            pl.col("start_date").dt.month(),
            pl.col("start_date").dt.day(),
            pl.col("start_time").str.strptime(pl.Time, "%I:%M:%S %p").dt.hour(),
            pl.col("start_time").str.strptime(pl.Time, "%I:%M:%S %p").dt.minute(),
            pl.col("start_time").str.strptime(pl.Time, "%I:%M:%S %p").dt.second()
        ).alias("start_datetime_tmp"),
        
        pl.datetime(
            pl.col("end_date").dt.year(),
            pl.col("end_date").dt.month(),
            pl.col("end_date").dt.day(),
            pl.col("end_time").str.strptime(pl.Time, "%I:%M:%S %p").dt.hour(),
            pl.col("end_time").str.strptime(pl.Time, "%I:%M:%S %p").dt.minute(),
            pl.col("end_time").str.strptime(pl.Time, "%I:%M:%S %p").dt.second()
        ).alias("end_datetime_tmp")
    ])

    # Calculate trip duration in minutes rounded to 2 decimal places
    df = df.with_columns(
        ((pl.col("end_datetime_tmp") - pl.col("start_datetime_tmp")).dt.total_seconds() / 60)
        .round(2)
        .alias("trip_duration_minutes")
    )

    # Filtering invalid business records (trips with zero or negative duration)
    print("Filtering invalid business records...")
    df = df.filter(pl.col("trip_duration_minutes") > 0)

    # Feature Engineering
    print("Extracting time features (Hour, Day of Week, Month)...")
    df = df.with_columns([
        pl.col("start_time").str.strptime(pl.Time, "%I:%M:%S %p").dt.hour().alias("pickup_hour"),
        pl.col("start_date").dt.strftime("%A").alias("day_of_week"),
        pl.col("start_date").dt.strftime("%B").alias("month_name")
    ])

    # Business Rules Application
    print("Applying business classification rules...")
    df = df.with_columns([
        # Categorize trip length
        pl.when(pl.col("trip_duration_minutes") < 10).then(pl.lit("Short Trip"))
        .when((pl.col("trip_duration_minutes") >= 10) & (pl.col("trip_duration_minutes") <= 30)).then(pl.lit("Medium Trip"))
        .otherwise(pl.lit("Long Trip"))
        .alias("trip_category"),
        
        # Categorize day type (Weekend vs Weekday based on Friday/Saturday)
        pl.when(pl.col("day_of_week").is_in(["Friday", "Saturday"])).then(pl.lit("Weekend"))
        .otherwise(pl.lit("Weekday"))
        .alias("day_type")
    ])

    # Drop temporary datetime calculation columns
    df = df.drop(["start_datetime_tmp", "end_datetime_tmp"])
    
    return df


def run_transformation():
    """
    Main function to execute the transformation pipeline.
    """
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found at: {INPUT_FILE}. Please run ingestion first.")

    print(f"Reading ingested data from: {INPUT_FILE}")
    
    # Updated: Enforce station IDs using schema_overrides to align with newest Polars versions
    df = pl.read_csv(
        INPUT_FILE, 
        try_parse_dates=True,
        schema_overrides={"start_station_id": pl.Utf8, "end_station_id": pl.Utf8}
    )

    # Execute transformations
    transformed_df = transform_data(df)

    # Save final results to interim directory
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    transformed_df.write_csv(OUTPUT_FILE)
    print(f"Saved transformed dataframe to: {OUTPUT_FILE}")
    
    print("\nProcess completed successfully!")
    print(f"Total row count after transformation: {transformed_df.height}")
    print("\nFirst 5 rows of the transformed DataFrame:")
    print(transformed_df.head(5))


if __name__ == "__main__":
    run_transformation()