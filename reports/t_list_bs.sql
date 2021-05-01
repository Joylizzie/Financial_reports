-- create view
--combine double entries posted in journal_entry, ar and ap
-- double entries from je

CREATE VIEW bs_t_list AS
    select  coa.coacat_id,
            cc.coa_category_name,
            coa.sub_coacat_id,
            sub_coa.sub_coacat_name,
            coa.bs_pl_index,
            bpi.bs_pl_cat_name,
	       --tmp.general_ledger_number,
	       --coa.general_ledger_name,
	       sum(case when tmp.debit_credit = 'credit' then -tmp.amount else tmp.amount end)
    from
        (
        select je.company_code, 
		        je.entry_type_id, 
		        je.je_id as entry_id,
		        je.transaction_date as date,
		        jei.general_ledger_number,
		        jei.cc_id as cost_centre,
		        jei.wbs_code,
		        jei.debit_credit,
		        jei.currency_id,
		        jei.amount,
		        coa.coacat_id
        from journal_entry_item jei
        inner join journal_entry je
        on je.je_id = jei.je_id
        inner join chart_of_accounts coa
        on coa.general_ledger_number = jei.general_ledger_number
        where je.company_code = 'US001'
        and je.transaction_date between %(start_date)s and %(end_date)s
        and coa.coacat_id in %(coacat_id_tup)s
        -- double entries from ar_invoice
        union all
        select ar.company_code, 
		        ar.entry_type_id,
		        ar.rie_id as entry_id,
		        ar.date,
		        aii.general_ledger_number,
		        aii.cc_id as cost_centre,
		        ''::char(5) as wbs_code,
		        aii.debit_credit,
		        aii.currency_id,
		        aii.amount,
		        coa.coacat_id	
        from ar_invoice as ar
        inner join ar_invoice_item aii
        on ar.rie_id = aii.rie_id
        inner join chart_of_accounts coa
        on coa.general_ledger_number = aii.general_ledger_number
        where ar.company_code = 'US001'
        and ar.date between %(start_date)s and %(end_date)s
        and coa.coacat_id in %(coacat_id_tup)s
        -- double entries from ar_receipt
        union all
        select arr.company_code,
		        arr.entry_type_id,
		        arr.rre_id as entry_id,
		        arr.date,
		        ari.general_ledger_number,
		        ''::char(6) cost_centre,
		        ''::char(5)	wbs_code,
		        ari.debit_credit,
		        ari.currency_id,
		        ari.amount,
		        coa.coacat_id
        from ar_receipt arr
        inner join ar_receipt_item ari
        on arr.rre_id = ari.rre_id
        inner join chart_of_accounts coa
        on coa.general_ledger_number = ari.general_ledger_number
        where arr.company_code = 'US001'
        and arr.date between %(start_date)s and %(end_date)s
        and coa.coacat_id in %(coacat_id_tup)s
        -- double entries from ap_invoice
        union all
        select ap.company_code,
		        ap.entry_type_id,
		        ap.pie_id as entry_id,
		        ap.date,
		        api.general_ledger_number,
		        api.cc_id as cost_centre,
		        api.wbs_code,
		        api.debit_credit,
		        api.currency_id,
		        api.amount,
		        coa.coacat_id
        from ap_invoice as ap
        inner join ap_invoice_item as api
        on ap.pie_id = api.pie_id
        inner join chart_of_accounts coa
        on coa.general_ledger_number = api.general_ledger_number
        where ap.company_code = 'US001'
        and ap.date between %(start_date)s and %(end_date)s
        and coa.coacat_id in %(coacat_id_tup)s
        -- double entries from ap_payment
        union all
        select app.company_code,
		        app.entry_type_id,
		        app.ppe_id,
		        app.date,
		        appi.general_ledger_number,
		        ''::char(6) cost_centre,
		        ''::char(5)	wbs_code,
		        appi.debit_credit,
		        appi.currency_id,
		        appi.amount,
		        coa.coacat_id
        from ap_payment as app
        inner join ap_payment_item as appi
        on app.ppe_id = appi.ppe_id
        inner join chart_of_accounts coa
        on coa.general_ledger_number = appi.general_ledger_number
        where app.company_code = 'US001'
        and app.date between %(start_date)s and %(end_date)s
        and coa.coacat_id in %(coacat_id_tup)s
    ) tmp
    inner join chart_of_accounts coa
    on coa.general_ledger_number = tmp.general_ledger_number
    inner join coa_categories cc
    on cc.coacat_id = coa.coacat_id
    inner join sub_coa_categories sub_coa
    on sub_coa.sub_coacat_id = coa.sub_coacat_id
    inner join bs_pl_idx bpi
    on  bpi.bs_pl_index = coa.bs_pl_index
        --where tmp.company_code = 'US001'
        --and tmp.date between %(start_date)s and %(end_date)s
        --and coa.coacat_id in %(coacat_id_tup)s
    group by rollup(coa.coacat_id,
                    cc.coa_category_name,
                    coa.sub_coacat_id,
                    sub_coa.sub_coacat_name,
                    coa.bs_pl_index,    
                    bpi.bs_pl_cat_name
            --rollup(  
                    
                     --tmp.coacat_id,
		             --tmp.general_ledger_number,
		             --coa.general_ledger_name
		             )
    order by coa.coacat_id,
            cc.coa_category_name,
            coa.sub_coacat_id,
            sub_coa.sub_coacat_name,
            coa.bs_pl_index,  
            bpi.bs_pl_cat_name;
              --coa.coacat_id,coa.sub_coacat_id,bpi.bs_pl_index;
