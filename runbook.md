# Runbook

1. Confirm the default Lakehouse is attached to every notebook.
2. Confirm source files exist at the exact `Files/source/...` paths in README.
3. Run notebooks in numeric order.
4. If a table already exists, rerun is supported for the demo because Bronze/Silver/Gold outputs are overwritten. The SCD2 notebook resets its dimension from batch 1 each run, so results are deterministic.
5. Review `audit.dq_results` and execute SQL validation queries.
6. For Power BI, create a semantic model from `gold.fact_order`, `gold.dim_product`, and `gold.dim_customer`.

Troubleshooting:
- `Path does not exist`: upload folders preserving the exact structure.
- `SCHEMA_NOT_FOUND`: run `00_setup` first.
- Table not found: run notebooks in order and verify the default Lakehouse attachment.
- SQL endpoint not updated yet: allow the Lakehouse SQL analytics endpoint to synchronize after Spark writes.
