import marimo

__generated_with = "0.20.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import ibis
    import matplotlib.pyplot as plt

    return ibis, mo, plt


@app.cell
def _(mo):
    mo.md("""
    ## 📚 Top 10 Authors by Book Count
    """)
    return


@app.cell
def _():
    import duckdb

    con_raw = duckdb.connect("../open_library_pipeline.duckdb")

    print("Schemas:")
    print(
        con_raw.execute(
            "SELECT schema_name FROM information_schema.schemata"
        ).fetchall()
    )

    print("\nTables:")
    print(
        con_raw.execute(
            "SELECT table_schema, table_name FROM information_schema.tables"
        ).fetchall()
    )
    return


@app.cell
def _(ibis, query):
    con = ibis.duckdb.connect("../open_library_pipeline.duckdb")
    books = con.table("books", database="open_library_data")
    authors = con.table("books__author_name", database="open_library_data")

    # Filter by title matching search input
    filtered_books = books.filter(
        books.title.ilike(f"%{query.value}%")
    )

    authors_joined = authors.join(
        filtered_books,
        authors._dlt_parent_id == filtered_books._dlt_id
    )

    authors_joined
    return (authors_joined,)


@app.cell
def _(authors_joined):
    top_authors = (
        authors_joined
        .group_by(author=authors_joined.value)
        .aggregate(book_count=authors_joined.count())
        .order_by(lambda t: t.book_count.desc())
        .limit(10)
    )

    df = top_authors.execute()
    df
    return (df,)


@app.cell
def _(df, plt):
    plt.figure()
    plt.barh(df["author"], df["book_count"])
    plt.xlabel("Book Count")
    plt.ylabel("Author")
    plt.title("Top 10 Authors (Filtered by Title)")
    plt.gca().invert_yaxis()
    plt.show()
    return


@app.cell
def _(mo):
    query = mo.ui.text(value="harry potter", label="Search Term")
    query
    return (query,)


if __name__ == "__main__":
    app.run()
