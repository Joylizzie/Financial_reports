/* 1.This query provides all transanctions from je, ar_invoice_item, ar_receipt_item,ap_invoice_item, ap_payment_item
   2.The amount is grouped by bs_pl_index
   3.Filted by company_code
   4.Signed bs_pl_index as variale so that python can use it
  
   5. The liabilities and shareholder's equity are showing as negative numbers, this is not the convention
   6. This query is to change 'credit' as postitive number 
*/

set search_path to ocean_stream;

select coa.bs_pl_index,
        bpi.bs_pl_cat_name,
        
		--tmp.general_ledger_number,
		sum(tmp.amount)
from(
 --je db list
	(select general_ledger_number, 
		sum(case when debit_credit = 'debit' then -amount else amount end) as amount
	from journal_entry_item je
	where je.company_code = 'US001'
	group by general_ledger_number
	) 
union
-- ar invoice item db list
	(select general_ledger_number, 
		sum(case when debit_credit = 'debit' then -amount else amount end) as amount
	from ar_invoice_item ar
	where ar.company_code = 'US001'
	group by general_ledger_number
	) 
union 
-- ar receipt item db list
	(select general_ledger_number, 
		sum(case when debit_credit = 'debit' then -amount else amount end) as amount
	from ar_receipt_item arr
	where arr.company_code = 'US001'
	group by general_ledger_number
	) 
union 
	(select general_ledger_number, 
		sum(case when debit_credit = 'debit' then -amount else amount end) as amount
	from ap_invoice_item api
	where api.company_code = 'US001'
	group by general_ledger_number
	)
union
	(select general_ledger_number, 
		sum(case when debit_credit = 'debit' then -amount else amount end) as amount
	from ap_payment_item app
	where app.company_code = 'US001'
	group by general_ledger_number
	)
)tmp
inner join chart_of_accounts coa
on coa.general_ledger_number = tmp.general_ledger_number
inner join bs_pl_idx bpi -- trying get name of bs_pl_index
on bpi.bs_pl_index = coa.bs_pl_index
where bpi.bs_pl_index in %(bs_pl_index_tup)s -- sign as variable, Python code can change it and get different result	 
group by coa.bs_pl_index,
         bpi.bs_pl_cat_name
order by coa.bs_pl_index;


