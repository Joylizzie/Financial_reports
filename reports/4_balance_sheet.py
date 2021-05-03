import os
import psycopg2
import pandas as pd
import numpy as np
import datetime
import csv
import itertools


# Get connection
def _get_conn(pw, user_str):
    conn = psycopg2.connect(host="localhost",
                            database = db,
                            user= user_str,
                            password=pw)
    conn.autocommit = False
    return conn
    
    
# get tranction list based on bs_pl_index
def get_t_list(conn):
    
    # read sql view from different files
    # t_list_simple_2_1.sql: debit side numbers showing as positive numbers
    # t_list_simple_2_1.sql: credit side numbers showing as positive numbers
    
    # connect with db to excute the queries
    with conn.cursor() as curs:
        t = []
        bs_pl_index_tup_1 = (1,2,3,4,5,6,6,7,8,10)
        bs_pl_index_tup_2 = (20,21,22,23,29, 30,35,40,41)        

        curs.execute(open('reports/t_list_simple_2_1.sql','r').read(), {'bs_pl_index_tup': bs_pl_index_tup_1})
        t.append(curs.fetchall())
        curs.execute(open('reports/t_list_simple_2_2.sql','r').read(), {'bs_pl_index_tup': bs_pl_index_tup_2})
        t.append(curs.fetchall())
 
        # flat t to a list of tuples
        bs_t = list(itertools.chain(*t))
        print(bs_t)
    conn.commit()
    
    # put the query results to dictionary 
    t_dict = {}
    for row in bs_t:
        t_dict[row[0]] = row[1]
    #print(t_dict)
    
    # write to csv file 
    with open(os.path.join('reporting_results', '4_bs_t_list.csv'), 'w') as write_obj:
        csv_writer = csv.writer(write_obj)
        for item in bs_t:
            csv_writer.writerow(item)

    print('4_bs_t_list done writing')
    return t_dict
    
# write the numbers in above dictionary values into predefined balance sheet
def t_to_bs(conn, end_date):    
 
    t_dict = get_t_list(conn)                    
    balance_at = end_date.strftime("%m") + "_" + end_date.strftime("%Y")
    with open(os.path.join('reporting_results','bs_template.csv'), 'r') as read_obj, \
            open(os.path.join('reporting_results', f'4_bs_{balance_at}.csv'),'w', newline='') as write_obj:
        bs_reader = csv.reader(read_obj, delimiter=',')
        bs_writer = csv.writer(write_obj)
        
        for row in bs_reader:
            if row[2] in t_dict.keys():
                row.append(float(t_dict.get(row[2])))
                bs_writer.writerow(row)
            else:
                bs_writer.writerow([row[0], row[1], row[2], ''])
                 
        print(f'4_bs_{balance_at}.csv done writing')


# get the sum amount by category for above balance sheet    
def sum_cat(conn, end_date):

    balance_at = end_date.strftime("%m") + "_" + end_date.strftime("%Y")
    with open(os.path.join('reporting_results',f'4_bs_{balance_at}.csv'), 'r') as read_obj, \
            open(os.path.join('reporting_results', f'4_sum_bs_{balance_at}.csv'),'w', newline='') as write_obj:
        bs_reader = csv.reader(read_obj, delimiter=',')
        bs_writer = csv.writer(write_obj)
        
        sum_ca = 0
        sum_nca = 0
        sum_a = 0
        sum_cl = 0
        sum_l = 0
        sum_s = 0
        sum_ls = 0 
                   
        for i, row in enumerate(bs_reader):
            # write head part of Balance sheet
            if i <= 2:
                bs_writer.writerow(row)
            # balance at the date    
            if i == 3:
                row = [row[0], row[1], row[2], 'as of 2021-03-31']            
                bs_writer.writerow(row)            
            # current assets    
            if 3 < i <= 10:
                row = [row[0], row[1], row[2], (float(row[3]) if row[3] != '' else row[3])]                
                bs_writer.writerow(row)
                if row[3] != '':                
                    sum_ca = sum_ca + row[3]
            # sub total of current assets       
            if i == 11:
                row = [row[0], row[1], row[2], sum_ca]
                bs_writer.writerow(row) 
                  
            if 12<= i <= 17:
                row = [row[0], row[1], row[2], (float(row[3]) if row[3] != '' else row[3])]                
                bs_writer.writerow(row)
                if row[3] != '':                
                    sum_nca = sum_nca + row[3]
            # sub total of Noncurrent assets                        
            if i == 18:
                row = [row[0], row[1], row[2], sum_nca]
                bs_writer.writerow(row)
                sum_a = sum_ca + sum_nca                 
            # Total of Assets 
            if i == 19:                
                row = [row[0], row[1], row[2], sum_a]
                bs_writer.writerow(row)                 
            # current liabilities    
            if 20 <= i <= 26:
                row = [row[0], row[1], row[2], (float(row[3]) if row[3] != '' else row[3])]                
                bs_writer.writerow(row)
                if row[3] != '':                
                    sum_cl = sum_cl + row[3]
            # sub total of current liabilities                                         
            if i == 27:
                row = [row[0], row[1], row[2], sum_cl]
                bs_writer.writerow(row) 
            # shareholder's equity    
            if 28 <= i <= 33:
                row = [row[0], row[1], row[2], (float(row[3]) if row[3] != '' else row[3])]                
                bs_writer.writerow(row)
                if row[3] != '':                
                    sum_s = sum_s + row[3] 
                    sum_ls = sum_cl + sum_s
            # sub total of shareholder's equity        
            if i == 34:
                row = [row[0], row[1], row[2], sum_s]
                bs_writer.writerow(row)      
            # blank line    
            if i == 35:
                bs_writer.writerow(row) 
            # Total of liabilities and shareholer's equity 
            if i == 36:
                row = [row[0], row[1], row[2], sum_ls]            
                bs_writer.writerow(row)
        # check if Total asset equial Total of liabilities and shareholer's equity. If not equial, print a message for correction
        if sum_a != sum_ls:
            row = ['Check!!', 'Balance Sheet', 'isn\'t balanced','check and correct!']               
            bs_writer.writerow(row)
                    

if __name__ == '__main__':
    # parameters:
    db = 'ocean_stream'
    pw = os.environ['POSTGRES_PW']
    user_str = os.environ['POSTGRES_USER']
    conn = _get_conn(pw, user_str)
    end_date = datetime.date(2021,3,31)

    # call functions
    get_t_list(conn)       
    t_to_bs(conn, end_date) 
    sum_cat(conn, end_date)   
