# This function is allowing python code talk with ocean_stream database in client pgAdmin4

import argparse # parsing command line arguments 
import psycopg2 # working with database
from psycopg2 import Error # database error catching


def get_connection(args): 
    conn = psycopg2.connect(host=args.host, 
                            port=args.port, 
                            database=args.database, 
                            user=args.user, 
                            password=args.password)   
    
    conn.autocommit = False
    return conn

def get_args():
    parser = argparse.ArgumentParser(description="Connects to a PostgreSQL server and performs some monitoring")
    parser.add_argument("password", help="The password of the PostgreSQL user")
    parser.add_argument("-ho","--host", help="The name of the host with the PostgreSQL Server Default:localhost", default="localhost")
    parser.add_argument("-p", "--port", help="The PostgreSQL Server port to connect to. Default:5432", type=int, default=5432)
    parser.add_argument("-u", "--user", help="The name of the PostgreSQL user you want to login as. Default:joy2020", default="joy2020")
    parser.add_argument("-d", "--database", help="The PostgreSQL database you want to connect to. Default:ocean_stream", default="ocean_stream")
    return parser.parse_args()

# define 'do_work' function for users using this module
def run_program(do_work, parms):
    args = get_args() # Get the command line arguments
    conn = get_connection(args)

    try:
        do_work(conn, **parms)

    except (Exception, psycopg2.Error) as error:
        print("Error while executing progamme", error)

    finally:
        # closing database connection.
        if (conn):
            conn.close()
            print("PostgreSQL connection is closed")


