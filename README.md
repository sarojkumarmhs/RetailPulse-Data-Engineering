# RetailPulse — Microsoft Fabric Lakehouse Project

A self-contained, portfolio-ready **Microsoft Fabric** data engineering project. It demonstrates a Bronze → Silver → Gold lakehouse, incremental ingestion, Delta Lake, SCD Type 1 and Type 2, data quality checks, and business SQL.

> **Data included:** small synthetic CSV datasets are included under `sample_data/`. Batch 2 deliberately changes customer locations and adds a new customer so the SCD Type 2 notebook has a repeatable change to process. The data is synthetic, not real customer data.

## Architecture

`sample_data (CSV) → OneLake Files → Bronze Delta → Silver Delta → Gold Delta → SQL analytics endpoint / Power BI`

## Requirements

- A Microsoft Fabric workspace with a Lakehouse.
- Fabric notebook runtime with PySpark and Delta Lake (standard Fabric Spark runtime).
- Permission to create tables and upload files to the Lakehouse.

## Quick start in Fabric

1. Create a workspace and a Lakehouse named **`RetailPulseLH`**.
2. In the Lakehouse, upload the contents of `sample_data/` into its `Files` area, preserving folders. The expected paths are:
   - `Files/source/customers/batch_1/customers.csv`
   - `Files/source/customers/batch_2/customers.csv`
   - `Files/source/orders/batch_1/orders.csv`
   - `Files/source/order_items/batch_1/order_items.csv`
   - `Files/source/products/products.csv`
3. Create/import the notebooks in `notebooks/` in the listed order. Attach each notebook to `RetailPulseLH` as its default Lakehouse.
4. Run:
   - `00_setup`
   - `01_bronze_ingestion`
   - `02_silver_transformations`
   - `03_customer_scd_type2`
   - `04_gold_model`
   - `05_data_quality`
5. In the Lakehouse SQL analytics endpoint, run `sql/gold_business_queries.sql`.

## Notebook import note

The `.py` files are Fabric notebook cell source exports: create a new Fabric notebook, attach `RetailPulseLH`, then copy each file's cells into the notebook in order. They are plain Python/PySpark and intentionally avoid non-Fabric services. Alternatively, use the accompanying `.ipynb` files if your workspace supports notebook upload/import.

## Expected outputs

Tables (in the Lakehouse schemas shown below):
- Bronze: `bronze_customers_batch1`, `bronze_customers_batch2`, `bronze_orders`, `bronze_order_items`, `bronze_products`
- Silver: `silver_customers`, `silver_orders`, `silver_order_items`, `silver_products`
- Dimension/fact: `dim_customer`, `dim_product`, `fact_order`
- Quality: `dq_results`

The SCD2 demo creates a new current version when a tracked customer attribute changes. For example, C001 changes from Bengaluru to Mysuru and C003 from Aizawl to Guwahati.

## Important honesty note

This repository contains complete code and data, plus expected design/validation logic. It has **not** been executed inside your private Fabric tenant; you must run the notebooks in your workspace to validate tenant permissions and runtime behavior. Do not describe it on LinkedIn as Fabric-executed until you have run it there.

## Repository structure

- `sample_data/` — all source CSVs required for the demo
- `notebooks/` — six ordered Fabric PySpark notebook scripts and `.ipynb` versions
- `sql/` — business queries and validation queries
- `docs/` — architecture, data dictionary, deployment and interview walkthrough
