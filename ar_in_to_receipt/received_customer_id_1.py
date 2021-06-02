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
			 x[1], 
	         x[0],
             x[2]) for x in random_rdi_tups]

# insert the generated value tuples into database
def insert_ar_receipt_id(conn,n):
    tups = weighted_receipt(conn, n)
    sql_insert = '''insert into ar_receipt(company_code, date,rie_id,customer_id)
                    VALUES(%s,%s,%s, %s)'''

    try:
        with conn.cursor() as curs:
            curs.execute(sql_insert, tups[0]) #cursor close after the execute
        conn.commit()#commit the connection to confirm the insertion
    except (Exception, psycopg2.Error) as error:
        print("Error while executing progamme", error)

    finally:
        # closing database connection.
        if (conn):
            conn.close()
            print("PostgreSQL connection is closed") 

def _to_csv(conn, outfile):
    tups = weighted_receipt(conn,n)
    with open(os.path.join('ar_in_to_receipt', outfile), 'w') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(['company_code', 'date', 'rie_id','customer_id']) # write header
        for tup in tups:
            csv_writer.writerow(tup)
        print('Done writing')               

def batch(conn, b_lst):
    # number of inovoices which receipts pending
    l = len(get_invoice_ids(conn))
    
    for n in b_lst:
        while sum(b_lst) < l:
            if n > l:
                break                
            else: 
                weighted_receipt(conn, n)
                insert_ar_receipt_id(conn,n)
       
        
if __name__ == '__main__':
    db = 'ocean_stream'
    pw = os.environ['POSTGRES_PW']
    user_str = os.environ['POSTGRES_USER']
    conn = _get_conn(pw, user_str)
    outfile = 'pre_ar_receipt_id.csv'
    b_lst = [5, 1, 2]
    get_invoice_ids(conn)
    weighted_receipt(conn,n)
    #_to_csv(conn, outfile)                
