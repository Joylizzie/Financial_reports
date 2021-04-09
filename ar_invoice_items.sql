
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
                  
-- credit side                 
insert into ar_invoice_item (company_code, rie_id, general_ledger_number, cc_id, currency_id, debit_credit, amount)
    select ar.company_code, 
            ar.rie_id,
            501001 as general_ledger_number, 
            1 as currency_id, 
            'credit' as debit_credit,
             as amount 
 from ar_invoice 
 group by company_code, transaction_date, customer_id, invoice_id, currency_id
 order by invoice_id;
