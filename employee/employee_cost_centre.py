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
    
def get_cost_centres_weights(conn):
    sql = """with x as (
                select cc_id,count(customer_id) as num_cust, sum(amount) as sum_amount 
                from ar_invoice_item 
                where company_code = 'US001' and general_ledger_number = 501001
                group by cc_id)
                select cc_id, --round(num_cust/(select sum(num_cust) from x),4) as num_cust_per, 
		    round(sum_amount/(select sum(sum_amount) from x), 4) as sum_amount_per 
		    from x
          """
    with conn.cursor() as curs:
        curs.execute(sql)
        cc = curs.fetchall()
    df = pd.DataFrame(cc, columns=['cc_id','weights_by_amount'])
#    print(len(df.index))
#    print(df['cc_id'].tolist())
    return df
  
    
# individual employee total compensation by month
def grade_monthly_salary(conn):
    # salaries in different grade
    grade_1_s = random.randrange(100000, 300000)
    grade_2_s = random.randrange(50000, 99999)
    grade_3_s = random.randrange(10000, 49999)
   
    df = pd.read_csv('data/employee_names.csv', usecols=['company_code','employee_id', 'employee_name','grade'])
    n = len(df.index)
#    print(n)
    
    condition = [df['grade'] == 1, df['grade'] == 2, df['grade'] == 3]
    values = [grade_1_s,grade_2_s,grade_3_s]
    df['salary'] = np.select(condition, values)
 
#    print(df)
    return df
    
    
def gen_employee_cost_centre(conn):
    df = grade_monthly_salary(conn)
#    #df = pd.read_csv('data/employee_ids.csv', usecols=['employee_id'])
#    employee_ids_lst = df['employee_id'].tolist()
    n = len(df.index)

    # allocate cc_id 
    df_cc = get_cost_centres_weights(conn)
    cc = df_cc['cc_id'].tolist()
    print(len(cc))
    cc_weights = df_cc['weights_by_amount'].tolist()
    print(len(cc_weights))
    
      
    df['cc_id'] = random.choices(cc, weights=cc_weights, k=n)
    print(df['cc_id'])
    return df
#    return [('US001',
#            employee_ids_lst[i], 
#            (employee_surnames[i] + ',' + employee_first_names[i][0]),
#            random.choices(cc, weights=weights,k=1)[0],
#            ) for i in range(n)]


#def create_csv(data_file, tup_gen, header,out_file):
#    tups = tup_gen(data_file)
#    with open(os.path.join('data', out_file), 'w') as write_obj:
#        csv_writer = csv.writer(write_obj)
#        csv_writer.writerow(header)
#        for i in range(len(tups)):
#            csv_writer.writerow(tups[i])
#        print('Done writing.')    
#    
#
if __name__ == '__main__':
    db = 'ocean_stream'
    pw = os.environ['POSTGRES_PW']
    user_str = os.environ['POSTGRES_USER']
    conn = _get_conn(pw, user_str)
    
    get_cost_centres_weights(conn)
    grade_monthly_salary(conn)
    gen_employee_cost_centre(conn)
#    data_file = '/home/lizhi/projects/joylizzie/Financial_reports/data/list-cities-washington-198j.csv'
#    generate_employee_names(data_file)
#    create_csv(data_file = data_file,
#            out_file = '/home/lizhi/projects/joylizzie/Financial_reports/data/employee_names.csv',
#            tup_gen = generate_employee_names,
#            header = ['company_code','employee_id','employee_name', 'grade'])
