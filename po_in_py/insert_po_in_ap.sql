
set search_path TO ocean;

/*
COPY vendors(company_code, vendor_id, vendor_name, general_ledger_number, currency_id)

FROM
    '/tmp/vendors.csv' DELIMITER ',' CSV HEADER;
    
COPY vendor_addresses(company_code, vendor_id, address_lin1, address_line2, city, state, country, postcode, phone_number, email_address)

FROM
    '/tmp/vendor_addresses.csv' DELIMITER ',' CSV HEADER;

*/
