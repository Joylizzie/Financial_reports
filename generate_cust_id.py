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
def address_line1s(n):
    sn = ['S','N']
    ew = ['E', 'W']
    count = 0  
    address_set = set() 
    while count < n:
        randomd = random.choice(sn) + random.choice(ew)
        new_address = f'{count} {count}th street {randomd}'
        if new_address in address_set:
            continue
        else:
            address_set.add(new_address) 
            count += 1
    return address_set
    

# randomly select a city from a given list(here is cities in Washington state)            
def citys(datafile,n):
    cities = pd.read_csv(datafile)
    t = [x for x in cities["County"].unique() if not pd.isna(x)]
    return [random.choice(t) for _ in range(n)]

'''   
print(customer_id(),end='\n\n')

print(customer_ids(10), end='\n\n')

print(address_line1s(19))

datafile = '/home/lizhi/projects/joylizzie/Financial_reports/list-cities-washington-198j.csv'
print(citys(datafile,19))
'''
