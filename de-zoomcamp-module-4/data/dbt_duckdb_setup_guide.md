# dbt + DuckDB Local Setup Guide (MacBook) --- Complete Setup, Issues & Fixes

This guide documents the complete setup process for running **dbt with
DuckDB locally**, including all issues faced, root causes, and final
solutions.

------------------------------------------------------------------------

# System Configuration

  Component                Value
  ------------------------ -----------------------
  Machine                  MacBook Air
  RAM                      16 GB
  OS                       macOS
  Initial Python Version   3.14 ❌ (unsupported)
  Final Python Version     3.12 ✅
  dbt version              1.11.5
  Adapter                  dbt-duckdb 1.10.0
  Database                 DuckDB

------------------------------------------------------------------------
# Initial Setup

- Run ingest_data.py file so that it download all the green and yellow data.

# Issue 1: dbt crashing with Python 3.14

## Error

mashumaro.exceptions.UnserializableField error

## Root Cause

dbt does NOT support Python 3.14 yet.

## Solution

Install Python 3.12:

``` bash
brew install python@3.12
```

Create virtual environment:

``` bash
python3.12 -m venv dbt-env
source dbt-env/bin/activate
```

Install dbt:

``` bash
pip install dbt-duckdb
```

------------------------------------------------------------------------

# Issue 2: dbt using system Python instead of virtual environment

Check:

``` bash
which dbt
```

Fix:

``` bash
hash -r
```

------------------------------------------------------------------------

# Issue 3: Missing dbt packages

Error:

dbt found 2 package(s) specified but 0 installed

Fix:

``` bash
dbt deps
```

------------------------------------------------------------------------

# Issue 4: DuckDB Out of Memory Error

Error:

Out of Memory Error

## Root Cause

dbt was rebuilding data in dev schema instead of using existing prod
schema.

## Fix

Run:

``` bash
dbt build --target prod
```

------------------------------------------------------------------------

# Recommended profiles.yml

``` yaml
taxi_rides_ny:
  target: prod
  outputs:
    dev:
      type: duckdb
      path: taxi_rides_ny.duckdb
      schema: dev
      threads: 1
      extensions:
        - parquet
      settings:
        memory_limit: '8GB'
        preserve_insertion_order: false

    prod:
      type: duckdb
      path: taxi_rides_ny.duckdb
      schema: prod
      threads: 1
      extensions:
        - parquet
      settings:
        memory_limit: '8GB'
        preserve_insertion_order: false
```

------------------------------------------------------------------------

# Final Working Commands

Activate environment:

``` bash
source dbt-env/bin/activate
```

Install deps:

``` bash
dbt deps
```

Verify:

``` bash
dbt debug
```

Build:

``` bash
dbt build --target prod
```

------------------------------------------------------------------------

# Conclusion

After fixing:

-   Python compatibility issue
-   Virtual environment setup
-   dbt dependency installation
-   dbt target configuration

dbt ran successfully and built all models.

Your local dbt + DuckDB setup is now fully functional.
