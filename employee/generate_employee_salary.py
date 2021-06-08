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
#    
#def get_cost_centres_weights(conn):
#    sql = """with x as (
#                select cc_id,count(customer_id) as num_cust, sum(amount) as sum_amount 
#                from ar_invoice_item 
#                where company_code = 'US001' and general_ledger_number = 501001
#                group by cc_id)
#                select cc_id, --round(num_cust/(select sum(num_cust) from x),4) as num_cust_per, 
#		    round(sum_amount/(select sum(sum_amount) from x), 4) as sum_amount_per 
#		    from x
#          """
#    with conn.cursor() as curs:
#        curs.execute(sql)
#        cc = curs.fetchall()
#    df = pd.DataFrame(cc, columns=['cc_id','weights_by_amount'])
#    print(len(df.index))
#    print(df['cc_id'].tolist())
#    return df
#  
def get_employee(conn):
    sql = """select company_code, employee_id, grade from employee_names where company_code = 'US001';
           """
    with conn.cursor() as curs:
        curs.execute(sql)
        employees = curs.fetchall()
    conn.commit()
    df = pd.DataFrame(employees, columns = ['company_code','employee_id', 'grade'])
    return df

    
# individual employee total compensation by month
def grade_monthly_salary(conn,out_file):
    
    # salaries in different grade
    grade_1_s = random.randrange(100000, 300000)
    grade_2_s = random.randrange(50000, 99999)
    grade_3_s = random.randrange(10000, 49999)
   
#    df = get_employee(conn)
    df = pd.read_csv('data/employee_names.csv', usecols=['company_code','employee_id', 'grade_code'])
    n = len(df.index)
    print(n)
    
    df['currency_id'] = 1
    
    condition = [df['grade_code'] == 1, df['grade_code'] == 2, df['grade_code'] == 3]
    values = [grade_1_s,grade_2_s,grade_3_s]
    df['salary'] = np.select(condition, values)
    
    df.to_csv(out_file, columns=['company_code','employee_id', 'grade_code', 'currency_id', 'salary'], header=True,index=False)
    print('Done writing.') 
     
    return df
    
    
#def gen_employee_cost_centre(conn):
#    df = grade_monthly_salary(conn)
#    #df = pd.read_csv('data/employee_ids.csv', usecols=['employee_id'])
#    employee_ids_lst = df['employee_id'].tolist()
#    n = len(df.index)
#
#    # allocate cc_id 
#    df_cc = get_cost_centres_weights(conn)
#    cc = df_cc['cc_id'].tolist()
#    print(len(cc))
#    cc_weights = df_cc['weights_by_amount'].tolist()
#    print(len(cc_weights))
    
      
#    df['cc_id'] = random.choices(cc, weights=cc_weights, k=n)
#    print(df['cc_id'])
#    return df
#    return [('US001',
#            employee_ids_lst[i], 
#            (employee_surnames[i] + ',' + employee_first_names[i][0]),
#            random.choices(cc, weights=weights,k=1)[0],
#            ) for i in range(n)]


def create_csv(conn):
    df = grade_monthly_salary(conn)
    df.to_csv(outfile, columns==['company_code','employee_id','currency_id', 'grade_code'], header=True)
    print('Done writing.')    
    

if __name__ == '__main__':
    db = 'ocean_stream'
    pw = os.environ['POSTGRES_PW']
    user_str = os.environ['POSTGRES_USER']
    conn = _get_conn(pw, user_str)
    out_file = '/home/lizhi/projects/joylizzie/Financial_reports/data/employee_salary.csv'

    grade_monthly_salary(conn, out_file)

