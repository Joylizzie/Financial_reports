import os
import psycopg2
import pandas as pd
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

# get newest chart_of_accounts to a dictionary as general_    
def get_gl(conn):
    sql = """select 
                general_ledger_number, 
                general_ledger_name 
             from chart_of_accounts
             where company_code = 'US001'
              
          """
    with conn.cursor() as curs:
        curs.execute(sql)  #cursor closed after the execute action
        gl_list = curs.fetchall()
    conn.commit()
    return dict(gl_list)


# get (debit - credit) amount during start and end date
def get_t_list(conn, coacat_id_tup, start_date, end_date):
    sql_file = open('reports/t_list_asset.sql', 'r')
    sql = sql_file.read()

    with conn.cursor() as curs:
        curs.execute(sql, {'start_date':start_date, 'end_date':end_date, 'coacat_id_tup':coacat_id_tup})  #cursor closed after the execute action
        t_list = curs.fetchall()
    conn.commit()
    return t_list


def pl(conn, coacat_id_tup, start_date, end_date):
    df = pd.DataFrame(get_t_list(conn, coacat_id_tup, start_date, end_date))
    print(df[0])
    print(df[1])
    print(df[2])
    #print(df.head())
    gl_dict = get_gl(conn)
        
    out_file = start_date.strftime("%m") + "_" + start_date.strftime("%y")
    with open(os.path.join('reporting_results', f'pl_{out_file}.csv'), 'w') as pl:
        name = 'Ocean Stream profit and loss - Year 2021' 
        pl_writer = csv.writer(pl)   
        pl_writer.writerow(['Ocean Stream profit and loss - Year 2021\n\n'])
        pl_writer.writerow(['',f'{start_date.strftime("%b")}'.center(15)])
        for item in df[0]:    
            if 500000 < item < 502001:
                revenue = df[2]
                pl_writer.writerow([df[1], f'{revenue:3,.2f}'.rjust(15)])
            if 502001 <= item <600000:
                cost = df[2]
                pl_writer.writerow([df[1], f'{cost:3,.2f}'.rjust(15)])
                pl_writer.writerow(['Gross margin', f'{revenue - cost}'])
            if item > 600000:
                expense = df[2]
                pl_writer.writerow([df[1], f'{expense:3,.2f}'.rjust(15)])
                #total_expenses = sum(expense for (_,_,expense) in t)
                #pl_writer.writerow(['total_expenses', total_expenses])
            #pl_writer.writerow(['operating income', (revenue - cost - total_expenses)])                    
            print('pl csv done writing')   

if __name__ == '__main__':
    db = 'ocean_stream'
    pw = os.environ['POSTGRES_PW']
    user_str = os.environ['POSTGRES_USER']
    conn = _get_conn(pw, user_str)
    coacat_id_tup = (5,6)
    start_date = datetime.date(2021,3,1)
    end_date = datetime.date(2021,3,31)
    pl(conn, coacat_id_tup, start_date, end_date)
    get_gl(conn)
    get_t_list(conn, coacat_id_tup, start_date, end_date)
    #pl((conn, coacat_id_tup, start_date, end_date))
