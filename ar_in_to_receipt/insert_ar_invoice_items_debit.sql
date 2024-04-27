
set search_path TO ocean_stream;

-- debit side
insert into ar_invoice_item (company_code, rie_id, customer_id, general_ledger_number, currency_id, debit_credit, amount)
	select
                    si.company_code,                    
                    ar.rie_id,
					si.customer_id,
                    102001 as general_ledger_number,
                    1 as currency_id,
					'debit' as debit_credit,
                    si.amount	
                  from sales_invoices si
                  inner join ar_invoice ar
                  on si.invoice_id = ar.invoice_id                
                  where si.company_code = 'US001'
                  and si.invoice_date between '2021-03-01' and '2021-03-31'
                  order by si.invoice_id;
                  

