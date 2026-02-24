"""@bruin
name: ingestion.trips
type: python
image: python:3.11

connection: duckdb-default

materialization:
  type: table
  strategy: append

columns:
  - name: pickup_datetime
    type: timestamp
    description: "When the meter was engaged"
  - name: dropoff_datetime
    type: timestamp
    description: "When the meter was disengaged"
@bruin"""

import os
import json
import pandas as pd

def materialize():
    start_date = os.environ["BRUIN_START_DATE"]
    end_date = os.environ["BRUIN_END_DATE"]
    taxi_types = json.loads(os.environ["BRUIN_VARS"]).get("taxi_types", ["yellow"])
    
        # Convert to pandas timestamps
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)

    # Generate list of months between start and end dates
    # Fetch parquet files from:
    # https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year}-{month}.parquet
        # Generate all months between start and end
    months = pd.period_range(start=start, end=end, freq="M")

    all_dataframes = []

    for taxi_type in taxi_types:
        for period in months:
            year = period.year
            month = period.month

            url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year}-{month:02d}.parquet"

            print(f"Downloading {url}")

            try:
                df = pd.read_parquet(url)

                # Standardize column names across taxi types
                if taxi_type == "yellow":
                    df["pickup_datetime"] = df["tpep_pickup_datetime"]
                    df["dropoff_datetime"] = df["tpep_dropoff_datetime"]
                elif taxi_type == "green":
                    df["pickup_datetime"] = df["lpep_pickup_datetime"]
                    df["dropoff_datetime"] = df["lpep_dropoff_datetime"]

                df["taxi_type"] = taxi_type

                # Select only required columns
                df = df[[
                    "pickup_datetime",
                    "dropoff_datetime",
                    "PULocationID",
                    "DOLocationID",
                    "fare_amount",
                    "payment_type",
                    "taxi_type"
                ]]

                df.columns = [
                    "pickup_datetime",
                    "dropoff_datetime",
                    "pickup_location_id",
                    "dropoff_location_id",
                    "fare_amount",
                    "payment_type",
                    "taxi_type"
                ]

                all_dataframes.append(df)

            except Exception as e:
                print(f"Failed to download {url}: {e}")

    if not all_dataframes:
        raise ValueError("No data was downloaded")

    final_dataframe = pd.concat(all_dataframes, ignore_index=True)

    print(f"Total rows loaded: {len(final_dataframe)}")

    return final_dataframe