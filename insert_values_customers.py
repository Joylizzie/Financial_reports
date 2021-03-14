import os
import csv
import random

import psycopg2

from generate_cust_id import customer_ids, address_line1s, citys
import make_random_data

random.seed(5)

def _generate_phone_num():
    pass

'''import the functions in file generate_cust_id.py to create customers.csv.'''

def generate_customer_tuples(n, data_file):
    customer_ids_lst = list(customer_ids(n))
    customer_name_lst = [x + ' Ltd.' for x in customer_ids_lst] #customer_name is customer_id + Ltd.
    address_lst = list(address_line1s(n))
    city_lst = citys(data_file, n) 
    cities_list = make_random_data.make_random_cities(path = 'data/wash_cities.csv', num = n)
    customer_surnames = make_random_data.make_random_surnames(path = 'data/surnames.csv', num = n)
    customer_first_names = make_random_data.make_random_first_names(path = 'data/first_names.csv', num = n)
    phone_nums = make_random_data.make_phone_numbers(num = n)
    street_addresses = make_random_data.make_street_address(path = 'data/street_names.csv', num = n)
    emails = make_random_data.make_random_email_domains(path = 'data/emails.csv', num = n)
    return [('US001',
            customer_ids_lst[k], 
            customer_surnames[k] + ',' + customer_first_names[k][0],
            1, 
            1,
            '{n} {s}'.format(n = random.randrange(1,100), s = street_addresses[k]),
            cities_list[k][0],
            'WA',
            'USA',
            cities_list[k][1],
            '{z}-{n}'.format(z = cities_list[k][2], n = phone_nums[k]),
            '{f}_{l}@{d}'.format(
                f = customer_first_names[k][0].lower()[0:5], 
                l = customer_surnames[k].lower()[0:7],
                d = emails[k],
                )) for k in range(n)]

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

