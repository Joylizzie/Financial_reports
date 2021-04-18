import os
import pandas as pd
import csv
import random


from generate_cust_id import customer_ids
import make_random_data

random.seed(5)


def generate_customer_names(data_file):
    business_type = [1,2]
    df = pd.read_csv('data/customer_ids.csv', usecols=['customer_id'])
    customer_ids_lst = df['customer_id'].values.tolist()
    n = len(customer_ids_lst)
    customer_surnames = make_random_data.make_random_surnames(path = 'data/surnames.csv', num = n)
    customer_first_names = make_random_data.make_random_first_names(path = 'data/first_names.csv', num = n)
    return [('US001',
            customer_ids_lst[k], 
            random.choice(business_type),
            customer_surnames[k] + ',' + customer_first_names[k][0],
            102001,1) for k in range(n)]


def create_csv(data_file, tup_gen, header,out_file):
    tups = tup_gen(data_file)
    with open(os.path.join('data', out_file), 'w') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(header)
        for i in range(len(tups)):
            csv_writer.writerow(tups[i])
        print('Done writing.')    
    

if __name__ == '__main__':
    
    create_csv(data_file = '/home/lizhi/projects/joylizzie/Financial_reports/data/list-cities-washington-198j.csv',
            out_file = '/home/lizhi/projects/joylizzie/Financial_reports/data/customer_names.csv',
            tup_gen = generate_customer_names,
            header = ['company_code','customer_id', 'business_type_id','customer_name', 'general_ledger_number', 'currency_id'])


