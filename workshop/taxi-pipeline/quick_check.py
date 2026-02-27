import duckdb

con = duckdb.connect("taxi_pipeline.duckdb")

# Count rows
print(
    con.execute("""
        SELECT COUNT(*) 
        FROM taxi_data.yellow_taxi_trips
    """).fetchall()
)
