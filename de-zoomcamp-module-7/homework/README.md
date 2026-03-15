# Module 7 Homework Setup (Green Taxi Streaming)

This homework streams **Green Taxi trips (October 2025)** with:

- Redpanda (Kafka-compatible broker)
- PyFlink
- PostgreSQL

Data file used in this folder:

- `green_tripdata_2025-10.parquet`

## 1) Start infrastructure

From this directory:

```bash
cd de-zoomcamp-module-7/homework
docker compose build
docker compose up -d
```

This starts:

- Redpanda on `localhost:9092`
- Flink Job Manager UI on `http://localhost:8081`
- Flink Task Manager
- PostgreSQL on `localhost:5432` (`postgres/postgres`)

If you previously ran containers and want a clean restart:

```bash
docker compose down -v
docker compose build
docker compose up -d
```

## 2) Run local producer (send rides to Redpanda)

```bash
uv run src/producers/producer_green_trips.py
```

Useful options:

```bash
uv run src/producers/producer_green_trips.py --topic green-trips
```

## 3) Submit pass-through Flink job

```bash
docker compose exec jobmanager flink run -py /opt/src/job/homework_job.py
```

The pass-through job reads topic `green-trips` and writes to Postgres table `green_trips_processed`.

Do not use plain `python /opt/src/job/homework_job.py` here. That starts PyFlink inside the container process, but it does not show up as a submitted Flink job in the dashboard.

## 4) Submit aggregation Flink job

```bash
docker compose exec jobmanager flink run -py /opt/src/job/homework_aggregation_job.py
```

The aggregation job reads topic `green-trips` and writes hourly aggregates to `green_trips_aggregated`.

## 5) Optional: local consumer check

```bash
uv run src/consumers/consumer_green_trips.py
```

## Notes

- Postgres tables are auto-created via `postgres-init/01-create-tables.sql`.
- Kafka source in both Flink jobs uses `earliest-offset`, so you can replay existing data in the topic.
- Both Flink jobs use `env.set_parallelism(1)` because `green-trips` has one partition.
- Container names depend on directory name (`homework-...` if this directory is `homework`).
