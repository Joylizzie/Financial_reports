
set search_path TO ocean;


COPY ar_receipt (company_code, entry_type_id, customer_id, transaction_date, rie_id, general_ledger_number,  currency_id, debit_credit, amount)
FROM
    '/tmp/ar_receipt_credit.csv' DELIMITER ',' CSV HEADER;


