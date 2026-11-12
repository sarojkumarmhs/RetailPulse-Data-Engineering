# Architecture and design

## Layers
- **Landing**: CSV files in OneLake `Files/source/`, organized by entity and batch.
- **Bronze**: raw-ish Delta tables with ingestion timestamp and source file lineage.
- **Silver**: typed, deduplicated and conformed Delta tables.
- **Gold**: SCD Type 2 customer dimension, product dimension and order-line fact.
- **Audit**: repeatable quality-check results.

## SCD Type 2
`03_customer_scd_type2` loads batch 1 as the initial dimension, compares batch 2 using a SHA-256 hash of tracked attributes, expires changed current records, and inserts changed/new versions. `effective_from`, `effective_to`, and `is_current` track validity.

## Incremental extension
For production, replace the fixed batch paths with a pipeline parameter (batch folder/date), persist a processed-file manifest, and use watermarking or CDC. Add late-arriving dimension handling and idempotent merge keys before production use.

## Operational considerations
Use workspace Git integration, deployment pipelines, pipeline retries, alerting, capacity monitoring, and least-privilege workspace roles. Keep secrets out of notebooks and source control.
