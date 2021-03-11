'''This function is allow python code talk with  pgAdmin4 inventoryManagement
database '''

import psycopg2
from psycopg2 import Error


def get_connection():

    connection = psycopg2.connect(user="joy2020",
                                  password="Dan",
                                  host="localhost",
                                  port="5432",
                                  database="ocean_stream")
    connection.autocommit = False
    return connection


if __name__ == '__main__':
    try:
        conn = get_connection()
        cursor = conn.cursor()

    except (Exception, psycopg2.Error) as error:
        print("Error while creating PostgreSQL table", error)

    finally:
        # closing database connection.
        if (conn):
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")
