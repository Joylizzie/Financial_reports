import os
import psycopg2
import datetime
import random
import pandas as pd
import numpy as np
import csv


# get connection
def _get_conn(pw, user_str):
    conn = psycopg2.connect(host="localhost",
                            database = db,
                            user= user_str,
                            password=pw)
    conn.autocommit = False
    return conn


def get_total_revenue(conn, start_date, end_date):
    sql = """select sum(ai.amount) from ar_invoice_item ai
               inner join ar_invoice ar
               on ai.rie_id = ar.rie_id                
               where general_ledger_number = 501001
               and ai.company_code = 'US001'
               and ar.date between %s and %s;
        """ 
    with conn.cursor() as curs:
        curs.execute(sql,(start_date, end_date))  #cursor closed after the execute action
        (revenue) = curs.fetchone()
    conn.commit
    return revenue[0] # get the first item in the tuple
    
# the tables in get_total_cost and get_total_expenses are not finalized yet and no data too. 
'''
def get_total_cost(conn, start_date, end_date):
    sql = 
       """select sum(amount) from ap_invoice
             where general_ledger_number = 502001
               and company_code = 'US001'
               and date between %s and %s;
        """ 
    with conn.cursor() as curs:
        curs.execute(sql,(start_date, end_date))  #cursor closed after the execute action
        (cost) = curs.fetchone()
    conn.commit
    return cost
    
    
    
def get_total_expenses_api(conn, start_date, end_date):
    sql = 
       """ select api.general_ledger_number, coa.general_ledger_name, sum(api.amount) 
           from ap_invoice api
           inner join chart_of_accounts coa
           on api.general_ledger_number = coa.general_ledger_number
           where company_code = 'US001'
           and api.general_ledger_number <> 502001
           and api.transaction_date between %s and %s
           group by api.general_ledger_number, coa.general_ledger_name
           order by api.general_ledger_number;
        """ 
    with conn.cursor() as curs:
        curs.execute(sql,(start_date, end_date))  #cursor closed after the execute action
        total_expenses = curs.fetchall()
    conn.commit
    return total_expenses
'''

def pl(conn, start_date, end_date):
    revenue = get_total_revenue(conn, start_date, end_date)
    #cost = get_total_cost(conn, start_date, end_date)
    #expenses = get_total_expenses_api(conn, start_date, end_date)
    #total_expenses = sum(expense for (_,_,expense) in expenses)

    with open(os.path.join('data', 'pl.csv'), 'w') as pl:
        name = 'Ocean Stream profit and loss - Year 2021' 
        pl_writer = csv.writer(pl)   
        pl_writer.writerow(['Ocean Stream profit and loss - Year 2021\n\n'])
        pl_writer.writerow(['',f'{start_date.strftime("%b")}'])
        pl_writer.writerow(['Revenue', f'{revenue}'])
        #pl_writer.writerow(['Cost', f'{cost}'])
        #pl_writer.writerow(['Gross margin', f'{revenue - cost}'])
        #for (gl_num, gl_name, expense) in expenses:
         #   pl_writer.writerow([gl_name, expense])
        #pl_writer.writerow(['total_expenses', total_expenses)])
        #pl_writer.writrow(['operating income', revenue - cost - total_expenses])    


        
if __name__ == '__main__':
    db = 'pacific'
    pw = os.environ['POSTGRES_PW']
    user_str = os.environ['POSTGRES_USER']
    conn = _get_conn(pw, user_str)
    start_date = datetime.date(2021,3,1)
    end_date = datetime.date(2021,3,31)
    pl(conn, start_date, end_date)
