# PyFlink Streaming Workshop -- Setup Guide

## Environment

-   macOS (Apple Silicon ARM64)
-   Docker & Docker Compose
-   Python 3.12
-   uv package manager

## Architecture

Producer (Python) → Redpanda (Kafka) → Flink → PostgreSQL

## Start Redpanda

docker compose up redpanda -d

Verify:

docker compose ps

## Install Python dependencies

uv init -p 3.12 uv add kafka-python pandas pyarrow

## PostgreSQL

Start database:

docker compose up postgres -d

Connect:

uvx pgcli -h localhost -p 5432 -U postgres -d postgres

Create table:

CREATE TABLE processed_events ( PULocationID INTEGER, DOLocationID
INTEGER, trip_distance DOUBLE PRECISION, total_amount DOUBLE PRECISION,
pickup_datetime TIMESTAMP );

## Flink Setup

Download build files:

wget
https://raw.githubusercontent.com/DataTalksClub/data-engineering-zoomcamp/main/07-streaming/workshop/Dockerfile.flink
wget
https://raw.githubusercontent.com/DataTalksClub/data-engineering-zoomcamp/main/07-streaming/workshop/pyproject.flink.toml
wget
https://raw.githubusercontent.com/DataTalksClub/data-engineering-zoomcamp/main/07-streaming/workshop/flink-config.yaml

## Build Flink Image

docker compose build --no-cache

Start cluster:

docker compose up jobmanager taskmanager

Flink UI: http://localhost:8081

## Issues Faced

### pemja build error

Error: Failed to build pemja

Cause: PyFlink dependency requires Java headers during compilation.

### JAVA_HOME path issue

Error: Path /usr/lib/jvm/java-17-openjdk-amd64 does not exist

Cause: Apple Silicon uses ARM Java path instead of AMD.

Fix:

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64

Install required packages:

apt-get install -y openjdk-17-jdk gcc

Result: Docker image builds successfully and PyFlink runs correctly.
