/* This query return a result that all customers owe Ocean Stream at the date of April 16(first part) , with total(second part)	
*/

--by customer
set search_path to ocean_stream;

(select tmp3.company_code,
		 cn.customer_name,
		 ca.phone_number,
		 tmp3.rie_id,
		 tmp3.age_in_days,
		 tmp3.current_ar
from 
	 ( select tmp1.company_code,
	            tmp1.rie_id,
				tmp2.rre_id,
				tmp1.customer_id,
				%(query_date)s-tmp1.invoice_date as age_in_days,
				tmp2.receiving_date,
				sum(tmp1.invoice_amount+coalesce(tmp2.received_amount,0)) as current_ar
		from 
		  (select ai.company_code,
		            ai.rie_id,
					ai.date as invoice_date,
					ari.customer_id,
					ari.amount as invoice_amount
				 from ar_invoice ai
							inner join ar_invoice_item ari
							on ai.rie_id = ari.rie_id
							where ari.company_code = %(company_code)s
								and ari.general_ledger_number = 102001
							order by  ai.rie_id) tmp1
			left join 
				 (select  ar.rie_id,
									ar.rre_id,
									ar.date as receiving_date,
									ar.customer_id,
									-arit.amount as received_amount
							  from ar_receipt ar
							  inner join ar_receipt_item arit
							  on ar.rre_id = arit.rre_id
							  where arit.company_code = %(company_code)s
										and arit.general_ledger_number = 102001
								  order by  arit.rre_id
				  ) tmp2
			on tmp1.rie_id = tmp2.rie_id
		group by tmp1.company_code,
		        tmp1.rie_id,
				tmp2.rre_id,
				tmp1.customer_id,
				tmp1.invoice_date,
				tmp2.receiving_date
	 ) tmp3
	 inner join customer_names cn
	 on cn.customer_id=tmp3.customer_id
	 inner join customer_addresses ca
	 on ca.customer_id = tmp3.customer_id
	 where tmp3.current_ar <> 0
order by cn.customer_name)

