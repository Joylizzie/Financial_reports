import os
import csv
import random


from generate_cust_id import customer_ids
import make_random_data

random.seed(5)


def generate_customer_names(n, data_file):
    business_type = [1,2]
    customer_ids_lst = list(customer_ids(n))
    customer_surnames = make_random_data.make_random_surnames(path = 'data/surnames.csv', num = n)
    customer_first_names = make_random_data.make_random_first_names(path = 'data/first_names.csv', num = n)
    return [('US001',
            customer_ids_lst[k], 
            random.choice(business_type),
            customer_surnames[k] + ',' + customer_first_names[k][0],
            102001,1) for k in range(n)]


def create_csv(n, data_file, tup_gen, header,out_file):
    tups = tup_gen(n, data_file)
    with open(os.path.join('data', out_file), 'w') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(header)
        for i in range(n):
            csv_writer.writerow(tups[i])
        print('Done writing.')    
    

if __name__ == '__main__':
    
    create_csv(
            n = 30000, 
            data_file = '/home/lizhi/projects/lizziezh/auto_FR/data/list-cities-washington-198j.csv',
            out_file = '/home/lizhi/projects/lizziezh/auto_FR/data/customer_names.csv',
            tup_gen = generate_customer_names,
            header = ['company_code','customer_id', 'business_type_id','customer_name', 'general_ledger_number', 'currency_id'])


