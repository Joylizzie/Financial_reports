
set search_path TO ocean;

-- sales_orders
COPY sales_orders (company_code, s_order_date, customer_id)
FROM
    '/tmp/sales_orders.csv' DELIMITER ',' CSV HEADER;

-- sales_orders_items
COPY sales_orders_items(company_code, sales_order_id, product_id, units, unit_selling_price, currency_id,tax_code, shipped)

FROM
    '/tmp/sales_orders_items_i.csv' DELIMITER ',' CSV HEADER;

-- sales invoices    
COPY sales_invoices(company_code, invoice_date, sales_order_id, customer_id, amount)

FROM
    '/tmp/sales_invoices_i_1.csv' DELIMITER ',' CSV HEADER;

-- double entry credit side    
COPY ar_invoice_item (company_code, rie_id, general_ledger_number, cc_id,  currency_id, debit_credit, amount)
FROM
    '/tmp/ar_item_credit.csv' DELIMITER ',' CSV HEADER;



