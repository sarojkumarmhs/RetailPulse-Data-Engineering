-- Run these in the Lakehouse SQL analytics endpoint after Gold tables sync.
-- Revenue definition: item price + freight value. Adjust business definition if needed.

-- 1. Monthly revenue and order volume
SELECT
    YEAR(order_purchase_timestamp) AS order_year,
    MONTH(order_purchase_timestamp) AS order_month,
    COUNT(DISTINCT order_id) AS order_count,
    SUM(item_price + freight_value) AS gross_item_revenue
FROM gold.fact_order_item
GROUP BY YEAR(order_purchase_timestamp), MONTH(order_purchase_timestamp)
ORDER BY order_year, order_month;

-- 2. Revenue by product category
SELECT
    p.product_category_name,
    SUM(f.item_price + f.freight_value) AS gross_item_revenue,
    COUNT(DISTINCT f.order_id) AS order_count
FROM gold.fact_order_item f
LEFT JOIN gold.dim_product p ON f.product_key = p.product_key
GROUP BY p.product_category_name
ORDER BY gross_item_revenue DESC;

-- 3. Order and revenue by customer state
SELECT
    c.customer_state,
    COUNT(DISTINCT f.order_id) AS order_count,
    SUM(f.item_price + f.freight_value) AS gross_item_revenue
FROM gold.fact_order_item f
LEFT JOIN gold.dim_customer c ON f.customer_key = c.customer_key
GROUP BY c.customer_state
ORDER BY gross_item_revenue DESC;

-- 4. Average delivery time in days (delivered orders only)
SELECT
    AVG(CAST(DATEDIFF(hour, order_purchase_timestamp, order_delivered_customer_date) AS FLOAT) / 24.0)
        AS avg_delivery_days
FROM gold.fact_order_item
WHERE order_delivered_customer_date IS NOT NULL;

-- 5. Payment type mix
SELECT
    payment_type,
    COUNT(*) AS payment_rows,
    SUM(payment_value) AS total_payment_value
FROM gold.fact_order_payment
GROUP BY payment_type
ORDER BY total_payment_value DESC;
