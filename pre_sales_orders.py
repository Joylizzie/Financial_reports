import os
import psycopg2
import random
import datetime
import csv
from common import randomdate


# get connection via psycopg2
def _get_conn(pw, user_str):
    conn = psycopg2.connect(host="localhost",
                            database = db,
                            user= user_str,
                            password=pw)
    conn.autocommit = False
    return conn

# fetch existing customer_ids in database where the company_code is 'US001'
# generate sale order tuples
def generate_value_tuples(n, start_date, end_date,conn):

    sql_cust =  """select customer_id from customer_names where company_code='US001';             
                """
    with conn.cursor() as curs:
        curs.execute(sql_cust)  #cursor closed after the execute action
        item_lst = curs.fetchall()# a list of tuples
    t = [('US001',randomdate(start_date, end_date),*item_lst[i]) for i in range(n)]
    return t

         
# generate sales order values and save in csv file, then upload to db from psql which is quicker comparing to below way.
def _to_csv(n, conn, outfile):
    tups = generate_value_tuples(n, start_date, end_date, conn)
    with open(os.path.join('intermediate_csv', outfile), 'w') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(['company_code', 's_order_date', 'customer_id']) # write header
        for i in range(n):
            csv_writer.writerow(tups[i])
        print('Done writing')

# OR connect db and insert the above generated values into db directly.
# Note, when use random function, the values generated in different run would be different, not recommend to use  this way           
def insert_value_tuple(conn, sql_insert):
    tups = generate_value_tuples(conn) 
    cur = conn.cursor()
    try:
        for tup in tups:
            cur.execute(sql_insert, tups)
        conn.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error while executing progamme", error)

    finally:
        # closing database connection.
        if (conn):
            conn.close()
            print("PostgreSQL connection is closed")

if __name__ == '__main__':
    db = 'pacific'
    pw = os.environ['POSTGRES_PW']
    user_str = os.environ['POSTGRES_USER']
    conn = _get_conn(pw, user_str)
    start_date = datetime.date(2021, 3, 1)
    end_date = datetime.date(2021, 3, 31)
    n = 18000
    _to_csv(n, conn, outfile='pre_sales_orders.csv')
