
set search_path TO ocean;


COPY journal_entry_item(company_code, je_id, transaction_date, description, general_ledger_number, cc_id, wbs_code, currency_id, debit_credit, amount)     
FROM
    '/tmp/je_item_capital.csv' DELIMITER ',' CSV HEADER;


