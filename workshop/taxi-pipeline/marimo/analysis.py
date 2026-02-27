import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import ibis
    import matplotlib.pyplot as plt

    return ibis, plt


@app.cell
def _(ibis):
    con = ibis.duckdb.connect("../taxi_pipeline.duckdb")
    trips = con.table("yellow_taxi_trips", database="taxi_data")
    trips
    return (trips,)


@app.cell
def _(trips):
    kpis = (
        trips
        .aggregate(
            total_trips=trips.count(),
            earliest_pickup=trips.trip_pickup_date_time.min(),
            latest_pickup=trips.trip_pickup_date_time.max(),
            max_fare=trips.fare_amt.max(),
            avg_fare=trips.fare_amt.mean(),
            avg_distance=trips.trip_distance.mean()
        )
    )

    kpis.execute()
    return


@app.cell
def _(plt, trips):
    passenger_dist = (
        trips
        .group_by(trips.passenger_count)
        .aggregate(count=trips.count())
        .order_by(lambda t: t.passenger_count)
    )

    df_pass = passenger_dist.execute()

    plt.figure()
    plt.bar(df_pass["passenger_count"], df_pass["count"])
    plt.xlabel("Passenger Count")
    plt.ylabel("Number of Trips")
    plt.title("Trips by Passenger Count")
    plt.show()
    return


@app.cell
def _(plt, trips):
    df_fare = (
        trips
        .filter(trips.fare_amt < 200)
        .select(trips.fare_amt)
        .execute()
    )

    plt.figure()
    plt.hist(df_fare["fare_amt"], bins=50)
    plt.xlabel("Fare Amount")
    plt.ylabel("Frequency")
    plt.title("Fare Distribution (Filtered < $200)")
    plt.show()
    return


@app.cell
def _(trips):
    (
        trips
        .aggregate(
            start_date=lambda t: t.trip_pickup_date_time.min(),
            end_date=lambda t: t.trip_pickup_date_time.max()
        )
        .execute()
    )
    return


if __name__ == "__main__":
    app.run()
