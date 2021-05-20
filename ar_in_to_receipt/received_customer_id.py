import os
import random
import psycopg2
import datetime
import csv
random.seed(5)

# This script is generate values for ar_receipt. 
# Pretending some of the customers will pay immediately upon the product is delievered, some long term customers
# will be in some period of time, with predefined percentage


# connect to 
def _get_conn(pw, user_str):
    conn = psycopg2.connect(host="localhost",
                            database = db,
                            user= user_str,
                            password=pw)
    conn.autocommit = False
    return conn
    
def get_invoice_ids(conn):
    sql = """ select rie_id, date as invoice_date, customer_id
            from ar_invoice ai
            inner join sales_invoices si
            on ai.invoice_id = si.invoice_id
            where ai.rie_id not in 
	            (select rie_id from ar_receipt where company_code = 'US001')
          """
    with conn.cursor() as curs:
        curs.execute(sql)
        (rdi) = curs.fetchall()
    conn.commit()
    #print(list(rdi))
    return rdi
    
 
def weighted_receipt(conn, n):
    # assuming n number of invoices issued will be received in the same month
    rdi_tups = get_invoice_ids(conn)
    random_rdi_tups = random.sample(list(rdi_tups), n)

    return [('US001',
			 '2021-03-31', 
	         x[0],
             x[2]) for x in random_rdi_tups]


def _to_csv(conn, outfile):
    tups = weighted_receipt(conn,n)
    with open(os.path.join('ar_in_to_receipt', outfile), 'w') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(['company_code', 'date', 'rie_id','customer_id']) # write header
        for tup in tups:
            csv_writer.writerow(tup)
        print('Done writing')               

if __name__ == '__main__':
    db = 'ocean_stream'
    pw = os.environ['POSTGRES_PW']
    user_str = os.environ['POSTGRES_USER']
    conn = _get_conn(pw, user_str)
    outfile = 'pre_ar_receipt_id.csv'
    n=2000
    get_invoice_ids(conn)
    weighted_receipt(conn,n)
    _to_csv(conn, outfile)                
