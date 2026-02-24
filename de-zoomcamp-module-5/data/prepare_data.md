# Module 5 – Data Platforms with Bruin  
## NYC Taxi Pipeline Setup Documentation (Local DuckDB)

This document describes the exact steps I followed to set up and run a complete data pipeline using Bruin and DuckDB locally.

---

# Overview

Goal: Build an end-to-end data pipeline using Bruin with:

- Ingestion layer
- Staging layer
- Reporting layer
- DuckDB as the local data warehouse
- NYC Taxi dataset as source data

Pipeline architecture:

```
ingestion.trips              → raw taxi data
ingestion.payment_lookup    → lookup table

        ↓

staging.trips               → cleaned & deduplicated data

        ↓

reports.trips_report        → aggregated reporting table
```

---

# Step 1: Install Bruin CLI

Install Bruin using the official install script:

```bash
curl -LsSf https://getbruin.com/install/cli | sh
```

Restart terminal or run:

```bash
source $HOME/.bruin/env
```

Verify installation:

```bash
bruin version
```

---

# Step 2: Initialize Bruin Zoomcamp Project

Create project using zoomcamp template:

```bash
bruin init zoomcamp my-taxi-pipeline
```

Navigate into project:

```bash
cd my-taxi-pipeline
```

Project structure created:

```
my-taxi-pipeline/
│
├── .bruin.yml
├── pipeline/
│   ├── pipeline.yml
│   └── assets/
│       ├── ingestion/
│       ├── staging/
│       └── reports/
```

---

# Step 3: Configure DuckDB Connection

Open `.bruin.yml`

Ensure DuckDB connection exists:

```yaml
default_environment: default

environments:
  default:
    connections:
      duckdb:
        - name: duckdb-default
          path: duckdb.db
```

This creates a local DuckDB database file:

```
duckdb.db
```

---

# Step 4: Verify pipeline.yml configuration

Open:

```
pipeline/pipeline.yml
```

Ensure configuration:

```yaml
name: nyc_taxi
schedule: daily
start_date: "2022-01-01"

default_connections:
  duckdb: duckdb-default

variables:
  taxi_types:
    type: array
    items:
      type: string
    default: ["yellow"]
```

---

# Step 5: Fix ingestion.trips asset connection

File:

```
pipeline/assets/ingestion/trips.py
```

Ensure connection exists inside decorator:

```python
connection: duckdb-default
```

This allows Bruin to load data into DuckDB.

---

# Step 6: Implement materialize() function

Implemented logic to:

• Read start_date and end_date  
• Download parquet files from NYC Taxi dataset  
• Convert columns to standardized schema  
• Combine into single DataFrame  
• Return DataFrame to Bruin  

Example download URL format:

```
https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_YYYY-MM.parquet
```

---

# Step 7: Validate pipeline

Run validation:

```bash
bruin validate pipeline/pipeline.yml
```

Successful output:

```
Successfully validated assets across pipeline
```

---

# Step 8: Run pipeline

Execute pipeline:

```bash
bruin run pipeline/pipeline.yml \
  --start-date 2022-01-01 \
  --end-date 2022-02-01
```

Pipeline execution order:

```
1 ingestion.trips
2 ingestion.payment_lookup
3 staging.trips
4 reports.trips_report
```

Successful output example:

```
PASS ingestion.trips
PASS ingestion.payment_lookup
PASS staging.trips
PASS reports.trips_report
```

---

# Step 9: Verify data was loaded

Query ingestion layer:

```bash
bruin query --connection duckdb-default \
--query "SELECT COUNT(*) FROM ingestion.trips"
```

Query staging layer:

```bash
bruin query --connection duckdb-default \
--query "SELECT COUNT(*) FROM staging.trips"
```

Query report layer:

```bash
bruin query --connection duckdb-default \
--query "SELECT COUNT(*) FROM reports.trips_report"
```

---

# Step 10: Verify lineage

Run lineage command:

```bash
bruin lineage pipeline/assets/staging/trips.sql
```

Output:

```
Upstream Dependencies:
- ingestion.trips
- ingestion.payment_lookup

Downstream Dependencies:
- reports.trips_report
```

This confirms correct pipeline orchestration.

---

# Step 11: Final project architecture

```
Project
│
├── DuckDB database
│
├── ingestion layer
│   ├── ingestion.trips
│   └── ingestion.payment_lookup
│
├── staging layer
│   └── staging.trips
│
├── reports layer
│   └── reports.trips_report
│
└── Pipeline orchestration via Bruin
```

---