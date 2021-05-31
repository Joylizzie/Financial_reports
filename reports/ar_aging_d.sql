/* This query return a result that all customers owe Ocean Stream at the date of April 16 , with total	
*/


(select tmp3.company_code,
		 cn.customer_name,
		 ca.phone_number,
		 tmp3.rie_id,
		 tmp3.age_in_days,
		 tmp3.current_ar
--		 sum(case when tmp3.age_in_days <10 then tmp3.current_ar else 0 end) as within_10_days,
--		 sum(case when tmp3.age_in_days between 10 and 19 then tmp3.current_ar else 0 end) as within_20_days,
--		 sum(case when tmp3.age_in_days between 20 and 29 then tmp3.current_ar else 0 end) as within_30_days, 
--		 sum(case when tmp3.age_in_days >=30 then tmp3.current_ar else 0 end) as over_30_days
from 
	 ( select tmp1.company_code,
	            tmp1.rie_id,
				tmp2.rre_id,
				tmp1.customer_id,
				'2021-04-16'-tmp1.invoice_date as age_in_days,
				tmp2.receiving_date,
				sum(tmp1.invoice_amount+coalesce(tmp2.received_amount,0)) as current_ar
		from 
		  (select ai.rie_id,
					ai.date as invoice_date,
					ari.customer_id,
					ari.amount as invoice_amount
				 from ar_invoice ai
							inner join ar_invoice_item ari
							on ai.rie_id = ari.rie_id
							where ari.company_code = 'US001'
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
							  where arit.company_code = 'US001'
										and arit.general_ledger_number = 102001
								  order by  arit.rre_id
				  ) tmp2
			on tmp1.rie_id = tmp2.rie_id
		group by tmp1.rie_id,
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

