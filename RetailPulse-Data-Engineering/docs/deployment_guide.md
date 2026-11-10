# Microsoft Fabric deployment guide

## Prerequisites
- A Microsoft Fabric workspace backed by an eligible capacity or trial.
- Permission to create a Lakehouse, notebooks, and Data Pipelines.
- The public Olist CSV dataset downloaded locally.

## Create the Lakehouse
1. In your Fabric workspace, select **New > Lakehouse**.
2. Name it `lh_retailpulse`.
3. Open the Lakehouse Explorer.
4. Under Files, create `source/olist` and `rejects`.
5. Upload the source CSV files to `Files/source/olist/`.

## Create notebooks
For each `.ipynb` file in `notebooks/`:
1. Create a new Fabric Notebook.
2. Import the notebook file if notebook import is available in your tenant, or copy its cells into a new notebook.
3. Attach the notebook to `lh_retailpulse` as its default Lakehouse.
4. Run the notebooks in numeric order.
5. Review output and confirm tables exist in the Lakehouse Tables area.

The notebooks rely on the default Lakehouse attachment and Spark's `saveAsTable` / `spark.table` APIs.

## Notebook execution order
- `00_setup_and_config`
- `01_bronze_ingestion`
- `02_silver_transformations`
- `03_customer_scd_type2`
- `04_gold_model`
- `05_data_quality_and_audit`

## Build a Fabric Data Pipeline
Follow `pipelines/pipeline_build_guide.md`. Create notebook activities in order and configure success dependencies.

## SQL analytics endpoint
After Gold Delta tables are created, open the Lakehouse SQL analytics endpoint. Run the statements in `sql/gold_business_queries.sql`. Fabric may take a short time to synchronise newly created Delta tables to the SQL endpoint.

## Power BI
Create a report from the Lakehouse SQL analytics endpoint or directly from the Lakehouse. Suggested pages:
- Executive overview: revenue, orders, average order value.
- Delivery: average delivery days, late delivery rate.
- Product: revenue by category and top products.
- Geography: orders and revenue by state.
- Payments: payment type mix.

## Troubleshooting
- `PATH_NOT_FOUND`: check that the CSV files were uploaded under the exact folder and filenames.
- `TABLE_OR_VIEW_NOT_FOUND`: run the upstream notebook and verify the Lakehouse attachment.
- SQL endpoint missing a table: refresh the endpoint metadata and confirm the Delta table was created successfully.
- Permission/capacity errors: confirm workspace role and capacity availability.
