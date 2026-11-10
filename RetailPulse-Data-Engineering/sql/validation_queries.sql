-- Basic validation checks after Gold model creation.

-- Fact grain: should return no rows
SELECT order_id, order_item_id, COUNT(*) AS row_count
FROM gold.fact_order_item
GROUP BY order_id, order_item_id
HAVING COUNT(*) > 1;

-- Customer dimension key uniqueness: should return no rows
SELECT customer_key, COUNT(*) AS row_count
FROM gold.dim_customer
GROUP BY customer_key
HAVING COUNT(*) > 1;

-- Referential integrity: should return zero
SELECT COUNT(*) AS orphan_customer_rows
FROM gold.fact_order_item f
LEFT JOIN gold.dim_customer c ON f.customer_key = c.customer_key
WHERE f.customer_key IS NOT NULL AND c.customer_key IS NULL;

-- Check current customer history rows: should return no rows
SELECT customer_id, COUNT(*) AS current_versions
FROM silver.customer_history
WHERE is_current = true
GROUP BY customer_id
HAVING COUNT(*) > 1;
