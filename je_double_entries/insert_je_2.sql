
set search_path TO ocean_stream;


\COPY journal_entry_item FROM '/tmp/je_item_2.csv' DELIMITER ',' CSV HEADER;


