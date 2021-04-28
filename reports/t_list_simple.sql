select coa.bs_pl_cat,
		tmp.general_ledger_number,
		sum(tmp.amount)
from(
 --je db list
	(select general_ledger_number, 
		sum(case when debit_credit = 'credit' then -amount else amount end) as amount
	from journal_entry_item
	group by general_ledger_number
	) 
union
-- ar invoice item db list
	(select general_ledger_number, 
		sum(case when debit_credit = 'credit' then -amount else amount end) as amount
	from ar_invoice_item
	group by general_ledger_number
	) 
union 
-- ar receipt item db list
	(select general_ledger_number, 
		sum(case when debit_credit = 'credit' then -amount else amount end) as amount
	from ar_receipt_item
	group by general_ledger_number
	) 
union 
	(select general_ledger_number, 
		sum(case when debit_credit = 'credit' then -amount else amount end) as amount
	from ap_invoice_item 
	group by general_ledger_number
	)
union
	(select general_ledger_number, 
		sum(case when debit_credit = 'credit' then -amount else amount end) as amount
	from ap_payment_item 
	group by general_ledger_number
	)
)tmp
inner join chart_of_accounts coa
on coa.general_ledger_number = tmp.general_ledger_number
group by coa.bs_pl_cat,
	tmp.general_ledger_number
order by coa.bs_pl_cat, tmp.general_ledger_number;

