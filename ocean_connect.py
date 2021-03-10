import os
import csv
import tempfile

import psycopg2


def _get_conn(pw):
    conn = psycopg2.connect(
        host="localhost",
        database="ocean_stream",
        user="financial_user",
        password=pw)
    return conn

def test_conn(pw):
    conn = _get_conn(pw)
    cur = conn.cursor()
    cur.execute('SELECT version()')

def main(pw):
    conn = _get_conn(pw)
    sql = """select company_code, company_name from companies"""
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
        for i in rows:
            print(i)

def create_csv(pw):
    conn = _get_conn(pw)
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
    pw = os.environ['POSTGRES_PW']
    #test_conn(pw)
    #main(pw)
    create_csv(pw)
