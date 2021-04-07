import os
import datetime
import psycopg2
from psyco_conn_ocean_pw_pc import _get_conn, run_program
from random_date import randomdate
#from retrieve_data_pw import retrieve_data


def generate_je_id(conn):
    #retrieve je_id in the database
    #conn = _get_conn(pw,user_str)
    sql_str = """select je_id+1 from journal_entry where company_code='US001'
             order by je_id desc limit 1
             """
    
    with conn.cursor() as curs:
        curs.execute(sql_str)  #cursor closed after the execute action
        largest_id = curs.fetchall()# if the data is large, then use fetchone or fetchmany(), loop through
    return [('US001', largest_id[0])]

# insert the generated value tuples into database
def insert_values_tuples(conn, sql_insert):
    tups = generate_je_id(conn)
    with conn.cursor() as curs:
        curs.execute(sql_insert, tups[0]) #cursor close after the execute
    conn.commit()#commit the connection to confirm the insertion

def do_work(conn, sql_insert):
    cur = conn.cursor()
    insert_values_tuples(conn, sql_insert)


if __name__ == '__main__':    

    # call the function with parameters to see if the function works# 
    sql_insert = '''insert into journal_entry (company_code, je_id)
                    VALUES(%s,%s)'''
    pw = os.environ['POSTGRES_PW']
    user_str = os.environ['POSTGRES_USER']
    parms = {'sql_insert':sql_insert}

    run_program(do_work, parms)


