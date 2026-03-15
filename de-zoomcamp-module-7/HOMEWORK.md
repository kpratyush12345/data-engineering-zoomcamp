# Module 7 Homework Runbook

This guide explains how to run the homework in this repository from **Question 2 to Question 6** using only:

- `de-zoomcamp-module-7/homework`

This file is meant to help someone who clones the repo and wants a clean, repeatable way to execute the homework end-to-end.

## Folder Layout

- Notebook with questions: `de-zoomcamp-module-7/Questions.ipynb`
- Homework code and infrastructure: `de-zoomcamp-module-7/homework`

All commands below assume you are inside:

```bash
cd de-zoomcamp-module-7/homework
```

## Prerequisites

- Docker Desktop running
- Python environment available with `uv`
- Ports available:
  - `8081` for Flink UI
  - `9092` for Redpanda
  - `5432` for PostgreSQL

## One-Time Setup

Build and start the homework stack:

```bash
cd de-zoomcamp-module-7/homework
docker compose down -v
docker compose build
docker compose up -d
```

This starts:

- Redpanda at `localhost:9092`
- PostgreSQL at `localhost:5432`
- Flink UI at `http://localhost:8081`

Check containers:

```bash
docker compose ps
```

## Important Rules

- Always use the `homework` directory only.
- For Flink questions, submit jobs with:

```bash
docker compose exec jobmanager flink run -py /opt/src/job/<job_file>.py
```

- If you rerun a producer into the same topic, you will create duplicates.
- Before each Flink question, it is safest to recreate the topic and resend the data once.
- If Postgres tables are missing, run:

```bash
docker compose down -v
docker compose up -d
```

That recreates the DB volume and reruns the SQL init scripts.

## Question 2

Goal:
- Create topic `green-trips`
- Send the October 2025 green taxi data to Kafka/Redpanda
- Measure how long it takes

Create the topic:

```bash
docker exec homework-redpanda-1 rpk topic create green-trips
```

Run the producer:

```bash
uv run src/producers/producer_green_trips.py
```

Producer file:

- `de-zoomcamp-module-7/homework/src/producers/producer_green_trips.py`

What it does:

- Reads `green_tripdata_2025-10.parquet`
- Keeps only:
  - `lpep_pickup_datetime`
  - `lpep_dropoff_datetime`
  - `PULocationID`
  - `DOLocationID`
  - `passenger_count`
  - `trip_distance`
  - `tip_amount`
  - `total_amount`
- Converts datetime columns to strings
- Sends JSON rows to `green-trips`
- Prints total send time

Expected output shape:

```text
Sent 49416 records to 'green-trips'
took X.XX seconds
```

Observed answer in this repo:

- Closest answer: `10 seconds`

## Question 3

Goal:
- Read all messages from `green-trips`
- Count trips where `trip_distance > 5`

Consumer file:

- `de-zoomcamp-module-7/homework/src/consumers/consumer_green_trips.py`

Run it:

```bash
uv run src/consumers/consumer_green_trips.py
```

Expected output shape:

```text
Consumed 49416 messages from 'green-trips'
Trips with trip_distance > 5: 8506
```

Expected answer:

- `8506`

Important:

- If the message count is larger than `49416`, you sent data more than once.
- If that happens, recreate the topic and resend once:

```bash
docker exec homework-redpanda-1 rpk topic delete green-trips
docker exec homework-redpanda-1 rpk topic create green-trips
uv run src/producers/producer_green_trips.py
uv run src/consumers/consumer_green_trips.py
```

## Part 2: PyFlink

For Questions 4, 5, and 6:

- Topic is `green-trips`
- Event time comes from `lpep_pickup_datetime`
- Timestamps are strings, not epoch milliseconds
- Parallelism is set to `1`

Before each Flink question, use a clean topic to avoid duplicate results:

```bash
docker exec homework-redpanda-1 rpk topic delete green-trips
docker exec homework-redpanda-1 rpk topic create green-trips
uv run src/producers/producer_green_trips.py
```

You can inspect running Flink jobs:

```bash
docker compose exec jobmanager flink list
```

You can cancel a running job:

```bash
docker compose exec jobmanager flink cancel <job_id>
```

You can also use the Flink UI:

- `http://localhost:8081`

To open Postgres interactively:

```bash
docker compose exec postgres psql -U postgres -d postgres
```

Useful `psql` commands:

- `\dt`
- `\d green_trips_q4`
- `\d green_trips_q5`
- `\d green_trips_q6`
- `\q`

## Question 4

Goal:
- 5-minute tumbling window
- Count trips per `PULocationID`
- Store:
  - `window_start`
  - `PULocationID`
  - `num_trips`

