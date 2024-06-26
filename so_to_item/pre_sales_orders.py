import os
import psycopg2
import random
import datetime
import csv

random.seed(5)

# get connection via psycopg2
# def _get_conn(pw, user_str):
#    """use .bashrc to store postgres variables"""
#     conn = psycopg2.connect(host="localhost",
#                             database = db,
#                             user= user_str,
#                             password=pw)
#     conn.autocommit = False
#     return conn

# get connection via psycopg2
def _get_conn(user_str):
    """use .pgpass to store postgres variables"""
    conn = psycopg2.connect(host="localhost",
                            database = db,
                            user= user_str
                            )
    conn.autocommit = False
    return conn



# choose random date bwtween start and end date
def randomdate(start_date, end_date):
    # calculate time between start_date and end_date, then convert the time to days
    days_between_dates = (end_date - start_date).days
    # select random day in above days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date

# fetch existing customer_ids in database where the company_code is 'US001'
# generate sale order tuples
def generate_value_tuples(n, start_date, end_date,conn):

    sql_cust =  """select cn.customer_id,cn.business_type_id from customer_names 
            where company_code='US001';             
                """
    with conn.cursor() as curs:
        curs.execute("set search_path to ocean_stream;")
        curs.execute(sql_cust)  #cursor closed after the execute action
        cust_ids = curs.fetchall()# a list of tuples
        
    random_cust_ids_sample = random.sample(cust_ids, 2*n)

    random_cust_ids = random.choices(random_cust_ids_sample, k=n)
    t = [('US001',randomdate(start_date, end_date),*random_cust_ids[i]) for i in range(n)]
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



if __name__ == '__main__':
    db = 'ocean_stream'
    # pw = os.environ['POSTGRES_PW']
    # user_str = os.environ['POSTGRES_USER']
    # conn = _get_conn(pw, user_str)
    user_str = 'ocean_user'
    conn = _get_conn(user_str)
    start_date = datetime.date(2021, 3, 1)
    end_date = datetime.date(2021, 3, 31)
    n = 5000
    generate_value_tuples(n, start_date, end_date,conn)
    _to_csv(n, conn, outfile='pre_sales_orders.csv')
