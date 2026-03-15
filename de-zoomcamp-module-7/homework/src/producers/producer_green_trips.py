import argparse
import json
from pathlib import Path
from time import time

import pandas as pd
from kafka import KafkaProducer


DATA_FILE = Path(__file__).resolve().parents[2] / "green_tripdata_2025-10.parquet"
REQUIRED_COLUMNS = [
    "lpep_pickup_datetime",
    "lpep_dropoff_datetime",
    "PULocationID",
    "DOLocationID",
    "passenger_count",
    "trip_distance",
    "tip_amount",
    "total_amount",
]
DATETIME_COLUMNS = [
    "lpep_pickup_datetime",
    "lpep_dropoff_datetime",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Send the full Green Taxi homework dataset to Redpanda."
    )
    parser.add_argument("--bootstrap-server", default="localhost:9092")
    parser.add_argument("--topic", default="green-trips")
    return parser.parse_args()


def load_records():
    df = pd.read_parquet(DATA_FILE, columns=REQUIRED_COLUMNS).copy()
    for column in DATETIME_COLUMNS:
        df[column] = df[column].dt.strftime("%Y-%m-%d %H:%M:%S")
    df = df.astype(object).where(pd.notna(df), None)
    return df.to_dict(orient="records")


def main():
    args = parse_args()
    producer = KafkaProducer(
        bootstrap_servers=[args.bootstrap_server],
        value_serializer=lambda row: json.dumps(row, allow_nan=False).encode("utf-8"),
    )
    records = load_records()

    t0 = time()
    for record in records:
        producer.send(args.topic, value=record)
    producer.flush()
    t1 = time()
    producer.close()

    print(f"Sent {len(records)} records to '{args.topic}'")
    print(f"took {(t1 - t0):.2f} seconds")


if __name__ == "__main__":
    main()
