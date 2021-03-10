drop table if exists test_csv;
create table if not exists test_csv(
    name varchar(10),
    num integer
    );
COPY test_csv
FROM '/home/henry/projects/Financial_reports/test.csv' 
DELIMITER ','
CSV HEADER;
