select * from (
    select  ai.rie_id,
		 	ai.invoice_id,
			ai.date as invoice_date,
			ari.customer_id,
		    ari.general_ledger_number,
		 	ari.debit_credit,
			ari.amount
	from ar_invoice ai
	inner join ar_invoice_item ari
	on ai.rie_id = ari.rie_id
	where ari.company_code = 'US001'
	    and ari.general_ledger_number
	order by  rie_id, debit_credit) tmp1


		(select  ar.rie_id,
	 		ar.rre_id,
			ar.date as receiving_date,
			ar.customer_id,
	        arit.general_ledger_number,
	 		arit.debit_credit,
			arit.amount
	from ar_receipt ar
	inner join ar_receipt_item arit
	on ar.rre_id = arit.rre_id
	where arit.company_code = 'US001'
	  and ar.date between '2021-01-01' and '2021-03-31' 	 
	) tmp2
 on tmp1.rie_id = tmp2.rie_id
order by tmp1.rie_id, tmp1.debit_credit

select debit_credit,sum(amount) from ar_invoice_item
group by debit_credit
order by  debit_credit

  
	) tmp1
