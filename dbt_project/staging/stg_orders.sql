SELECT
    order_id,
    customer_id,
    customer_name,
    product,
    category,
    quantity,
    unit_price,
    order_date,
    city,
    country,
    total_amount,
    loaded_at
FROM {{ source('ecommerce', 'raw_orders') }}