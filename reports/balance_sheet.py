import os
import psycopg2
import datetime
import csv


# get connection
def _get_conn(pw, user_str):
    conn = psycopg2.connect(host="localhost",
                            database = db,
                            user= user_str,
                            password=pw)
    conn.autocommit = False
    return conn

# get (debit - credit) amount during start and end date
def get_t_list(conn, coacat_id_tup, start_date, end_date):
    sql_file = open('reports/t_list_asset.sql', 'r')
    sql = sql_file.read()
    with conn.cursor() as curs:
        curs.execute(sql, {'start_date':start_date, 'end_date':end_date, 'coacat_id_tup':coacat_id_tup})  #cursor closed after the execute action
        t_list = curs.fetchall()
    conn.commit
    print(t_list)
    return t_list 
    
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

def bs(conn, coacat_id, start_date, end_date):
    t = get_tlist(conn, start_date, end_date)
    #cost = get_total_cost(conn, start_date, end_date)
    #expenses = get_total_expenses_api(conn, start_date, end_date)
    #total_expenses = sum(expense for (_,_,expense) in expenses)
    
    balance_at = end_date.strftime("%m") + "_" + end_date.strftime("%Y")
    with open(os.path.join('reporting_results', f'bs_{out_file}.csv'), 'w') as bs:
        name = 'Ocean Stream Balance Sheet ' 
        bs_writer = csv.writer(bs)   
        bs_writer.writerow([f'{name}\n\n'])
        bs_writer.writerow(['',f'as of {end_date}'.rjust(15)])
        for amount in t:
            bs_writer.writerow(['amount', f'{t[8]:3,.2f}'.rjust(15)]) # number will be shown in 2 decimal
        #pl_writer.writerow(['Cost', f'{cost:3,.2f}'.rjust(15)])
        #pl_writer.writerow(['Gross margin', f'{revenue - cost}'])
        #for (gl_num, gl_name, expense) in expenses:
         #   pl_writer.writerow([gl_name, f'{expense:3,.2f}'])
        #pl_writer.writerow(['total_expenses', total_expenses)])
        #pl_writer.writrow(['operating income', revenue - cost - total_expenses])
        print('balance sheet csv done writing')   


        
if __name__ == '__main__':
    db = 'ocean_stream'
    pw = os.environ['POSTGRES_PW']
    user_str = os.environ['POSTGRES_USER']
    conn = _get_conn(pw, user_str)
    coacat_id_tup = (2,3)
    start_date = datetime.date(2021,3,1)
    end_date = datetime.date(2021,3,31)
    get_t_list(conn, coacat_id_tup, start_date, end_date)
