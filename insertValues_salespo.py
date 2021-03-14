import os
import random
import datetime

import psycopg2

from common import randomdate
from common import retrieve_data

# fetch existing customer_ids in database ocean_stream where the company_code is 'US001'
# generate sale order tuples
def generate_value_tuples(n):
    print('generating value tuples....')
    #retrieve existing data to a list of tuples
    item_lst = retrieve_data(conn, sql)
    # unpack item_lst to tuples to feed column, here is "customer_id", plus the values to feed other related columns, form a list of tuples
    t = [('US001',randomdate(start_date, end_date),*item_lst[i]) for i in range(n)]
    return t

# insert the generated value tuples into database
def insert_values_tuples(n, conn, sql_insert):
    tups = generate_value_tuples(n)
    with conn.cursor() as curs:
        for i in range(n):
            curs.execute(sql_insert, tups[i]) #cursor close after the execute
    conn.commit()#commit the connection to confirm the insertion

# call the function with parameters to see if the function works# 
sql = """select customer_id from customers where company_code='US001'
      """

sql_insert = ''' insert into sales_orders(company_code,s_order_date,customer_id)
                    values(%s,%s,%s)
            '''
if __name__ == '__main__':
    conn = psycopg2.connect(
        host="localhost",
        database="ocean_stream",
        user="financial_user",
        password=os.environ['POSTGRES_PW'])
    n = 10
    start_date = datetime.date(2021, 3, 1)
    end_date = datetime.date(2021, 3, 31)
    print(insert_values_tuples(n, conn, sql_insert))

