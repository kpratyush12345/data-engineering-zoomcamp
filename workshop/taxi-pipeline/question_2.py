import duckdb

con = duckdb.connect("taxi_pipeline.duckdb")

print(
    con.execute("""
        SELECT 
            100.0 * SUM(CASE WHEN payment_type = 'Credit' THEN 1 ELSE 0 END)
            / COUNT(*) AS credit_card_percentage
        FROM taxi_data.yellow_taxi_trips
    """).fetchdf()
)