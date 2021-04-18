import os
import pandas as pd
import csv
import random

from generate_cust_id import customer_ids
from generate_cust_names import  generate_customer_names, create_csv 
import make_random_data

random.seed(5)


def generate_customer_addresses(data_file):
    df = pd.read_csv('data/customer_names.csv', usecols=['customer_id'])
    n = len(df['customer_id'])
    customer_ids_lst = df['customer_id'].values.tolist()
    cities_list = make_random_data.make_random_cities(path = 'data/wash_cities.csv', num = n)
    customer_surnames = make_random_data.make_random_surnames(path = 'data/surnames.csv', num = n)
    customer_first_names = make_random_data.make_random_first_names(path = 'data/first_names.csv', num = n)
    phone_nums = make_random_data.make_phone_numbers(num = n)
    street_addresses = make_random_data.make_street_address(path = 'data/street_names.csv', num = n)
    emails = make_random_data.make_random_email_domains(path = 'data/emails.csv', num = n)
    # return a list of tuples for customer_addresses table
    return [('US001',# company_code
            customer_ids_lst[k], # customer_id,
            '{n} {s}'.format(n = random.randrange(1,100), s = street_addresses[k]),# address_line1
            cities_list[k][0],# city
            'WA',# state
            'USA', # country
            cities_list[k][1], # postcode
            '{z}-{n}'.format(z = cities_list[k][2], n = phone_nums[k]),# phone_number
            '{l}@{d}'.format(
                            f = customer_first_names[k][0].lower()[0:5], 
                            l = customer_surnames[k].lower()[0:7],
                            d = emails[k]) # email_address
              ) for k in range(n)
             ]

# write above customer addresses into csv file then use bash to upload into database
def create_csv(data_file, tup_gen, header,out_file):
    tups = tup_gen(data_file)
    with open(os.path.join('data', out_file), 'w') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(header)
        for i in range(len(tups)):
            csv_writer.writerow(tups[i])
    print('Done writing')
      

if __name__ == '__main__':
    create_csv(data_file = '/home/lizhi/projects/joylizzie/Financial_reports/data/list-cities-washington-198j.csv',
       out_file = '/home/lizhi/projects/joylizzie/Financial_reports/data/customer_addresses.csv',
       tup_gen = generate_customer_addresses,
       header = ['company_code','customer_id', 'address_line1','city','state','country','postcode','phone_number','email_address'])
 
