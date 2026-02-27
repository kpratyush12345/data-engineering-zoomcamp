import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import ibis
    import os

    print("Current directory:", os.getcwd())

    con = ibis.duckdb.connect("../taxi_pipeline.duckdb")

    print("Tables:", con.raw_sql("SHOW TABLES").fetchall())

    trips = con.table("yellow_taxi_trips", database="taxi_data")

    trips
    return mo, trips


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    📘 Question 1

    What is the start date and end date of the dataset?
    """)
    return


@app.cell
def _(trips):
    date_range = trips.aggregate(
        start_date=trips.trip_pickup_date_time.min(),
        end_date=trips.trip_pickup_date_time.max()
    )

    date_range.execute()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    📘 Question 2

    What proportion of trips are paid with credit card?
    """)
    return


@app.cell
def _(trips):
    credit_percentage = trips.aggregate(
        credit_percentage=(
            (trips.payment_type == "Credit").sum() * 100.0
            / trips.count()
        )
    )

    credit_percentage.execute()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    📘 Question 3

    What is the total amount of money generated in tips?
    """)
    return


@app.cell
def _(trips):
    total_tips = trips.tip_amt.sum()

    total_tips.execute()
    return


if __name__ == "__main__":
    app.run()
