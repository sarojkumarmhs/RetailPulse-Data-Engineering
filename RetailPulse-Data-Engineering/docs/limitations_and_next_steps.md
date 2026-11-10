# Limitations and next steps

This is a portfolio implementation intended to be deployed and validated in a Fabric workspace.

## Current scope
- CSV batch ingestion from OneLake Files.
- Bronze/Silver/Gold Delta tables.
- SCD Type 2 demonstration for customer attributes.
- Star-schema facts and dimensions.
- Basic DQ and audit outputs.
- SQL KPI and validation queries.

## Not yet implemented
- Automated file-arrival detection and manifest.
- Incremental watermark-based ingestion.
- Schema evolution policy and quarantine routing for malformed files.
- Production alerting / notifications.
- CI/CD deployment pipelines and environment promotion.
- Row-level security and semantic model deployment.
- Measured performance tuning at scale.

## Before claiming production readiness
Run the solution in Fabric, capture actual row counts and run times, test a rerun, verify SCD history, validate Gold metrics, and add screenshots. Describe it as a portfolio project until these checks have been completed.
