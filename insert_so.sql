
set search_path TO ocean;


COPY sales_orders (company_code, s_order_date, customer_id)
FROM
    '/tmp/sales_orders.csv' DELIMITER ',' CSV HEADER;


