
set search_path TO ocean;


COPY journal_entry_item
FROM
    '/tmp/je_item_2.csv' DELIMITER ',' CSV HEADER;


