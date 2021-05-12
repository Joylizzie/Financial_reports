import os
import psycopg2


def _get_conn(pw, user_str):
    conn = psycopg2.connect(host="localhost",
                            database = db,
                            user= user_str,
                            password=pw)
    conn.autocommit = False
    return conn

def generate_je_id(conn):
    sql_str = """ select nextval('journal_entry_je_id_seq')"""
    with conn.cursor() as curs:
        curs.execute(sql_str)  #cursor closed after the execute action
        (next_je_id) = curs.fetchone()# if the data is large, then use fetchone or fetchmany(), loop through
    return [('US001','JE', next_je_id)]

# insert the generated value tuples into database
def insert_je_id(conn):
    tups = generate_je_id(conn)
    sql_insert = '''insert into journal_entry (company_code, entry_type_id, je_id)
                    VALUES(%s,%s,%s)'''

    try:
        with conn.cursor() as curs:
            curs.execute(sql_insert, tups[0]) #cursor close after the execute
        conn.commit()#commit the connection to confirm the insertion
    except (Exception, psycopg2.Error) as error:
        print("Error while executing progamme", error)

    finally:
        # closing database connection.
        if (conn):
            conn.close()
            print("PostgreSQL connection is closed")                        
    

if __name__ == '__main__':  
    # call the function with parameters to see if the function works#
    db = 'ocean_stream' 
    pw = os.environ['POSTGRES_PW']
    user_str = os.environ['POSTGRES_USER']
    conn = _get_conn(pw, user_str)
    insert_je_id(conn)



