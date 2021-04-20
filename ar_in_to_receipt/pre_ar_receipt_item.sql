/*
Before products shipped, money is collected from individual customers    

In reality, money received in bank from customers, will be identified who sent the money, for what, like which sales invoice, then double entries will be posted to corresponding customers

Here is just pretending Ocean Stream received the money and all the reconciliations are done and confirmed the results and double entries can be posted to the system.

The double entry will be like this:
    Debit: 100001 Checking acount              usd amount
        Credit: 102001 Accounts Receivables customer_id   usd amount
*/

--credit side
insert into ar_receipt_item(company_code, rre_id, general_ledger_number, currency_id,debit_credit,amount)
    -- get the details of each customers receivables then change to credit side
    select ar.company_code, 
           ar.rre_id, 
           aii.general_ledger_number, 
           aii.currency_id, 
           'credit' as debit_credit,
           aii.amount from ar_receipt ar
    inner join ar_invoice_item aii
    on ar.rie_id = aii.rie_id
    where ar.company_code = 'US001' and aii.general_ledger_number = 102001

--debit side
insert into ar_receipt_item(company_code, rre_id, general_ledger_number, currency_id,debit_credit,amount)
    -- get the details of each customers receivables then change to debit side 'checking account'	 
    select ar.company_code, 
            ar.rre_id,  
            100001 as general_ledger_number,
            aii.currency_id, 
            'debit' as debit_credit,
            aii.amount from ar_receipt ar
    inner join ar_invoice_item aii
    on ar.rie_id = aii.rie_id
    where ar.company_code = 'US001'
    and aii.general_ledger_number = 102001;
