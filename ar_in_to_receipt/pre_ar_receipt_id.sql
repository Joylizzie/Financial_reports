-- generate ar_receipt_ids-rre_ids from below query
-- after insert this query, rre_ids will be auto generated
-- in reality, the date depends on when money received from customers 
insert into ar_receipt(company_code, date, rie_id, customer_id)
select 
	            company_code,
				date '2021-03-25', 
	            rie_id,
                customer_id
              from ar_invoice_item
               where company_code='US001' and general_ledger_number = 102001
         ;
  
