# 🚕 NYC Taxi dlt Pipeline — Homework Setup Guide

This project builds a custom **dlt pipeline** that:

- Extracts NYC Yellow Taxi trip data from a paginated REST API
- Loads it into DuckDB
- Explores the data using SQL / Marimo / Ibis

---

# 🧰 Prerequisites

- Python 3.11+
- pip installed
- (Optional) uv

Check Python version:

```bash
python3 --version
```

---

# 1️⃣ Create Project Folder

```bash
mkdir taxi-pipeline
cd taxi-pipeline
```

Open this folder in VSCode (or your preferred IDE).

---

# 2️⃣ Install dlt Workspace

```bash
pip install "dlt[workspace]"
```

---

# 3️⃣ Initialize the dlt Project

Since this is a custom API (not scaffolded), run:

```bash
dlt init dlthub:taxi_pipeline duckdb
```

When prompted for IDE, choose:

```
codex
```

This creates:

- `.dlt/` configuration folder
- `taxi_pipeline_pipeline.py`
- `requirements.txt`
- `AGENT.md`

---

# 4️⃣ Build the Custom REST API Source

API Details:

| Property | Value |
|----------|--------|
| Base URL | https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api |
| Format | Paginated JSON |
| Page Size | 1000 records |
| Pagination | Stop when empty page returned |

Inside `taxi_pipeline_pipeline.py`:

- Create a `@dlt.source`
- Create a `@dlt.resource`
- Implement manual pagination
- Yield rows page by page

⚠️ Important:
Do NOT define a primary key unless it actually exists in the data.
Defining a non-existent primary key causes `UnboundColumnException`.

---

# 5️⃣ Run the Pipeline

```bash
python3 taxi_pipeline_pipeline.py
```

Expected behavior:

- Pages fetched sequentially
- ~10,000 rows extracted
- Normalize stage runs
- Load stage runs
- `taxi_pipeline.duckdb` file created

---

# 6️⃣ Verify Tables (Quick Check)

Create a verification script:

```bash
touch quick_check.py
```

Add:

```python
import duckdb

con = duckdb.connect("taxi_pipeline.duckdb")
print(con.execute("SHOW TABLES").fetchall())
```

Run:

```bash
python3 quick_check.py
```

Expected output:

```
('taxi_data', 'yellow_taxi_trips')
('taxi_data', '_dlt_loads')
('taxi_data', '_dlt_pipeline_state')
('taxi_data', '_dlt_version')
```

---

# 7️⃣ Optional: Use dlt Dashboard

```bash
dlt pipeline taxi_pipeline show
```

This opens a web dashboard to inspect:

- Pipeline runs
- Schemas
- Row counts
- Metadata

---

# 8️⃣ Set Up Marimo for Analysis

Create analysis folder:

```bash
mkdir marimo
cd marimo
marimo init analysis.py
```

Install analysis dependencies:

```bash
pip install marimo ibis-framework duckdb matplotlib pyarrow-hotfix
```

Run editor:

```bash
marimo edit analysis.py
```

---

# 9️⃣ Connect to DuckDB in Marimo

Since `analysis.py` is inside `/marimo`, connect using:

```python
import ibis

con = ibis.duckdb.connect("../taxi_pipeline.duckdb")
trips = con.table("taxi_data.yellow_taxi_trips")
```

Important: Use schema-qualified table name:

```
taxi_data.yellow_taxi_trips
```

---

# 🔟 Example Analysis: Dataset Date Range

```python
(
    trips
    .aggregate(
        start_date=lambda t: t.trip_pickup_date_time.min(),
        end_date=lambda t: t.trip_pickup_date_time.max()
    )
    .execute()
)
```

Expected result:

```
Start: 2009-06-01
End:   2009-06-30
```

---

# 🛠 Debugging Lessons Learned

During setup, the following issues were resolved:

1. Removed non-existent primary key (`trip_id`)
2. Learned dlt creates tables inside dataset schema (`taxi_data`)
3. Corrected column name:
   - Correct: `trip_pickup_date_time`
   - Not: `tpep_pickup_datetime`
4. Fixed relative path issue (`../taxi_pipeline.duckdb`)
5. Ensured ibis aggregations use the same relation

---

# 📂 Final Project Structure

```
taxi-pipeline/
│
├── .dlt/
├── taxi_pipeline_pipeline.py
├── quick_check.py
├── taxi_pipeline.duckdb
├── marimo/
│   └── analysis.py
└── requirements.txt
```

---

# ✅ Final Outcome

This project demonstrates:

- Custom paginated REST API ingestion
- Manual pagination handling
- dlt extract → normalize → load workflow
- DuckDB as analytical warehouse
- Ibis + Marimo analysis
- Schema debugging and validation

You now have a fully functional end-to-end data pipeline.