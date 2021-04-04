import os
import psycopg2
import random
import pandas as pd
import numpy as np
import csv
import itertools


# fetch existing sales_order_ids and product_ids in database where the company_code is 'US001'
# generate sale_orders_items tuples
def _get_conn(pw, user_str):
    conn = psycopg2.connect(host="localhost",
                            database = db,
                            user= user_str,
                            password=pw)
    conn.autocommit = False
    return conn


# get shipped sales order ids placed by individuals
def get_s_so_items(conn):
    sql_so_item = """select
                        si.company_code,
                        so.s_order_date, 
                        si.sales_order_id,
                        si.product_id ,
                        so.customer_id
                     from sales_orders_items  si
                     inner join sales_orders so
                     on si.sales_order_id = so.sales_order_id
                     where si.shipped = 'yes'
                     and si.company_code='US001' 
                     and so.s_order_date between '2021-03-01' and '2021-03-31'
                     order by sales_order_id;           
             """
    with conn.cursor() as curs:
        curs.execute(sql_so_item)  #cursor closed after the execute action
        (s_so_items) = curs.fetchall()

    # write to csv file 
    with open(os.path.join('data', 's_so_items_i.csv'), 'w') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(['company_code','s_order_date', 'sales_order_id', 'product_id', 'customer_id'])
        for s_so_item in s_so_items:
            csv_writer.writerow(s_so_item)
        print('Done writing')
        
    return s_so_items

# map customer_id to predefined areas
# predefined areas are SE- north of king county, SP-east of cascade, KG- king and pierce county,
#                      OY - west of pugesound, south of pierce county, west of cascade.
def geo_cc(a, b):
    a = 'data/customer_addresses.csv'
    b = 'data/area_code.csv' 
    
    df_a = pd.read_csv(a)
    df_b = pd.read_csv(b)
    
    df_b.rename(columns={'zip':'postcode'}, inplace=True) # join on postcode, the column name should be the same
    # new table with two columns 'customer_id', 'area'
    df_c = pd.merge(df_a, df_b, on='postcode', how='right')[['customer_id', 'area']]
    # drop empty rows with empty customer_id
    nan_value = float("NaN")
    df_c.replace('', nan_value, inplace=True)
    df_c.dropna(subset = ["customer_id"], inplace=True) 
    # save to csv    
    df_c.to_csv('data/geo_cc.csv', index=False)
    return df_c
    

def get_cc_ids(pr_cc):
    a = pd.read_csv('data/s_so_items_i.csv')
    b = pd.read_csv('data/geo_cc.csv')
    df = pd.merge(a, b, on='customer_id', how='left')
    df['cc_id'] = df.apply(lambda row: pr_cc[(row.product_id, row.area)], axis =1)
    df.to_csv('data/cc_id.csv', index=False)
    return df[['company_code', 's_order_date', 'sales_order_id', 'cc_id']]
    

# generate sales invoices from above dataframe
def so_invoices(df, pr_cc):
    
    df.rename(columns={'s_order_date': 'invoice_date'}, inplace=True)
    #sales_invoices =[company_code, invoice_date, invoice_id, sales_order_id, general_ledger_number, cc_id]
    return df.to_csv('data/sales_invoices.csv', index=False)
    
    
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
    
    pr_cc = {(3, 'SE'): 'PSE02', (3, 'KG'): 'PKG02', (3, 'SP'): 'PSP02', (3, 'OY'): 'POY02', (4, 'SE'): 'PSE04', (4, 'KG'): 'PKG04', (4, 'SP'): 'PSP04', (4, 'OY'): 'POY04', (5, 'SE'): 'SSE03', (5, 'KG'): 'SKG03', (5, 'SP'): 'SSP03', (5, 'OY'): 'SOY03'} 
    df = get_cc_ids(pr_cc)  
    so_invoices(df, pr_cc)    
