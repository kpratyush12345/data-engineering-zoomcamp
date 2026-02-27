# From APIs to Warehouses: AI-Assisted Data Ingestion with dlt

This project demonstrates how to build a complete ELT pipeline using:

- **dlt** for ingestion and normalization
- **DuckDB** as a local data warehouse
- **Ibis** for query abstraction
- **marimo** for reactive visualization

We extract data from the **Open Library API**, normalize nested JSON into relational tables, store it in DuckDB, and build an interactive dashboard.

---

# 🚀 Project Architecture

```
Open Library API
        ↓
dlt Extract
        ↓
dlt Normalize (child tables)
        ↓
DuckDB (local warehouse)
        ↓
Ibis (query abstraction)
        ↓
marimo (reactive UI)
        ↓
Matplotlib (visualization)
```

---

# 📦 1️⃣ Prerequisites

- Python 3.11+
- pip (or uv)
- VS Code (or any editor)

Check Python version:

```bash
python --version
```

---

# 📁 2️⃣ Create Project Folder

```bash
mkdir my-dlt-pipeline
cd my-dlt-pipeline
```

---

# 📦 3️⃣ Install Dependencies

## Install dlt workspace

```bash
pip install "dlt[workspace]"
```

## Install analytics & visualization stack

```bash
pip install marimo ibis-framework[duckdb] pyarrow matplotlib duckdb
```

> Installing `pyarrow` prevents the `pyarrow_hotfix` error.

---

# ⚙️ 4️⃣ Initialize dlt Project

```bash
dlt init dlthub:open_library duckdb
```

When prompted for IDE:

```
Press Enter to accept default, or type a name:
```

Type:

```
codex
```

This creates:

```
.dlt/
open_library_pipeline.py
open_library-docs.yaml
requirements.txt
```

---

# 📝 5️⃣ Configure `open_library_pipeline.py`

Replace contents with:

```python
import dlt
from dlt.sources.rest_api import rest_api_resources
from dlt.sources.rest_api.typing import RESTAPIConfig

@dlt.source
def open_library_rest_api_source():

    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://openlibrary.org",
        },
        "resources": [
            {
                "name": "books",
                "endpoint": {
                    "path": "search.json",
                    "params": {
                        "q": "harry potter",
                        "limit": 100,
                    },
                    "data_selector": "docs",
                },
            }
        ],
        "resource_defaults": {
            "primary_key": "key",
            "write_disposition": "replace",
        },
    }

    yield from rest_api_resources(config)


pipeline = dlt.pipeline(
    pipeline_name="open_library_pipeline",
    destination="duckdb",
    dataset_name="open_library_data",
    refresh="drop_sources",
    progress="log",
)

if __name__ == "__main__":
    load_info = pipeline.run(open_library_rest_api_source())
    print(load_info)
```

---

# ▶️ 6️⃣ Run the Pipeline

From project root:

```bash
python open_library_pipeline.py
```

This creates:

```
open_library_pipeline.duckdb
```

---

# 🔎 7️⃣ Verify Tables in DuckDB (Optional)

```python
import duckdb

con = duckdb.connect("open_library_pipeline.duckdb")

print(
    con.execute(
        "SELECT table_schema, table_name FROM information_schema.tables"
    ).fetchall()
)
```

Expected schema:

```
('open_library_data', 'books')
('open_library_data', 'books__author_name')
...
```

---

# 📊 8️⃣ Setup marimo Visualization

## Create marimo folder

```bash
mkdir marimo
cd marimo
```

## Create notebook

```bash
marimo edit analysis.py
```

---

# ⚠️ Important: Database Path

Because `analysis.py` is inside `/marimo/`
and the `.duckdb` file is one level above:

Use:

```python
con = ibis.duckdb.connect("../open_library_pipeline.duckdb")
```

NOT:

```python
con = ibis.duckdb.connect("open_library_pipeline.duckdb")
```

---

# 📘 marimo Notebook Structure

## 1️⃣ Imports

```python
import marimo as mo
import ibis
import matplotlib.pyplot as plt
```

---

## 2️⃣ Connect to DuckDB

```python
con = ibis.duckdb.connect("../open_library_pipeline.duckdb")

books = con.table("books", database="open_library_data")
authors = con.table("books__author_name", database="open_library_data")
```

---

## 3️⃣ UI Input

```python
query = mo.ui.text(value="harry potter", label="Search Term")
query
```

---

## 4️⃣ Filter + Join

```python
filtered_books = books.filter(
    books.title.ilike(f"%{query.value}%")
)

authors_joined = authors.join(
    filtered_books,
    authors._dlt_parent_id == filtered_books._dlt_id
)

authors_joined
```

---

## 5️⃣ Aggregation

> Note: Author column is named `value` (not `author_name`).

```python
top_authors = (
    authors_joined
    .group_by(author=authors_joined.value)
    .aggregate(book_count=authors_joined.count())
    .order_by(lambda t: t.book_count.desc())
    .limit(10)
)

df = top_authors.execute()
df
```

---

## 6️⃣ Plot

```python
plt.figure()
plt.barh(df["author"], df["book_count"])
plt.xlabel("Book Count")
plt.ylabel("Author")
plt.title(f"Top 10 Authors for: {query.value}")
plt.gca().invert_yaxis()
plt.show()
```

Changing the text input updates the chart reactively.

---

# ⚠️ Common Issues & Fixes

### ❌ TableNotFound
Cause:
Wrong DB path or schema.

Fix:
```
"../open_library_pipeline.duckdb"
database="open_library_data"
```

---

### ❌ KeyError: 'author_name'
Cause:
dlt child table column is `value`.

Fix:
```
authors_joined.value
```

---

### ❌ ModuleNotFoundError: pyarrow_hotfix
Fix:

```bash
pip install pyarrow
```

---

### ❌ Marimo variable redefinition error
Cause:
Same variable defined in multiple cells.

Fix:
Define connection once and reuse it.

---

# ✅ Final Outcome

You now have:

- A working ELT pipeline
- Normalized relational schema
- Local analytics warehouse
- Reactive dashboard
- AI-assisted debugging workflow

This completes the workshop setup successfully.