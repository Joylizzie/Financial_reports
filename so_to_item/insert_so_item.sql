
set search_path TO ocean_stream;


COPY sales_orders_items(company_code, sales_order_id, product_id, units, unit_selling_price, currency_id,tax_code, shipped)

FROM
    '/tmp/pre_sales_orders_items_i_2021_03.csv' DELIMITER ',' CSV HEADER;

COPY sales_orders_items(company_code, sales_order_id, product_id, units, unit_selling_price, currency_id,tax_code, shipped)

FROM
    '/tmp/pre_sales_orders_items_b_2021_03.csv' DELIMITER ',' CSV HEADER;

