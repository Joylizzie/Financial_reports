set search_path TO ocean_stream;

\COPY ar_receipt(company_code, date,rie_id,customer_id) FROM '/tmp/pre_ar_receipt_id.csv' DELIMITER ',' CSV HEADER;
  
