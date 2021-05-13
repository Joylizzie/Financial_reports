import os
import psycopg2
import datetime
import csv
import itertools


# Don't repeat myself - combine read sql queries from one connection.


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
        #print(bs_t)
    conn.commit()
    
    # put the query results to dictionary 
    t_dict = {}
    for row in bs_t:
        t_dict[row[0]] = row[1]
    print(t_dict)
    
    # write the query results to csv file
    with open(os.path.join('reporting_results', '3_bs_t_list.csv'), 'w') as write_obj:
        csv_writer = csv.writer(write_obj)
        for item in t:
            csv_writer.writerow(item)
    
    # return the query results for functions   
    return t_dict 
    
    
def t_to_bs(conn, end_date):    
 
    t_dict = get_t_list(conn)                    
    balance_at = end_date.strftime("%m") + "_" + end_date.strftime("%Y")
    with open(os.path.join('reporting_results','bs_template.csv'), 'r') as read_obj, \
            open(os.path.join('reporting_results', f'3_bs_{balance_at}.csv'),'w', newline='') as write_obj:
        bs_reader = csv.reader(read_obj, delimiter=',')
        bs_writer = csv.writer(write_obj)
        
        for row in bs_reader:
            if row[2] in t_dict.keys():
                row.append(t_dict.get(row[2]))
                bs_writer.writerow(row)           
            else:
                bs_writer.writerow(row)
                
                    
    print('bs done writing')
    
        
if __name__ == '__main__':
    # parameters:
    db = 'ocean_stream'
    pw = os.environ['POSTGRES_PW']
    user_str = os.environ['POSTGRES_USER']
    conn = _get_conn(pw, user_str)
    end_date = datetime.date(2021,3,31)
    
    # call functions
    #get_t_list(conn)       
    t_to_bs(conn, end_date)   
