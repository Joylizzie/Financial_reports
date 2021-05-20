			  
create or replace function ar_aging_report(
	            company_code_p char(6), customer_id_p char(6), query_date date)
  returns table(customer_id_p char(6),
			  invoice_id integer,
			  'within 10 days' varchar(30),
			  'greater than 10 days smaller than 20 days' varchar(50),
			  'greater than 20 days smaller than 30 days' varchar(50),
			  'Over due' varchar(30)
			  )
as
 $$
	select 
			case
			  when query_date - tmp1.invoice_date <10 then 'within 10 days' 
			  when 10 <= query_date - tmp1.invoice_date <20 then 'greater than 10 days smaller than 20 days'
			  when 20 <= query_date - tmp1.invoice_date <=30 then 'greater than 20 days smaller than 30 days' 
			  else 'Over due'
		    end
	from 
        (select customer_id_p,
		        tmp3.invoice_id,
		        tmp3_rie_id, 
		        tmp3.rre_id,
		        query_date::date -tmp3.invoice_date as age_in_days,
		        tmp3.invoice_amount + tmp3.received_amount as remaining_amount
        from (
          	    select  ai.rie_id,
				        ai.invoice_id,
				        ai.date as invoice_date,
				        ari.customer_id,
				        ari.general_ledger_number,
				        ari.debit_credit,
				        ari.amount as invoice_amount
		        from ar_invoice ai
		        inner join ar_invoice_item ari
		        on ai.rie_id = ari.rie_id
		        where ari.company_code = 'US001'
			        and ari.general_ledger_number = 102001
		        order by  rie_id, debit_credit
             ) tmp1
           left join 
		         (select  ar.rie_id,
				        ar.rre_id,
				        ar.date as receiving_date,
				        ar.customer_id,
				        arit.general_ledger_number,
				        arit.debit_credit,
				        -arit.amount as received_amount
		        from ar_receipt ar
		        inner join ar_receipt_item arit
		        on ar.rre_id = arit.rre_id
		        where arit.company_code = 'US001'
		         and arit.general_ledger_number = 102001
		          and ar.date between '2021-01-01' and '2021-03-31'
		        order by  arit.rre_id,arit.debit_credit
		         ) tmp2
	        on  tmp1.customer_id = tmp2.customer_id
	        order by tmp1.rie_id
          ) tmp3
         where tmp3.customer_id = 'WOJ691'  
         order by tmp3.invoice_id, tmp3.rie_id, tmp3.rre_id

	    
	    
    select *, 
    case 
	    when age_in_days < 50 then 'age_in_days < 50'
	    when age_in_days < 60 then '50 <= age_in_days < 60'
	    when age_in_days < 70 then '60 <= age_in_days < 70'
	    when age_in_days < 80 then '70 <= age_in_days < 80'
	    else '80 <= age_in_days'
	    end
    from
    (
    select date, '2021-05-16'::date - date as age_in_days
    from ar_invoice 
    limit 10
    ) as tmp
	    
	
