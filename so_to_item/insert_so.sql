
set search_path TO ocean_stream;


\COPY sales_orders (company_code, s_order_date, customer_id) FROM '/tmp/pre_sales_orders_1.csv' DELIMITER ',' CSV HEADER;
    

