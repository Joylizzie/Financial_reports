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


# Get (debit - credit) amount by category with rollup during start and end date
def get_t_list(conn, coacat_id_tup, start_date, end_date):
    sql_file = open('reports/t_list_pl.sql', 'r')
    sql = sql_file.read()
    #print(sql)
    
    with conn.cursor() as curs:
        curs.execute(sql, {'start_date':start_date, 'end_date':end_date, 'coacat_id_tup':coacat_id_tup})  #cursor closed after the execute action
        t_list_w_None = curs.fetchall()
    #print(t_list_w_None)
    conn.commit()
    
    # write to csv file 
    with open(os.path.join('reporting_results', 't_list_query_res_pl.csv'), 'w') as write_obj:
        csv_writer = csv.writer(write_obj)
        for item in t_list_w_None:
            csv_writer.writerow(item)
    print('pl_t_list_None done writing')
    return t_list_w_None
           
    
def pl(conn, start_date, end_date):
    t_list_pl = get_t_list(conn, coacat_id_tup, start_date, end_date)     
    out_file = start_date.strftime("%m") + "_" + start_date.strftime("%Y")
    with open(os.path.join('reporting_results', f'pl_{out_file}.csv'), 'w') as pl:
        name = 'Ocean Stream profit and loss - Year 2021' 
        pl_writer = csv.writer(pl)   
        pl_writer.writerow(['Ocean Stream'])
        pl_writer.writerow(['Profit and Loss'])
        pl_writer.writerow(['Year 2021'])
        pl_writer.writerow(['','', f'{start_date.strftime("%b-%Y")}'.center(15)])

        for item in t_list_pl:
            pl_writer.writerow(item)
        print('pl csv done writing')   

        
if __name__ == '__main__':
    db = 'ocean_stream'
    pw = os.environ['POSTGRES_PW']
    user_str = os.environ['POSTGRES_USER']
    conn = _get_conn(pw, user_str)
    coacat_id_tup = (5,6)
    start_date = datetime.date(2021,3,1)
    end_date = datetime.date(2021,3,31)
    #get_t_list(conn, coacat_id_tup, start_date, end_date)
    pl(conn, start_date, end_date)
