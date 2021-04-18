import os

import psycopg2

PW = os.environ['POSTGRES_PW']

conn = psycopg2.connect(
    host="localhost",
    database="test_conn",
    user="financial_user",
    password=PW)

sql = """select * from accounts"""
cur = conn.cursor()
cur.execute('SELECT version()')
rows = cur.fetchall()
for i in rows:
    print(i)
cur.execute(sql)
rows = cur.fetchall()
for i in rows:
    print(i)
