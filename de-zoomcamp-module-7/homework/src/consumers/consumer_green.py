import argparse
from pathlib import Path

from kafka import KafkaConsumer

try:
    from src.models import ride_deserializer
except ModuleNotFoundError:
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from src.models import ride_deserializer


def parse_args():
    parser = argparse.ArgumentParser(description="Consume green taxi rides from Kafka/Redpanda.")
    parser.add_argument("--bootstrap-server", default="localhost:9092")
    parser.add_argument("--topic", default="green-rides")
    parser.add_argument("--group-id", default="green-rides-console")
    parser.add_argument("--max-messages", type=int, default=10)
    return parser.parse_args()


def main():
    args = parse_args()
    consumer = KafkaConsumer(
        args.topic,
        bootstrap_servers=[args.bootstrap_server],
        auto_offset_reset="earliest",
        group_id=args.group_id,
        value_deserializer=ride_deserializer,
    )

    print(f"Listening for green taxi rides on '{args.topic}'...")

    count = 0
    for message in consumer:
        print(message.value)
        count += 1
        if count >= args.max_messages:
            break

    consumer.close()
    print(f"Done. Read {count} messages.")


if __name__ == "__main__":
    main()
