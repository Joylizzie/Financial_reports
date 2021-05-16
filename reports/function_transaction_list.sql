/* 1.This function retrieve all transanctions from je, ar_invoice_item, ar_receipt_item,ap_invoice_item, ap_payment_item
   2.Filtered by company_code
  
*/

--drop function transaction_list(char(6),date, date);

create or replace function transaction_list(
                company_code_p char(6), 
                general_ledger_number_sp integer,
                general_ledger_number_ep integer, 
                start_date_p date, 
                end_date_p date) 
   returns table(company_code char(6),
                 entry_type_id char(3),
				 entry_id integer,
                 t_date date,
                 general_ledger_number integer,
                 cost_centre char(5),
                 wbs_code char(5),
                 debit_credit varchar(6),
                 currency_id integer,
                 amount numeric)
as
 $$
  
    select * from
        (
        select je.company_code, 
		        je.entry_type_id, 
		        je.je_id as entry_id,
		        jei.transaction_date as t_date,
		        jei.general_ledger_number,
		        jei.cc_id as cost_centre,
		        jei.wbs_code,
		        jei.debit_credit,
		        jei.currency_id,
		        jei.amount
        from journal_entry_item jei
        inner join journal_entry je
        on je.je_id = jei.je_id
        where je.company_code = company_code_p
            and jei.transaction_date between start_date_p and end_date_p
            and jei.general_ledger_number between general_ledger_number_sp and general_ledger_number_ep
        -- double entries from ar_invoice
        union all
        select ar.company_code, 
		        ar.entry_type_id,
		        ar.rie_id as entry_id,
		        ar.date as t_date,
		        aii.general_ledger_number,
		        aii.cc_id as cost_centre,
		        ''::char(5) as wbs_code,
		        aii.debit_credit,
		        aii.currency_id,
		        aii.amount	
        from ar_invoice as ar
        inner join ar_invoice_item aii
        on ar.rie_id = aii.rie_id
        where ar.company_code = company_code_p
          and aii.general_ledger_number between general_ledger_number_sp and general_ledger_number_ep
          and ar.date between start_date_p and end_date_p
        -- double entries from ar_receipt
        union all
        select arr.company_code,
		        arr.entry_type_id,
		        arr.rre_id as entry_id,
		        arr.date as t_date,
		        ari.general_ledger_number,
		        ''::char(6) cost_centre,
		        ''::char(5)	wbs_code,
		        ari.debit_credit,
		        ari.currency_id,
		        ari.amount
        from ar_receipt arr
        inner join ar_receipt_item ari
        on arr.rre_id = ari.rre_id
        where arr.company_code = company_code_p
         and ari.general_ledger_number between general_ledger_number_sp and general_ledger_number_ep
         and arr.date between start_date_p and end_date_p
        -- double entries from ap_invoice
        union all
        select ap.company_code,
		        ap.entry_type_id,
		        ap.pie_id as entry_id,
		        ap.date as t_date,
		        api.general_ledger_number,
		        api.cc_id as cost_centre,
		        api.wbs_code,
		        api.debit_credit,
		        api.currency_id,
		        api.amount
        from ap_invoice as ap
        inner join ap_invoice_item as api
        on ap.pie_id = api.pie_id
        where ap.company_code = company_code_p
          and api.general_ledger_number between general_ledger_number_sp and general_ledger_number_ep
          and ap.date between start_date_p and end_date_p
        -- double entries from ap_payment
        union all
        select app.company_code,
		        app.entry_type_id,
		        app.ppe_id,
		        app.date as t_date,
		        appi.general_ledger_number,
		        ''::char(6) cost_centre,
		        ''::char(5)	wbs_code,
		        appi.debit_credit,
		        appi.currency_id,
		        appi.amount
        from ap_payment as app
        inner join ap_payment_item as appi
        on app.ppe_id = appi.ppe_id
        where app.company_code = company_code_p
         and appi.general_ledger_number between general_ledger_number_sp and general_ledger_number_ep
         and app.date between start_date_p and end_date_p
        ) tmp
    order by entry_type_id, entry_id, debit_credit;
 
 $$ language sql;


/* 
-- not part of the function, if you want to call the function

 select * from transaction_list('US001', 100001, 999999, '2021-03-01', '2021-03-31');
 
*/
