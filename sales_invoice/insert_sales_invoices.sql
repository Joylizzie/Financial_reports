
set search_path TO ocean;


COPY sales_invoices(company_code, invoice_date, sales_order_id, customer_id, amount)

FROM
    '/tmp/pre_sales_invoices.csv' DELIMITER ',' CSV HEADER;


