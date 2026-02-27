import dlt

pipeline = dlt.pipeline(
    pipeline_name="open_library_pipeline",
    destination="duckdb",
    dataset_name="open_library_data",
)

ds = pipeline.dataset()

print(ds.tables)
print(ds.books.df().head())