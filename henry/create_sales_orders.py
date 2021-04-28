import csv
import random
import datetime

random.seed(5)


def random_date(start_date, end_date):
    # calculate time between start_date and end_date, then convert the time to days    
    days_between_dates = (end_date - start_date).days
    # select random day in above days
    random_number_of_days = random.randrange(days_between_dates) 
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date

def make_sales_orders(path, num, start_date, end_date):
    customer_ids = []
    with open(path, 'r') as read_obj:
        csv_reader = csv.DictReader(read_obj)
        for i in csv_reader:
            customer_ids.append(i['customer_id'])
    with open('data/sales_orders.csv', 'w') as write_obj:
        csv_writer = csv.writer(write_obj)
        for i in range(num):
            csv_writer.writerow(['US001', i+ 1, random_date(start_date, end_date), 
                random.choice(customer_ids)])

if __name__ == '__main__':
    start_date = datetime.date(2021, 3, 1)
    end_date = datetime.date(2021, 3, 31)
    make_sales_orders(path = 'data/customers.csv', num = 10000, start_date = start_date, 
            end_date = end_date)

