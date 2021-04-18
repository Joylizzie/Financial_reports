
set search_path TO ocean;

COPY customer_names
FROM
    '/tmp/customer_names.csv' DELIMITER ',' CSV HEADER;

COPY customer_addresses
FROM
    '/tmp/customer_addresses.csv' DELIMITER ',' CSV HEADER;

