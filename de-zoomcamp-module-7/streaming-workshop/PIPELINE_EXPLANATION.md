# PyFlink Streaming Workshop -- Pipeline Explanation

## Architecture

Producer (Python) → Kafka (Redpanda) → Flink → PostgreSQL

## Project Structure

src/ models.py producers/ producer.py consumers/ consumer.py
consumer_postgres.py job/ pass_through_job.py aggregation_job.py

## Shared Data Model

src/models.py

``` python
from dataclasses import dataclass

@dataclass
class Ride:
    PULocationID: int
    DOLocationID: int
    trip_distance: float
    total_amount: float
    tpep_pickup_datetime: int
```

## Producer

Location: src/producers/producer.py

Reads taxi trip parquet dataset and sends records to Kafka.

Dependencies:

uv add kafka-python pandas pyarrow

Example:

``` python
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

producer.send("rides", value=dataclasses.asdict(ride))
producer.flush()
```

## Consumer

Location: src/consumers/consumer.py

Consumes Kafka messages and prints rides.

``` python
consumer = KafkaConsumer(
    "rides",
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    group_id='rides-console'
)
```

## PostgreSQL Consumer

Location: src/consumers/consumer_postgres.py

Reads Kafka events and writes them to PostgreSQL.

Dependency:

uv add psycopg2-binary

Example insert:

``` python
INSERT INTO processed_events
(PULocationID, DOLocationID, trip_distance, total_amount, pickup_datetime)
VALUES (%s, %s, %s, %s, %s)
```

## Flink Jobs

### Pass-through Job

Reads events from Kafka and writes directly to PostgreSQL.

Kafka source: properties.bootstrap.servers = redpanda:29092

Sink connector: JDBC connector for PostgreSQL.

### Aggregation Job

Performs windowed aggregation using Flink SQL.

Example aggregation:

``` sql
SELECT
    window_start,
    PULocationID,
    COUNT(*) AS num_trips,
    SUM(total_amount) AS total_revenue
FROM TABLE(
    TUMBLE(TABLE events, DESCRIPTOR(event_timestamp), INTERVAL '1' HOUR)
)
GROUP BY window_start, PULocationID
```

Key concepts:

-   Tumbling windows
-   Watermarks
-   Checkpointing
-   Parallelism

Result: Flink processes streaming taxi data and stores processed results
in PostgreSQL.
