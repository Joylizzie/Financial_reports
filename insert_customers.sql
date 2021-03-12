COPY customers
FROM '/tmp/customers.csv'
DELIMITER ','
CSV HEADER;
