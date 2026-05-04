# DuckDB & Data Warehouse Instructions

**Purpose**: Standardize access to `overseas_data.duckdb` and other data sources to prevent errors and ensured data integrity.

## 1. Mandatory Data Map

**BEFORE** accessing any data, you **MUST** consult:
`Officer/00_Data_Warehouse/DATA_SOURCES_MAP.md`

This file contains:

- Locations of all databases and parquet files.
- Links to the correct schema definitions.
- Status of data sources (e.g., "Golden Record", "Raw").

## 2. Schema Location

All schema definitions are centralized in:
`Officer/00_Data_Warehouse/schemas/`

- **`overseas_dictionary.json`**: Mappings for `overseas_data.duckdb` (Chinese -> English column names).
- **`product_features_schema.json`**: Schema for `product_features.parquet`.

## 3. Connection Rules (Python)

When connecting to DuckDB via Python, you **MUST** use `read_only=True` to prevent locking the database for other users/processes.

```python
import duckdb
con = duckdb.connect("path/to/overseas_data.duckdb", read_only=True)
```

## 4. Querying via MCP

Use the `mcp:duckdb` tool for SQL queries.

- **Tool**: `mcp_duckdb_query_sql`
- **Database**: `overseas_data.duckdb` (attach explicitly if needed)

## 5. Column Name Handling (CRITICAL)

The `overseas_data.duckdb` contains columns with **newlines** and **special characters** (e.g., `中文全称 \nProduct name`).

**DO NOT** try to guess the exact string representation in SQL. It often fails due to encoding/escaping issues.

**Recommended Strategy:**
Use **DuckDB's Regex Column Selection** or **Index Access** to safely select columns without typing their full, messy names.

```sql
-- Select by Regex matches
SELECT
    COLUMNS('.*Product name.*') AS Product_Name,
    COLUMNS('.*Model.*') AS Model,
    COLUMNS('.*Quantity.*') AS Qty
FROM current_state
WHERE COLUMNS('.*Model.*') ILIKE '%BP1%';
```

**Python Fallback:**
If SQL fails, load the table into **Pandas** and filter there.

```python
# Python approach is more robust for column names
df = con.execute("SELECT * FROM current_state").fetchdf()
# Filter columns by partial string match
cols = [c for c in df.columns if "Product name" in c]
```
