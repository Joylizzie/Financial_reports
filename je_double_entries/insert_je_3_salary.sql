
--assuming the salaries paid to employees by checking account

--debit side: cost of goods sold
insert into journal_entry_item(company_code,je_id,transaction_date, description,general_ledger_number, cc_id, currency_id,debit_credit,amount)    
    select 
        ecc.company_code, 
        3 as je_id,
        '2021-03-31' as transaction_date,
        'Salary in March 2021' as description,
        502001 as general_ledger_number,
        ecc.cc_id, 
        es.currency_id, 
        'debit' as debit_credit,
        es.salary
    from employee_cost_centres ecc
    inner join employee_salaries es
    on es.employee_id = ecc.employee_id
    where ecc.company_code = 'US001'
    order by ecc.cc_id;


-- credit side, paid to employee from checkong account
insert into journal_entry_item(company_code,je_id,transaction_date, description,general_ledger_number, cc_id, currency_id,debit_credit,amount)    
select 
        ecc.company_code, 
        3 as je_id,
        '2021-03-31' as transaction_date,
        'Salary in March 2021' as description,
        100001 as general_ledger_number,
        ecc.cc_id, 
        es.currency_id, 
        'credit' as debit_credit,
        es.salary
    from employee_cost_centres ecc
    inner join employee_salaries es
    on es.employee_id = ecc.employee_id
    where ecc.company_code = 'US001'
    order by ecc.cc_id;
					
					
