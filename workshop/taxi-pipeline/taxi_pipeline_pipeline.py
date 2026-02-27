import requests
import dlt


BASE_URL = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"


@dlt.source
def nyc_taxi_source():

    @dlt.resource(
        name="yellow_taxi_trips",
        write_disposition="replace",
    )
    def taxi_data():

        page = 1

        while True:
            print(f"Fetching page {page}...")

            response = requests.get(
                BASE_URL,
                params={"page": page}
            )

            response.raise_for_status()
            data = response.json()

            # Stop when empty page returned
            if not data:
                print("No more data. Stopping pagination.")
                break

            yield data

            page += 1

    return taxi_data


pipeline = dlt.pipeline(
    pipeline_name="taxi_pipeline",
    destination="duckdb",
    dataset_name="taxi_data",
    progress="log",
)


if __name__ == "__main__":
    load_info = pipeline.run(nyc_taxi_source())
    print(load_info)