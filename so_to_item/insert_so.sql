
set search_path TO ocean;


COPY sales_orders (company_code, s_order_date, customer_id)
FROM
    '/tmp/pre_sales_orders.csv' DELIMITER ',' CSV HEADER;


COPY sales_orders_items(company_code, sales_order_id, product_id, units, unit_selling_price, currency_id,tax_code, shipped)

FROM
    '/tmp/pre_sales_orders_items_i.csv' DELIMITER ',' CSV HEADER;
    




