-- get shipped sales order ids placed by individuals
-- credit side
insert into ar_invoice_item (company_code, rie_id, customer_id, general_ledger_number,cc_id, currency_id, debit_credit, amount)
select tmp.company_code,
       ari.rie_id,
       --tmp.sales_order_id,       
       si.customer_id,
      -- si.invoice_id,
       tmp.general_ledger_number,
       concat( p.cat_id,ac.area,'0', tmp.product_id)  as cc_id,	   
       tmp.currency_id,
       tmp.debit_credit,
       tmp.amount 
from(
        (select 
               soi.company_code,
               soi.sales_order_id,
               soi.product_id,
               501001 as general_ledger_number,
               1 as currency_id,
               'credit' as debit_credit,
               soi.units * soi.unit_selling_price as amount
           from sales_orders_items  soi
           where soi.shipped = 'yes'
          )  
    union 
        (select 
               soi.company_code,
               soi.sales_order_id,
               soi.product_id,
               203001 as general_ledger_number,
               1 as currency_id,
               'credit' as debit_credit,               
               soi.units * soi.unit_selling_price * t.tax_rate as amount
            from sales_orders_items  soi
            inner join tax t
            on t.tax_code = soi.tax_code
             where soi.shipped = 'yes'
        )   
    ) tmp
    
inner join sales_invoices si
on si.sales_order_id = tmp.sales_order_id
inner join ar_invoice ari
on ari.invoice_id = si.invoice_id
inner join customer_addresses ca
on ca.customer_id = si.customer_id
inner join area_code as ac
on ca.postcode = ac.zip
inner join products p
on p.product_id = tmp.product_id
--inner join customer_names cn
--on si.customer_id = cn.customer_id
--where cn.business_type_id = 2
order by ari.rie_id;
  

