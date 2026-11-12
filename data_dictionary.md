# Data dictionary

| Entity | Important fields | Meaning |
|---|---|---|
| customers | customer_id, customer_name, city, state, updated_at | Customer snapshot; batch 2 includes changes |
| orders | order_id, customer_id, order_date, order_status | Order header |
| order_items | order_id, product_id, quantity, unit_price | Order line and unit price |
| products | product_id, product_name, category | Product lookup |
| dim_customer | effective_from, effective_to, is_current, attribute_hash | SCD Type 2 customer history |
| fact_order | order_id, customer_key, product_key, gross_amount | Gold order-line fact |
| dq_results | check_name, failed_count, status, checked_at | Data quality audit log |

All source data is synthetic and created for this demonstration.
