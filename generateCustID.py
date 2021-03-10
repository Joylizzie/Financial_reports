import string
import random
import pandas as pd

# generate 3 random uppercase letters
def randomUc(d):
    return ''.join([random.choice(string.ascii_uppercase) for _ in range(d)])

# generate 3 random digits
def randomDg(d):
    return ''.join([random.choice(string.digits) for _ in range(d)])

# generate random customer id, with length=6, first 3 uppercase letters, followed by 3 digits
def customer_id():
    return randomUc(3) + randomDg(3)

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

# generate random address with given format of address
def address_line1(n):
    direction = ['SE','NE', 'SW', 'NW']
    randomd = random.choice(direction)
    i = 1
    while i < n+1:
        print(f'{i} {i}th street {randomd}')
        i += 1

# randomly select a city from a given list(here is cities in Washington state)            
def citys(datafile):
    cities = pd.read_csv(datafile)
    return random.choice(cities["County"].unique())

    
print(customer_id(),end='\n\n')

print(customer_ids(10), end='\n\n')

address_line1(9)

datafile = '/home/lizhi/projects/joylizzie/Financial_reports/list-cities-washington-198j.csv'
print(citys(datafile))
