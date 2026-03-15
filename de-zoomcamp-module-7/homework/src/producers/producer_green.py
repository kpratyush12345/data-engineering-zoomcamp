import argparse
import dataclasses
import json
import time
from pathlib import Path

import pandas as pd
from kafka import KafkaProducer

try:
    from src.models import GreenRide
except ModuleNotFoundError:
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from src.models import GreenRide


DATA_FILE = Path(__file__).resolve().parents[2] / "green_tripdata_2025-10.parquet"


def ride_serializer(ride):
    ride_dict = dataclasses.asdict(ride)
    json_str = json.dumps(ride_dict)
    return json_str.encode("utf-8")


def ride_from_row(row):
    return GreenRide(
        PULocationID=int(row["PULocationID"]),
        DOLocationID=int(row["DOLocationID"]),
        trip_distance=float(row["trip_distance"]),
        total_amount=float(row["total_amount"]),
        lpep_pickup_datetime=int(row["lpep_pickup_datetime"].timestamp() * 1000),
    )


def parse_args():
    parser = argparse.ArgumentParser(description="Stream green taxi rides to Kafka/Redpanda.")
    parser.add_argument("--bootstrap-server", default="localhost:9092")
    parser.add_argument("--topic", default="green-rides")
    parser.add_argument("--limit", type=int, default=None, help="Max records to send")
    parser.add_argument("--sleep-seconds", type=float, default=0.0)
    return parser.parse_args()


def main():
    args = parse_args()

    df = pd.read_parquet(DATA_FILE)
    if args.limit:
        df = df.head(args.limit)

    producer = KafkaProducer(
        bootstrap_servers=[args.bootstrap_server],
        value_serializer=ride_serializer,
    )

    print(f"Sending {len(df)} rides to topic '{args.topic}'...")
    sent = 0
    try:
        for _, row in df.iterrows():
            ride = ride_from_row(row)
            producer.send(args.topic, value=ride)
            sent += 1
            if sent % 1000 == 0:
                print(f"Sent {sent} rides...")
            time.sleep(args.sleep_seconds)
    finally:
        producer.flush()
        producer.close()

    print(f"Done. Sent {sent} rides.")


if __name__ == "__main__":
    main()
