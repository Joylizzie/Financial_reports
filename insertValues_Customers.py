'''import the functions in  file generateCustID.py to create customers, then insert the neccessary values
 into customers table.'''

import psycopg2
from generateCustID import customer_ids,address_line1s,citys

def generate_customer_tuples(n):
    customer_ids_lst = list(customer_ids(n))
    customer_name_lst = [x + ' Ltd.' for x in customer_ids_lst] #customer_name is customer_id + Ltd.
    address_lst = list(address_line1s(n))
    city_lst = citys(datafile, n) 
    return [('US001',
            customer_ids_lst[k], 
            customer_name_lst[k],
            1, 
            address_lst[k],
            city_lst[k],
            'WA',
            'USA',
            '98004',
            '999-999-9999',
            'ab@gmail.com') for k in range(n)]

def insert_customer_tuple(n, cur, conn):
    tups = generate_customer_tuples(n)
    sql = '''insert into customers (company_code,customer_id,customer_name,currency_id,address_line1,city,state,country,
                postcode,phone_number,email_address)
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    for i in range(n):
        cur.execute(sql, tups[i])
    conn.commit()
    

def get_connection():

    connection = psycopg2.connect(user="joy2020",
                                  password="Dan",
                                  host="localhost",
                                  port="5432",
                                  database="ocean_stream")
    connection.autocommit = False
    return connection
    
def process():
    try:
        conn = get_connection()
        cur = conn.cursor()
    
        insert_customer_tuple(n, cur,conn)

    except (Exception, psycopg2.Error) as error:
        print("Error while creating PostgreSQL table", error)

    finally:
        # closing database connection.
        if (conn):
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")

 

datafile = '/home/lizhi/projects/joylizzie/Financial_reports/list-cities-washington-198j.csv'
n=10000
process()

    




