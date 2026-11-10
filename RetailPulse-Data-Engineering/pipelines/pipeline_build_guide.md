# Fabric Data Pipeline orchestration

Create a Fabric Data Pipeline named `pl_retailpulse_daily`.

## Activities and dependencies

1. Notebook activity: `00_setup_and_config` (optional for routine runs; use once initially).
2. Notebook activity: `01_bronze_ingestion`.
3. Notebook activity: `02_silver_transformations` — depends on Bronze success.
4. Notebook activity: `03_customer_scd_type2` — depends on Silver success.
5. Notebook activity: `04_gold_model` — depends on SCD success.
6. Notebook activity: `05_data_quality_and_audit` — depends on Gold success.

For a production pipeline, configure notebook activity retries, timeout, and failure notifications according to operational requirements. Do not run the SCD simulation notebook repeatedly against the same history table without resetting the demo state or replacing the simulated change with a real source change feed.

## Suggested parameters for a future incremental version
- `p_source_folder`
- `p_load_date`
- `p_load_type` (`FULL` / `INCREMENTAL`)
- `p_pipeline_run_id`

The supplied notebooks are a reproducible full-load portfolio implementation, not a fully parameterised enterprise ingestion framework.
