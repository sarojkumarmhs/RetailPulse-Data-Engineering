# Architecture and design decisions

## Medallion layers

### Bronze
Stores source-shaped Delta tables. Adds `source_file_name` and `ingested_at`. The notebook reads the CSVs from OneLake Files and writes Delta tables.

### Silver
Applies trimming, explicit casts, deduplication, timestamp parsing, and basic standardisation. Silver is the conformed layer used by downstream modelling.

### Gold
Publishes a dimensional model for analytics: dimensions and facts with documented grain.

## SCD Type 2 design

`silver.customer_history` stores:
- `customer_id` — natural/business key
- tracked attributes: `customer_unique_id`, `customer_zip_code_prefix`, `customer_city`, `customer_state`
- `effective_start_ts`, `effective_end_ts`
- `is_current`
- `record_hash`

When tracked attributes change:
1. Expire the current version by setting `is_current = false` and `effective_end_ts` to the incoming effective timestamp.
2. Insert the new version with `is_current = true` and an open-ended end timestamp.

The notebook includes a small deterministic change simulation because the public dataset is a snapshot rather than a true customer CDC source.

## Idempotency and reruns

Bronze is intentionally loaded as a snapshot using overwrite. Silver transformations overwrite their target tables. This makes the initial portfolio run repeatable. The SCD notebook uses a stable test effective timestamp and should be reset/re-run according to its documented simulation cell. For real incremental production workloads, use file manifests, source watermarks, deduplication keys, and Delta MERGE.

## Operational metadata

`ops.audit_run` and `ops.dq_results` provide basic run and quality observability. A production implementation should also persist pipeline run IDs, activity IDs, source file counts, row counts, durations, and error details.

## Security

Use Fabric workspace roles and item permissions. Never commit tenant IDs, workspace IDs, access tokens, connection strings, personal data, or employer data to GitHub.
