import duckdb

con = duckdb.connect("taxi_pipeline.duckdb")

print(
    con.execute("""
        SELECT 
            MIN(trip_pickup_date_time) AS start_date,
            MAX(trip_pickup_date_time) AS end_date
        FROM taxi_data.yellow_taxi_trips
    """).fetchdf()
)