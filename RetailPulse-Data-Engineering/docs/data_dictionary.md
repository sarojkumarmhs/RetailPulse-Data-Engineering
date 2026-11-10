# Dataset and data dictionary

## Source files

Upload the extracted Olist CSV files to `Files/source/olist/`.

| Source file | Bronze table | Main business grain |
|---|---|---|
| `olist_orders_dataset.csv` | `bronze.orders` | One row per order |
| `olist_order_items_dataset.csv` | `bronze.order_items` | One row per order item |
| `olist_customers_dataset.csv` | `bronze.customers` | One row per customer/order customer ID |
| `olist_products_dataset.csv` | `bronze.products` | One row per product |
| `olist_sellers_dataset.csv` | `bronze.sellers` | One row per seller |
| `olist_order_payments_dataset.csv` | `bronze.order_payments` | One row per payment sequence |
| `olist_order_reviews_dataset.csv` | `bronze.order_reviews` | One row per review |
| `olist_geolocation_dataset.csv` | `bronze.geolocation` | Multiple rows per zip prefix/location |

## Important fields

### orders
- `order_id`: order business key
- `customer_id`: customer business key
- `order_status`: order lifecycle status
- `order_purchase_timestamp`: order purchase timestamp
- `order_delivered_customer_date`: delivered timestamp, nullable

### customers
- `customer_id`: customer business key used by the Olist order model
- `customer_unique_id`: customer identity across orders
- `customer_city`, `customer_state`: customer location attributes

### order_items
- `order_id`, `order_item_id`: composite source key
- `product_id`, `seller_id`: product and seller business keys
- `price`, `freight_value`: item-level measures

## Modelling grain

- `fact_order_item`: one row per `(order_id, order_item_id)`.
- `fact_order_payment`: one row per `(order_id, payment_sequential)`.
- `dim_customer`: one row per customer business key in the current-state Gold model. SCD history is retained in `silver.customer_history`.
- `dim_product`: one row per product.
- `dim_seller`: one row per seller.

## Caveats

The dataset's `customer_id` is generally associated with an order-specific customer record; `customer_unique_id` is the cross-order customer identity. This project uses `customer_id` for order joins and demonstrates historical attribute tracking against that key. Do not conflate the two identifiers.
