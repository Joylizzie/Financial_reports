import os
import psycopg2
import pandas as pd
import numpy as np
import csv
import random

random.seed(5)


# Get connection
def _get_conn(pw, user_str):
    conn = psycopg2.connect(host="localhost",
                            database = db,
                            user= user_str,
                            password=pw)
    conn.autocommit = False
    return conn

# get the percentage of each sales invoice amount to total invoice amount    
def get_cost_centres_weights(conn):
    sql = """with x as (
                select cc_id,count(customer_id) as num_cust, sum(amount) as sum_amount 
                from ar_invoice_item 
                where company_code = 'US001' and general_ledger_number = 501001
                group by cc_id)
                select cc_id,
                        --percentage of each invoice amount of total invoice amount
		               (sum_amount/(select sum(sum_amount) from x)) as sum_amount_per 
		            from x
          """
    with conn.cursor() as curs:
        curs.execute(sql)
        cc = curs.fetchall()
    # to DataFrame    
    df = pd.DataFrame(cc, columns=['cc_id','weights_by_amount'])
    #print(len(df.index))
    return df
    
def get_employee(conn):
    sql = """select employee_id from employee_names where company_code = 'US001';
           """
    with conn.cursor() as curs:
        curs.execute(sql)
        employees = curs.fetchall()
    conn.commit()
    # to DataFrame
    df = pd.DataFrame(employees, columns = ['employee_id'])
    return df
        
def gen_employee_cost_centre(conn):
    df_cc = get_cost_centres_weights(conn)
    cc_lst = df_cc['cc_id'].tolist()
    #print(cc_lst)
    cc_weights_dec = df_cc['weights_by_amount'].tolist()
    cc_weights = []
    for x in cc_weights_dec:
        cc_weights.append(float(x)) # decimal convert to float type 
    #print(cc_weights)  
    df_em = get_employee(conn)
    em_cc_lst = []
    employee_ids_lst = df_em['employee_id'].tolist()
    # length of employee_ids_lst
    n = len(df_em.index)
    for x in employee_ids_lst:
        y = ('US001', x, random.choices(cc_lst, weights=cc_weights, k=1)[0]) # a tuple
        em_cc_lst.append(y)
    print(em_cc_lst)
        
    df_em_cc = pd.DataFrame(em_cc_lst, columns=['company_code','employee_id', 'cc_dd'])
    # to csv
    df_em_cc.to_csv(path_or_buf='data/employee_cost_centres.csv', header=['company_code','employee_id', 'cc_dd'], index=False)
    return df_em_cc
  

if __name__ == '__main__':
    db = 'ocean_stream'
    pw = os.environ['POSTGRES_PW']
    user_str = os.environ['POSTGRES_USER']
    conn = _get_conn(pw, user_str)
    
    get_cost_centres_weights(conn)
    gen_employee_cost_centre(conn)

