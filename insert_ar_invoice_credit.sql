
set search_path TO ocean;


COPY ar_invoice_item (company_code, rie_id, general_ledger_number, cc_id,  currency_id, debit_credit, amount)
FROM
    '/tmp/ar_item_credit.csv' DELIMITER ',' CSV HEADER;


