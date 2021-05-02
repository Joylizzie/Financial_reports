import os
import psycopg2
import pandas as pd
import numpy as np
import datetime
import csv


# Get connection
def _get_conn(pw, user_str):
    conn = psycopg2.connect(host="localhost",
                            database = db,
                            user= user_str,
                            password=pw)
    conn.autocommit = False
    return conn
    
#def get_t_list_a(conn, bs_pl_index_tup):
def get_t_list_a(conn):
    # read sql view from a file
    sql_file = open('reports/t_list_simple_2_1.sql', 'r')
    sql = sql_file.read()
    
    # connect with db to excute the query
    with conn.cursor() as curs:
        bs_pl_index_tup = (1,2,3,4,5,6,6,7,8,10)
        curs.execute(sql, {'bs_pl_index_tup': bs_pl_index_tup})
        bs_ca_t_list = curs.fetchall()
    conn.commit()
    
    # put the query results to dictionary 
    t_dict = {}
    for row in bs_ca_t_list:
        t_dict[row[0]] = row[1]
    print(t_dict)
    
#    # write the query results to csv file
#    with open(os.path.join('in_progress', '2_bs_ca_t_list.csv'), 'w') as write_obj:
#        csv_writer = csv.writer(write_obj)
#        for item in bs_ca_t_list:
#            csv_writer.writerow(item)
    
    # return the query results for functions   
    return t_dict 
    
    
#def get_t_list_ls(conn, bs_pl_index_tup):
def get_t_list_ls(conn):
    # read sql view from a file
    sql_file = open('reports/t_list_simple_2_2.sql', 'r')
    sql = sql_file.read()
    
    # connect with db to excute the query
    with conn.cursor() as curs:
        bs_pl_index_tup = (20,21,22,23,29, 30,35,40,41)  
        curs.execute(sql, {'bs_pl_index_tup': bs_pl_index_tup})
        bs_ca_t_list = curs.fetchall()
    conn.commit()
    
    # put the query results to dictionary 
    t_dict = {}
    for row in bs_ca_t_list:
        t_dict[row[0]] = row[1]
    print(t_dict)
    
#    # write the query results to csv file
#    with open(os.path.join('in_progress', '2_bs_ca_t_list.csv'), 'w') as write_obj:
#        csv_writer = csv.writer(write_obj)
#        for item in bs_ca_t_list:
#            csv_writer.writerow(item)
    
    # return the query results for functions   
    return t_dict 
    
    
#def t_to_bs(conn, bs_pl_index_tup, end_date):
def t_to_bs(conn, end_date):    
    t_dict_a = get_t_list_a(conn)
    t_dict_ls = get_t_list_ls(conn)
                    
    balance_at = end_date.strftime("%m") + "_" + end_date.strftime("%Y")
    with open(os.path.join('reporting_results','bs_template.csv'), 'r') as read_obj, \
            open(os.path.join('reporting_results', f'2_bs_{balance_at}.csv'),'w', newline='') as write_obj:
        bs_reader = csv.reader(read_obj, delimiter=',')
        bs_writer = csv.writer(write_obj)
        
        for row in bs_reader:
            if row[2] in t_dict_a.keys():
                row.append(t_dict_a.get(row[2]))
                bs_writer.writerow(row)
            elif row[2] in t_dict_ls.keys():
                row.append(t_dict_ls.get(row[2]))
                bs_writer.writerow(row)            
            else:
                bs_writer.writerow(row)
                
#        for row in bs_reader:                            
#            if row[2] in t_dict_ls.keys():
#                row.append(t_dict_ls.get(row[2]))
#                bs_writer.writerow(row)
#            else:
#                bs_writer.writerow(row)
                    
    print('bs done writing')
    
        
if __name__ == '__main__':
    # parameters:
    db = 'ocean_stream'
    pw = os.environ['POSTGRES_PW']
    user_str = os.environ['POSTGRES_USER']
    conn = _get_conn(pw, user_str)
    #coacat_id_tup = (1,)
    #sub_coacat_id_tup = (1,)
    #bs_pl_index_tup = (1,2,3,4,5,6,7,8,9,10)    
    #start_date = datetime.date(2021,3,1)
    end_date = datetime.date(2021,3,31)
    # call functions
    get_t_list_a(conn) 
    get_t_list_ls(conn)  
    t_to_bs(conn, end_date)   
