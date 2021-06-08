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

  
def get_employee(conn):
    sql = """select company_code, employee_id, grade_code from employee_names where company_code = 'US001';
           """
    with conn.cursor() as curs:
        curs.execute(sql)
        employees = curs.fetchall()
    conn.commit()
    df = pd.DataFrame(employees, columns = ['company_code','employee_id', 'grade_code'])
    return df

    
# individual employee total compensation by month
def grade_monthly_salary(conn,out_file):
    
    # salaries in different grade
    grade_1_s = random.randrange(100000, 300000)
    grade_2_s = random.randrange(50000, 99999)
    grade_3_s = random.randrange(10000, 49999)
   
    df = get_employee(conn)
    # or read from csv file if employee_names.csv is up to date
#    df = pd.read_csv('data/employee_names.csv', usecols=['company_code','employee_id', 'grade_code'])
#    n = len(df.index)
#    print(n)
    
    df['currency_id'] = 1
    
    condition = [df['grade_code'] == 1, df['grade_code'] == 2, df['grade_code'] == 3]
    values = [grade_1_s,grade_2_s,grade_3_s]
    df['salary'] = np.select(condition, values)
    
    df.to_csv(out_file, columns=['company_code','employee_id', 'grade_code', 'currency_id', 'salary'], header=True,index=False)
    print('Done writing.') 
     
    return df
    
    
if __name__ == '__main__':
    db = 'ocean_stream'
    pw = os.environ['POSTGRES_PW']
    user_str = os.environ['POSTGRES_USER']
    conn = _get_conn(pw, user_str)
    out_file = '/home/lizhi/projects/joylizzie/Financial_reports/data/employee_salary.csv'

    grade_monthly_salary(conn, out_file)

