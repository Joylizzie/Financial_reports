-- each sales_invoice will be followed by a ar_invoice double entry - ar_invoce
-- generate ar_invoice id - rie_ids from below query
-- after insert the query into database, rie_ids will be auto generated
-- info of ar_invoice will feed the table ar_invoice_items

insert into ar_invoice(company_code, date, invoice_id)
	select company_code,invoice_date as date, invoice_id from sales_invoices
	        where company_code = 'US001'
	        and invoice_date between '2021-03-01' and '2021-03-31';