Flink job file:

- `de-zoomcamp-module-7/homework/src/job/homework_q4_job.py`

Safe clean run:

```bash
docker exec homework-redpanda-1 rpk topic delete green-trips
docker exec homework-redpanda-1 rpk topic create green-trips
uv run src/producers/producer_green_trips.py
docker compose exec postgres psql -U postgres -d postgres -c "TRUNCATE TABLE green_trips_q4;"
docker compose exec jobmanager flink run -py /opt/src/job/homework_q4_job.py
```

Wait a little for the job to process the topic, then query:

```bash
docker compose exec postgres psql -U postgres -d postgres
```

```sql
SELECT PULocationID, num_trips
FROM green_trips_q4
ORDER BY num_trips DESC
LIMIT 3;
```

Expected answer:

- `74`

## Question 5

Goal:
- 5-minute session window
- Partition sessions by `PULocationID`
- Use `lpep_pickup_datetime` as event time
- Watermark tolerance is 5 seconds
- Find the location with the longest session

Flink job file:

- `de-zoomcamp-module-7/homework/src/job/homework_q5_job.py`

Important:

- This job must partition the session window by `PULocationID`
- The topic must be clean
- The result table should be truncated before rerunning

Safe clean run:

```bash
docker exec homework-redpanda-1 rpk topic delete green-trips
docker exec homework-redpanda-1 rpk topic create green-trips
uv run src/producers/producer_green_trips.py
docker compose exec postgres psql -U postgres -d postgres -c "TRUNCATE TABLE green_trips_q5;"
docker compose exec jobmanager flink run -py /opt/src/job/homework_q5_job.py
```

Query result:

```bash
docker compose exec postgres psql -U postgres -d postgres
```

```sql
SELECT PULocationID, num_trips
FROM green_trips_q5
ORDER BY num_trips DESC
LIMIT 5;
```

Expected answer:

- Intended multiple-choice answer: `81`

Note:

- A raw local calculation in this repo produced a top session very close to that value.
- Use the multiple-choice option `81`.

## Question 6

Goal:
- 1-hour tumbling window
- Sum `tip_amount` across all locations
- Find the hour with the highest total tips

Flink job file:

- `de-zoomcamp-module-7/homework/src/job/homework_q6_job.py`

Safe clean run:

```bash
docker exec homework-redpanda-1 rpk topic delete green-trips
docker exec homework-redpanda-1 rpk topic create green-trips
uv run src/producers/producer_green_trips.py
docker compose exec postgres psql -U postgres -d postgres -c "TRUNCATE TABLE green_trips_q6;"
docker compose exec jobmanager flink run -py /opt/src/job/homework_q6_job.py
```

Query result:

```bash
docker compose exec postgres psql -U postgres -d postgres
```

```sql
SELECT window_start, total_tip_amount
FROM green_trips_q6
ORDER BY total_tip_amount DESC
LIMIT 5;
```

Expected answer:

- `2025-10-16 18:00:00`

## Final Answers

- Question 2: `10 seconds`
- Question 3: `8506`
- Question 4: `74`
- Question 5: `81`
- Question 6: `2025-10-16 18:00:00`

## Troubleshooting

### Flink job is restarting

Check jobs:

```bash
docker compose exec jobmanager flink list
```

Check logs:

```bash
docker compose logs --tail=200 jobmanager
docker compose logs --tail=200 taskmanager
```

### Topic has duplicate data

Delete and recreate it:

```bash
docker exec homework-redpanda-1 rpk topic delete green-trips
docker exec homework-redpanda-1 rpk topic create green-trips
uv run src/producers/producer_green_trips.py
```

### Postgres table does not exist

Recreate containers and volumes:

```bash
docker compose down -v
docker compose up -d
```

### Flink job writes no rows

Check:

- topic exists
- topic has data
- job is `RUNNING`
- table exists in Postgres

Verify topic:

```bash
docker exec homework-redpanda-1 rpk topic describe green-trips -p
```

Verify tables:

```bash
docker compose exec postgres psql -U postgres -d postgres -c "\\dt"
```

## Files Used

- Producer: `de-zoomcamp-module-7/homework/src/producers/producer_green_trips.py`
- Consumer: `de-zoomcamp-module-7/homework/src/consumers/consumer_green_trips.py`
- Q4 job: `de-zoomcamp-module-7/homework/src/job/homework_q4_job.py`
- Q5 job: `de-zoomcamp-module-7/homework/src/job/homework_q5_job.py`
- Q6 job: `de-zoomcamp-module-7/homework/src/job/homework_q6_job.py`
- Postgres init: `de-zoomcamp-module-7/homework/postgres-init/01-create-tables.sql`
