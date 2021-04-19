import os
import string
import random
import csv

random.seed(5)

# generate 3 random uppercase letters
def random_uc(d):
    return ''.join([random.choice(string.ascii_uppercase) for _ in range(d)])

# generate 3 random digits
def random_dg(d):
    return ''.join([random.choice(string.digits) for _ in range(d)])

# generate random customer id, with length=6, first 3 uppercase letters, followed by 3 digits
def customer_id():
    return random_uc(3) + random_dg(3)

# generate given number of customer ids
def customer_ids(n):
    count = 0
    customer_ids_set = set()
    while count < n:
        new_customer_id = customer_id()
        if new_customer_id in customer_ids_set:
            continue
        else:
            customer_ids_set.add(new_customer_id)
            count += 1      
    return customer_ids_set 
    

def to_csv(n, out_file):
    cust_ids_lst = list(customer_ids(n))
    company_code = 'US001'
    with open(os.path.join('data', out_file), 'w') as cust_ids:
        csv_writer = csv.writer(cust_ids)
        csv_writer.writerow(header)
        for cust_id in cust_ids_lst:
            csv_writer.writerow([company_code, cust_id]) # [] must be around cust_id, otherwise it will be each character separated by coma. 
    print('Done writing') 

    
if __name__ == '__main__':
    n = 30000
    out_file = '/home/lizhi/projects/joylizzie/Financial_reports/data/customer_ids.csv'
    header = ['company_code', 'customer_id']
    to_csv(n, out_file)
    

