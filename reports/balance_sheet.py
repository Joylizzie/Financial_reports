import os
import psycopg2
import pandas as pd
import datetime
import csv


# get connection
def _get_conn(pw, user_str):
    conn = psycopg2.connect(host="localhost",
                            database = db,
                            user= user_str,
                            password=pw)
    conn.autocommit = False
    return conn

# get newest chart_of_accounts to a dictionary as general_    
def get_gl(conn):
    sql = """select 
                bs_pl_cat, 
                general_ledger_number 
             from chart_of_accounts
             where company_code = 'US001'
              
          """
    with conn.cursor() as curs:
        curs.execute(sql)  #cursor closed after the execute action
        gl_list = curs.fetchall()
    conn.commit()
    gl_dict = {}
    for row in gl_list:
        gl_dict[row[0]] = row[1]
    return gl_dict


# get (debit - credit) amount during start and end date
def get_t_dict(conn, coacat_id_tup, start_date, end_date):
    sql_file = open('reports/t_list.sql', 'r')
    sql = sql_file.read()
    #print(sql)
    try:
        with conn.cursor() as curs:
            curs.execute(sql, {'start_date':start_date, 'end_date':end_date, 'coacat_id_tup':coacat_id_tup})  #cursor closed after the execute action
            t_list = curs.fetchall()
        conn.commit()
    finally:
        conn.close()
    return t_list
   
# write a blank balance sheet    
def blank_bs(conn, coacat_id_tup, start_date, end_date):
    #balance_at = end_date.strftime("%m") + "_" + end_date.strftime("%Y")  
    with open(os.path.join('reporting_results', f'blank_bs.csv'), 'w') as bbs:
        # Equation: Assets = shareholder's equity + Liabilities
        # Head part of balance sheet
        name = 'Ocean Stream' 
        bbs_writer = csv.writer(bbs)   
        bbs_writer.writerow([f'{name}','', '', ''])
        bbs_writer.writerow([f'Balance Sheet', '', '', ''])
        bbs_writer.writerow([f'USD $', '', '', ''])
        bbs_writer.writerow(['','','',f'as of {end_date}'.rjust(15)])  
        
        # Body of balance sheet
        # Assets    
        bbs_writer.writerow([f'Assets','','',''])
        bbs_writer.writerow(['',f'Current assets','',''])
        bbs_writer.writerow(['','',f'Cash and cash equivalent',0])
        bbs_writer.writerow(['','',f'Inventory',0])
        bbs_writer.writerow(['','',f'Account receivables',0])
        bbs_writer.writerow(['','',f'Prepaid expenses',0])        
        bbs_writer.writerow(['','','','',''])        
        bbs_writer.writerow(['','',f'Total current assets',0])
        bbs_writer.writerow(['','','','',''])
        bbs_writer.writerow(['','',f'Property and Equipment',0])
        bbs_writer.writerow(['', '', '- Accumulated depreciation',0])
        bbs_writer.writerow(['','','Other assets',0])        
        bbs_writer.writerow(['Total Assets','','',0])
        bbs_writer.writerow(['','','',''])
        # Liabilities
        bbs_writer.writerow([f'Liabilities','','',''])
        bbs_writer.writerow(['',f'Current liabilities','',''])
        bbs_writer.writerow(['','',f'Accounts Payable',0])
        bbs_writer.writerow(['','',f'Accured expenses',0])
        bbs_writer.writerow(['','',f'Unearned revenue',0])       
        bbs_writer.writerow(['',f'Total current liabilities',0,0])
        bbs_writer.writerow(['','','','',''])
        bbs_writer.writerow([f'Total Liabilities','','',0])
        bbs_writer.writerow(['','','','',''])
        # shareholders equity
        bbs_writer.writerow([f'Shareholder\'s Equity','','','']) 
        bbs_writer.writerow(['',f'Equity Capital','','']) 
        bbs_writer.writerow(['',f'Retained Earnings','',''])
        bbs_writer.writerow([f'Total Shareholder\'s Equity ','','',''])
        bbs_writer.writerow(['','','',''])
        bbs_writer.writerow([f'Total Liabilities & Total Shareholder\'s Equity','','',''])     
 
        print('blank balance sheet csv done writing')  
         

def read_write_bs(conn, coacat_id_tup, start_date, end_date):
    t_list = get_t_dict(conn, coacat_id_tup, start_date, end_date)
    print(t_list)
    with open('reporting_results/blank_bs.csv', 'r') as bs:
        bs_reader = csv.reader(bs, delimiter=',')
        new_rows_list = []
        for row in bs_reader:
            #print(row)
            #print(row[2])
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
            for tup in t_list:
                if tup[1] == row[2]:
                    new_row = [row[0],row[1],row[2], tup[1]]
                    new_rows_list.append(new_row)
#                if row[1] is not '':
#                    new_row = [row[1]]
#                    new_rows_list.append(new_row)                                         
#                if row[0] is '' and row[1] is '' and row[2] in dict_t.keys():
#                    new_row = [row[0], row[1], row[2],dict_t[row[2]]]
#                    new_rows_list.append(new_row)
        print(new_rows_list)
         
        # write to a new file
        balance_at = end_date.strftime("%m") + "_" + end_date.strftime("%Y")
        with open(os.path.join('reporting_results', f'bs_{balance_at}.csv'), 'w') as bs:
            bs_writer = csv.writer(bs)
            bs_writer.writerows(new_rows_list)
    #for (bs_pl_cat, amount) in t:
     #   bs_writer.writerow([bs_pl_cat, f'{amount:3,.2f}'])                    
    #for (coa_cat, sub_coa_cat, bs_pl_cat, amount) in t:
        #bs_writer.writerow([bs_pl_cat,gl_num,gl_name, f'{amount:3,.2f}'])           
        #bs_writer.writerow([coa_cat, sub_coa_cat, bs_pl_cat, f'{amount:3,.2f}'])        
   
if __name__ == '__main__':
    db = 'ocean_stream'
    pw = os.environ['POSTGRES_PW']
    user_str = os.environ['POSTGRES_USER']
    conn = _get_conn(pw, user_str)
    coacat_id_tup = (1,2,3,5,6)
    start_date = datetime.date(2021,3,1)
    end_date = datetime.date(2021,3,31)
    #get_gl(conn)
    #gl_to_dict(conn)
    #get_t_list(conn, coacat_id_tup, start_date, end_date)
    blank_bs(conn, coacat_id_tup, start_date, end_date)
    read_write_bs(conn, coacat_id_tup, start_date, end_date)
    #bs(conn, coacat_id_tup, start_date, end_date)
