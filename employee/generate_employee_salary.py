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
    #df = pd.DataFrame(employees, columns = ['company_code','employee_id', 'grade_code'])
    return employees

       
def get_random_salary(grade):
    ranges = [(60000, 90000), (30000, 59999),(10000, 29999)]
    return random.randrange(*ranges[grade-1])
            
    
# individual employee total compensation by month
def grade_monthly_salary(conn,out_file):
    
    employees = get_employee(conn)
    lst = []
    for tup in employees:
        lst.append(list(tup) + [1] + [get_random_salary(tup[2])])

    with open(out_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(['company_code','employee_id','grade_code','currency_id','salary'])
        writer.writerows(lst)
#        print('done writing')    
    
if __name__ == '__main__':
    db = 'ocean_stream'
    pw = os.environ['POSTGRES_PW']
    user_str = os.environ['POSTGRES_USER']
    conn = _get_conn(pw, user_str)
    out_file = '/home/lizhi/projects/joylizzie/Financial_reports/data/employee_salaries.csv'

    grade_monthly_salary(conn, out_file)

