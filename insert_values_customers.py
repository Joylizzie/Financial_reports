import os
import csv

import psycopg2
from generate_cust_id import customer_ids, address_line1s, citys

'''import the functions in  file generate_cust_id.py to create customers.csv.'''

def generate_customer_tuples(n, data_file):
    customer_ids_lst = list(customer_ids(n))
    customer_name_lst = [x + ' Ltd.' for x in customer_ids_lst] #customer_name is customer_id + Ltd.
    address_lst = list(address_line1s(n))
    city_lst = citys(data_file, n) 
    return [('US001',
            customer_ids_lst[k], 
            customer_name_lst[k],
            1, 
            1,
            address_lst[k],
            city_lst[k],
            'WA',
            'USA',
            '98004',
            '999-999-9999',
            'ab@gmail.com') for k in range(n)]

def create_csv(n, data_file, out_file):
    tups = generate_customer_tuples(n, data_file)
    with open(os.path.join('data', out_file), 'w') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(['company_code','customer_id',
            'customer_name', 'general_ledger_number', 'currency_id','address_line1','city','state','country',
                'postcode','phone_number','email_address'])
        for i in range(n):
            csv_writer.writerow(tups[i])
    

if __name__ == '__main__':
    create_csv(n = 10000, 
            data_file = 'list-cities-washington-198j.csv', out_file = 'customers.csv')

