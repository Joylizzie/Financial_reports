import os
import csv
import tempfile

import psycopg2

def get_conn(str_user):
    conn = psycopg2.connect(
        host="localhost",
        database="ocean_stream",
        user=str_user
        )
    return conn

def test_conn(pw):
    conn = _get_conn(pw)
    cur = conn.cursor()
    cur.execute('SELECT version()')

def main():
    conn = _get_conn()
    sql = """select * from area_code limit 10"""
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
        for i in rows:
            print(i)

def create_csv():
    conn = _get_conn()
    sql  = """ create table if not exists test_csv(
    name varchar(10),
    num integer
    );
    """
    with conn.cursor() as cur:
        cur.execute('drop table if exists test_csv')
        cur.execute(sql)
    conn.commit()
    # make csv
    fh, path = tempfile.mkstemp()
    with conn.cursor() as cur:
        with open(path, 'w') as write_obj:
            csv_writer = csv.writer(write_obj)
            row1 = ['name1', 1]
            csv_writer.writerow(row1)
        with open(path, 'r') as read_obj:
            cur.copy_from(read_obj, 'test_csv', sep=',')

    os.close(fh)
    os.remove(path)
    with conn.cursor() as cur:
        cur.execute('select * from test_csv')
        for i in cur.fetchall():
            print(i)
        cur.execute('drop table test_csv')

if __name__ == '__main__':
    #pw = os.environ['POSTGRES_PW']
    #test_conn(pw)
    #main(pw)
    # user="financial_user",
    # password=pw
    create_csv()
