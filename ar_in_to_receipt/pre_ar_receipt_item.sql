--credit side

insert into ar_receipt_item(company_code, rre_id, general_ledger_number, currency_id,debit_credit,amount)		 
select ar.company_code, ar.rre_id, aii.general_ledger_number, 
	aii.currency_id, 'credit' as debit_credit, aii.amount from ar_receipt ar
inner join ar_invoice_item aii
on ar.rie_id = aii.rie_id
where ar.company_code = 'US001' and aii.general_ledger_number = 102001

--debit side
insert into ar_receipt_item(company_code, rre_id, general_ledger_number, currency_id,debit_credit,amount)		 
select ar.company_code, ar.rre_id,  100001 as general_ledger_number, 
	aii.currency_id, 'debit' as debit_credit, aii.amount from ar_receipt ar
inner join ar_invoice_item aii
on ar.rie_id = aii.rie_id
where ar.company_code = 'US001' and aii.general_ledger_number = 102001
