
set search_path TO ocean;


COPY ar_invoice_item (company_code, rie_id, description,general_ledger_number, cc_id,  currency_id, debit_credit, amount)
FROM
    '/tmp/pre_ar_invoices_credit_i_3.csv' DELIMITER ',' CSV HEADER;


