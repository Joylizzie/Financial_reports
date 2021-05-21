import os
import psycopg2
import csv


# Get connection
def _get_conn(pw, user_str):
    conn = psycopg2.connect(host="localhost",
                            database = db,
                            user= user_str,
                            password=pw)
    conn.autocommit = False
    return conn
    
def ar_aging(conn, company_code, query_date):
    sql_file = open('reports/ar_aging_w_p.sql', 'r')
    sql = sql_file.read()
    
    with conn.cursor() as curs:
        curs.execute(sql, {'company_code':company_code, 'query_date':query_date})  #cursor closed after the execute action
        (ar_aging) = curs.fetchall()
        return ar_aging
    conn.commit()

def to_csv(conn, company_code, query_date):
    ar_aging_tups = ar_aging(conn, company_code, query_date) 
      
    with open(os.path.join('reporting_results', f'ar_aging_report_{query_date}.csv'),'w', newline='') as write_obj:
        ar_aging_writer = csv.writer(write_obj)
        ar_aging_writer.writerow(['Customer Name', 'Phone number', 'Total current AR', 'Within 10 days','Within 20 days ', 'Within 30 days', 'Over 30 days']) # write header
        for tup in ar_aging_tups:
            ar_aging_writer.writerow(tup) 
        print('aging report done writing')   
    
if __name__ == '__main__':
    db = 'ocean_stream'
    pw = os.environ['POSTGRES_PW']
    user_str = os.environ['POSTGRES_USER']
    conn = _get_conn(pw, user_str)
    query_date = '2021-04-16'
    company_code = 'US001'
    ar_aging(conn, company_code, query_date)
    to_csv(conn, company_code, query_date)
