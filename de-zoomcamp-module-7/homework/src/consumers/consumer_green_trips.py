import argparse
import json
from uuid import uuid4

from kafka import KafkaConsumer


def parse_args():
    parser = argparse.ArgumentParser(
        description="Count green-trips Kafka messages with trip_distance > 5."
    )
    parser.add_argument("--bootstrap-server", default="localhost:9092")
    parser.add_argument("--topic", default="green-trips")
    parser.add_argument(
        "--group-id",
        default=f"green-trips-distance-counter-{uuid4()}",
        help="Consumer group id. Defaults to a unique id so earliest offset is used cleanly.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    consumer = KafkaConsumer(
        args.topic,
        bootstrap_servers=[args.bootstrap_server],
        auto_offset_reset="earliest",
        group_id=args.group_id,
        value_deserializer=lambda value: json.loads(value.decode("utf-8")),
        consumer_timeout_ms=5000,
    )

    total = 0
    over_5 = 0
    for message in consumer:
        total += 1
        if float(message.value["trip_distance"]) > 5.0:
            over_5 += 1

    consumer.close()
    print(f"Consumed {total} messages from '{args.topic}'")
    print(f"Trips with trip_distance > 5: {over_5}")


if __name__ == "__main__":
    main()
