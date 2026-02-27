import duckdb

con = duckdb.connect("taxi_pipeline.duckdb")

print(
    con.execute("""
        SELECT ROUND(SUM(tip_amt), 2) AS total_tips
        FROM taxi_data.yellow_taxi_trips
    """).fetchdf()
)