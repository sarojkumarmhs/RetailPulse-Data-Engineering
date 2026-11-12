-- Run against the Lakehouse SQL analytics endpoint.
-- Revenue by month (cancelled orders excluded)
SELECT
    YEAR(order_date) AS order_year,
    MONTH(order_date) AS order_month,
    SUM(CAST(gross_amount AS DECIMAL(18,2))) AS gross_revenue,
    COUNT(DISTINCT order_id) AS order_count
FROM gold.fact_order
WHERE order_status <> 'Cancelled'
GROUP BY YEAR(order_date), MONTH(order_date)
ORDER BY order_year, order_month;

-- Revenue by product category
SELECT p.category, SUM(CAST(f.gross_amount AS DECIMAL(18,2))) AS revenue
FROM gold.fact_order f
JOIN gold.dim_product p ON f.product_key = p.product_key
WHERE f.order_status <> 'Cancelled'
GROUP BY p.category
ORDER BY revenue DESC;

-- Current customer dimension
SELECT customer_id, customer_name, city, state, effective_from
FROM gold.dim_customer
WHERE is_current = 1;
