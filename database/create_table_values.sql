
set search_path TO ocean;

COPY companies
FROM
    '/tmp/companies.csv' DELIMITER ',' CSV HEADER;

COPY business_type
FROM
    '/tmp/business_type.csv' DELIMITER ',' CSV HEADER;
    
COPY fiscal_months(year, month, start_date, end_date)
FROM
    '/tmp/fiscal_months.csv' DELIMITER ',' CSV HEADER;    
    
COPY entry_type
FROM
    '/tmp/entry_type.csv' DELIMITER ',' CSV HEADER;    

COPY coa_categories(coacat_id,coa_category_name)
FROM
    '/tmp/coa_categories.csv' DELIMITER ',' CSV HEADER;
    
COPY sub_coa_categories(sub_coacat_id, sub_coacat_name, coacat_id)
FROM
    '/tmp/sub_coa_categories.csv' DELIMITER ',' CSV HEADER;
    
COPY bs_pl_idx(bs_pl_index, bs_pl_cat_name,coacat_id, sub_coacat_id)
FROM
    '/tmp/bs_pl_idx.csv' DELIMITER ',' CSV HEADER;    

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

COPY product_categories(company_code, cat_id, cat_name, subcat_id, subcat_name)
FROM
    '/tmp/product_categories.csv' DELIMITER ',' CSV HEADER;

COPY products(company_code, product_id, cat_id, product_name, product_unit_name, product_units, product_unit_price, currency_id)
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



