import os
import psycopg2


def _get_conn(pw,user_str):
    conn = psycopg2.connect(host="localhost",
                            database="pacific",
                            user= user_str,
                            password=pw)
    conn.autocommit = False
    return conn

         
# define 'do_work' function for users using this module
def run_program(do_work, parms):
    pw = os.environ['POSTGRES_PW']
    user = os.environ['POSTGRES_USER']
    conn = _get_conn(pw,user)
 
    try:
        do_work(conn, **parms)

    except (Exception, psycopg2.Error) as error:
        print("Error while executing progamme", error)

    finally:
        # closing database connection.
        if (conn):
            conn.close()
            print("PostgreSQL connection is closed")


if __name__ == '__main__':
    pw = os.environ['POSTGRES_PW']
 
