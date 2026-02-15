import duckdb
import requests
from pathlib import Path

BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download"

def download_and_convert_fhv():
    taxi_type = "fhv"
    year = 2019

    data_dir = Path("data") / taxi_type
    data_dir.mkdir(exist_ok=True, parents=True)

    for month in range(1, 13):

        parquet_filename = f"{taxi_type}_tripdata_{year}-{month:02d}.parquet"
        parquet_filepath = data_dir / parquet_filename

        if parquet_filepath.exists():
            print(f"Skipping {parquet_filename} (already exists)")
            continue

        csv_gz_filename = f"{taxi_type}_tripdata_{year}-{month:02d}.csv.gz"
        csv_gz_filepath = data_dir / csv_gz_filename

        url = f"{BASE_URL}/{taxi_type}/{csv_gz_filename}"

        print(f"Downloading {url}")

        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(csv_gz_filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Converting {csv_gz_filename} → parquet")

        con = duckdb.connect()

        con.execute(f"""
            COPY (
                SELECT *
                FROM read_csv_auto('{csv_gz_filepath}')
            )
            TO '{parquet_filepath}'
            (FORMAT PARQUET)
        """)

        con.close()

        csv_gz_filepath.unlink()

        print(f"Completed {parquet_filename}")


def load_into_duckdb():
    con = duckdb.connect("taxi_rides_ny.duckdb")

    con.execute("CREATE SCHEMA IF NOT EXISTS prod")

    con.execute("""
        CREATE OR REPLACE TABLE prod.fhv_tripdata AS
        SELECT *
        FROM read_parquet('data/fhv/*.parquet', union_by_name=true)
    """)

    con.close()

    print("Loaded FHV data into DuckDB")


def update_gitignore():
    gitignore_path = Path(".gitignore")

    content = gitignore_path.read_text() if gitignore_path.exists() else ""

    if "data/" not in content:
        with open(gitignore_path, "a") as f:
            f.write("\n# Data directory\ndata/\n")

        print("Added data/ to .gitignore")


if __name__ == "__main__":

    update_gitignore()

    download_and_convert_fhv()

    load_into_duckdb()

    print("FHV ingestion complete")