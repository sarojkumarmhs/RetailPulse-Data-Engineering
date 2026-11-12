-- SCD2: exactly one current row per customer
SELECT customer_id, SUM(CASE WHEN is_current = 1 THEN 1 ELSE 0 END) AS current_versions
FROM gold.dim_customer
GROUP BY customer_id
HAVING SUM(CASE WHEN is_current = 1 THEN 1 ELSE 0 END) <> 1;

-- No invalid order line values
SELECT COUNT(*) AS invalid_lines
FROM gold.fact_order
WHERE quantity <= 0 OR unit_price < 0 OR gross_amount < 0;

-- Orphan fact keys
SELECT COUNT(*) AS orphan_customer_keys
FROM gold.fact_order
WHERE customer_key IS NULL;
