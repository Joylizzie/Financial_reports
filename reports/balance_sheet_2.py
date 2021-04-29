import os
import psycopg2
import pandas as pd
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


# write a blank balance sheet    
def blank_bs(conn, coacat_id_tup, start_date, end_date):
    
    with open(os.path.join('reporting_results', 'blank_bs.csv'), 'w') as bbs:
        # Equation: Assets = shareholder's equity + Liabilities
        # Head part of balance sheet
        name = 'Ocean Stream' 
        bbs_writer = csv.writer(bbs)   
        bbs_writer.writerow([f'{name}','', '', ''])
        bbs_writer.writerow(['Balance Sheet', '', '', ''])
        bbs_writer.writerow(['USD $', '', '', ''])
        bbs_writer.writerow(['','','',f'as of {end_date}'.rjust(15)])  
        
        # Body of balance sheet
        # Assets    
        bbs_writer.writerow(['Assets','','',''])
        bbs_writer.writerow(['','Current assets','',''])
        bbs_writer.writerow(['','','Cash and cash equivalent',''])
        bbs_writer.writerow(['','','Inventory',''])
        bbs_writer.writerow(['','','Account receivables',''])
        bbs_writer.writerow(['','','Prepaid expenses',''])        
        #bbs_writer.writerow(['','','','',''])        
        bbs_writer.writerow(['', 'Total current assets','',''])
        #bbs_writer.writerow(['','','','',''])
        bbs_writer.writerow(['','','Property and Equipment',''])
        bbs_writer.writerow(['', '', '- Accumulated depreciation',''])
        bbs_writer.writerow(['','','Other assets',''])        
        bbs_writer.writerow(['Total Assets','','',''])
        #bbs_writer.writerow(['','','',''])
        # Liabilities
        bbs_writer.writerow(['Liabilities','','',''])
        bbs_writer.writerow(['','Current liabilities','',''])
        bbs_writer.writerow(['','','Accounts Payable',''])
        bbs_writer.writerow(['','','Accrued expenses',''])
        bbs_writer.writerow(['','','Unearned revenue',''])       
        bbs_writer.writerow(['','Total current liabilities','',''])
        bbs_writer.writerow(['','','','',''])
        bbs_writer.writerow(['Total Liabilities','','',''])
        #bbs_writer.writerow(['','','','',''])
        # shareholders equity
        bbs_writer.writerow(['Shareholder\'s Equity','','','']) 
        bbs_writer.writerow(['','','Equity Capital','']) 
        bbs_writer.writerow(['','','Retained Earnings',''])
        bbs_writer.writerow(['Total Shareholder\'s Equity','','',''])
        #bbs_writer.writerow(['','','',''])
        bbs_writer.writerow(['Total Liabilities & Total Shareholder\'s Equity','','',''])     
 
        print('blank balance sheet csv done writing')  

# Get (debit - credit) amount by category with rollup during start and end date
def get_t_list(conn, coacat_id_tup, start_date, end_date):
    sql_file = open('reports/t_list_bs.sql', 'r')
    sql = sql_file.read()
    #print(sql)
    with conn.cursor() as curs:
        curs.execute(sql, {'start_date':start_date, 'end_date':end_date, 'coacat_id_tup':coacat_id_tup})  #cursor closed after the execute action
        t_list_w_None = curs.fetchall()
    #print(t_list_w_None)
    conn.commit()
    # write to csv file 
    with open(os.path.join('reporting_results', 'bs_t_list_None.csv'), 'w') as write_obj:
        csv_writer = csv.writer(write_obj)
        for item in t_list_w_None:
            csv_writer.writerow(item)
    #print('t_list_None done writing')
    return t_list_w_None
           
# convert None in t_list_None to ''
def conv_None(conn, coacat_id_tup, start_date, end_date):
    t_list_w_None = get_t_list(conn, coacat_id_tup, start_date, end_date)
    #print(type(t_list_w_None))    
    t_list = []
    for tup in t_list_w_None:
        tup = tuple('' if v is None else v for v in tup)
        t_list.append(tup)
  
    #print(t_list)
    return t_list          

def read_write_bs(conn, coacat_id_tup, start_date, end_date):
    # a list of tuples with string, empty and numbers
    t_list = conv_None(conn, coacat_id_tup, start_date, end_date)
    print(t_list)
    print('-----------')
    with open('reporting_results/blank_bs.csv', 'r') as bs:
        bs_reader = csv.reader(bs, delimiter=',')
        print(list(bs_reader))
        for row in bs_reader:    
            # read the rows without numbers to be added and append them to the list above          
            if row[0] in ['Ocean Stream','Balance Sheet', 'USD $', 'Assets',  'Liabilities', 'Shareholder\'s Equity']:
                new_row = [row[0], '', '','']
                new_rows_list.append(new_row)
            if row[1] in ['Current assets', 'Current liabilities']:
                    new_row = ['', row[1], '','']
                    new_rows_list.append(new_row)       
            if row[3] is not None or '':
                new_row = ['', '', '',row[3]]
                new_rows_list.append(new_row)
            # read the rows with numbers to be added and append them to the list above            
            for tup in t_list:             
                if row[1] in ['Total current assets' , 'Total current liabilities']:
                    new_row = ['', row[1], '',tup[3]]
                    new_rows_list.append(new_row)                           
                if row[0] in ['Total Assets','Total Liabilities', 'Total Shareholder\'s Equity', 'Total Liabilities & Total Shareholder\'s Equity']:
                    new_row = [row[0], '', '',tup[3]]
                    new_rows_list.append(new_row)                                   
                if row[0] is '' and row[1] is '' and row[2] == tup[2]:
                    new_row = ['', '', tup[2],tup[3]]
                    new_rows_list.append(new_row)
            print(new_rows_list)

            # write above new_rows_list to a new file
            balance_at = end_date.strftime("%m") + "_" + end_date.strftime("%Y")
            with open(os.path.join('reporting_results', f'bs_{balance_at}.csv'), 'w') as bs:
                bs_writer = csv.writer(bs)
                bs_writer.writerows(new_rows_list)
                print('bs done writing')
        
if __name__ == '__main__':
    # parameters:
    db = 'ocean_stream'
    pw = os.environ['POSTGRES_PW']
    user_str = os.environ['POSTGRES_USER']
    conn = _get_conn(pw, user_str)
    coacat_id_tup = (1,2,3)
    start_date = datetime.date(2021,3,1)
    end_date = datetime.date(2021,3,31)
    # call functions
    #get_t_list(conn, coacat_id_tup, start_date, end_date)
    #blank_bs(conn, coacat_id_tup, start_date, end_date)
    #conv_None(conn, coacat_id_tup, start_date, end_date)
    read_write_bs(conn, coacat_id_tup, start_date, end_date)
