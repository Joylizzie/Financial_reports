
set search_path TO ocean;

COPY companies
FROM
    '/tmp/companies.csv' DELIMITER ',' CSV HEADER;

COPY business_type
FROM
    '/tmp/business_type.csv' DELIMITER ',' CSV HEADER;
    
COPY entry_type
FROM
    '/tmp/entry_type.csv' DELIMITER ',' CSV HEADER;    

COPY coa_categories
FROM
    '/tmp/coa_categories.csv' DELIMITER ',' CSV HEADER;
    
COPY sub_coa_categories
FROM
    '/tmp/sub_coa_categories.csv' DELIMITER ',' CSV HEADER;

COPY currencies
FROM
    '/tmp/currencies.csv' DELIMITER ',' CSV HEADER;

COPY chart_of_accounts
FROM
    '/tmp/chart_of_accounts.csv' DELIMITER ',' CSV HEADER;

COPY profit_centres
FROM
    '/tmp/profit_centres.csv' DELIMITER ',' CSV HEADER;

COPY cost_centres
FROM
    '/tmp/cost_centres.csv' DELIMITER ',' CSV HEADER;

COPY product_categories
FROM
    '/tmp/product_categories.csv' DELIMITER ',' CSV HEADER;

COPY products
FROM
    '/tmp/products.csv' DELIMITER ',' CSV HEADER;

COPY tax
FROM
    '/tmp/tax.csv' DELIMITER ',' CSV HEADER;

COPY wbs
FROM
    '/tmp/wbs.csv' DELIMITER ',' CSV HEADER;

COPY area_code(zip, zipcode_name, city, state, county_name, area)
FROM '/tmp/area_code.csv'
DELIMITER ','
CSV HEADER;

