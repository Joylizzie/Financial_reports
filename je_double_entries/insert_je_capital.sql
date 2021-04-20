
set search_path TO ocean;


COPY journal_entry_item
FROM
    '/tmp/je_double_entries/je_item_capital.csv' DELIMITER ',' CSV HEADER;


