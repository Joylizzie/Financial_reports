import os
import psycopg2
import pandas as pd
import numpy as np
import datetime
import csv
from balance_sheet_2 import blank_bs



# Get connection
def _get_conn(pw, user_str):
    conn = psycopg2.connect(host="localhost",
                            database = db,
                            user= user_str,
                            password=pw)
    conn.autocommit = False
    return conn
    
    
def get_t_list(conn, coacat_id_tup, start_date, end_date):
    sql_file = open('reports/t_list_bs_ca.sql', 'r')
    sql = sql_file.read()
  
    with conn.cursor() as curs:
        curs.execute(sql, {'start_date':start_date, 'end_date':end_date, 'coacat_id_tup':coacat_id_tup}) 
        bs_ca_t_list = curs.fetchall()
    conn.commit()
    # write to csv file 
    with open(os.path.join('reporting_results', 'bs_ca_t_list.csv'), 'w') as write_obj:
        csv_writer = csv.writer(write_obj)
        for item in bs_ca_t_list:
            csv_writer.writerow(item)
        t_dict = {}
        for row in bs_ca_t_list:
            t_dict[row[0]] = row[1]
           
    #print('bs_ca_t_list done writing')
    return t_dict
    

def t_to_bs(conn, coacat_id_tup, start_date, end_date):
    df = pd.read_csv('reporting_results/blank_bs.csv', header=None)
    print(df.iloc[:,2])
    t_dict = get_t_list(conn, coacat_id_tup, start_date, end_date)
    for item in df.iloc[:,2]:
        for k in t_dict.keys():
            if item == k:
                df.replace(to_replace=np.nan,value=t_dict.get(k), inplace=True)
    print(df)
    return df    


    
if __name__ == '__main__':
    # parameters:
    db = 'ocean_stream'
    pw = os.environ['POSTGRES_PW']
    user_str = os.environ['POSTGRES_USER']
    conn = _get_conn(pw, user_str)
    coacat_id_tup = (1,)
    start_date = datetime.date(2021,3,1)
    end_date = datetime.date(2021,3,31)
    # call functions
    get_t_list(conn, coacat_id_tup, start_date, end_date)
    t_to_bs(conn, coacat_id_tup, start_date, end_date)
    
