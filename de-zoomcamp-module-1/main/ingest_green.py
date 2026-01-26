import pandas as pd
from sqlalchemy import create_engine

# Parquet file
PARQUET_FILE = "data/green_tripdata_2025-11.parquet"
CSV_ZONES = "data/taxi_zone_lookup.csv"

# Postgres connection (from docker-compose)
USER = "postgres"
PASSWORD = "postgres"
HOST = "localhost"   # host machine
PORT = "5433"        # mapped port
DB = "ny_taxi"

engine = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")

print("Reading parquet...")
df = pd.read_parquet(PARQUET_FILE)
print("Rows:", len(df))

print("Writing green_trips table...")
df.to_sql("green_trips", engine, if_exists="replace", index=False)
print("Loaded green_trips")

print("Reading zones csv...")
zones = pd.read_csv(CSV_ZONES)
print("Writing zones table...")
zones.to_sql("zones", engine, if_exists="replace", index=False)
print("Loaded zones")