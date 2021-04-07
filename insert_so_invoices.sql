
set search_path TO ocean;


COPY sales_invoices(company_code, invoice_date, sales_order_id, cc_id)

FROM
    '/tmp/sales_invoices.csv' DELIMITER ',' CSV HEADER;


