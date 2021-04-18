insert into ar_invoice(company_code, date, invoice_id)
	select company_code,invoice_date as date, invoice_id from sales_invoices
	        where company_code = 'US001'
	        and invoice_date between '2021-03-01' and '2021-03-31';
