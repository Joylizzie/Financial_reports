import csv
import random
random.seed(5)


def _get_pop_first_names(path):
    total = 0
    with open(path, 'r') as read_obj:
        csv_reader = csv.DictReader(read_obj)
        for row in csv_reader:
            if row['occurence'] == None:
                continue
            pop = int(row['occurence'])

            total += pop
    return total

def _get_pop(path):
    total = 0
    with open(path, 'r') as read_obj:
        csv_reader = csv.DictReader(read_obj)
        for row in csv_reader:
            if row['population'] == None:
                continue
            pop = int(row['population'])

            total += pop
    return total

def _make_weighted(path, pop):
    final = []
    with open(path, 'r') as read_obj:
        csv_reader = csv.DictReader(read_obj)
        for row in csv_reader:
            if row['population'] == None:
                continue
            city_pop = int(row['population'])
            percent = city_pop/pop
            final.append((row['city'], row['zip_code'], row['area_code'], 
                percent))
    return final

def _make_weighted_first_names(path, pop):
    final = []
    with open(path, 'r') as read_obj:
        csv_reader = csv.DictReader(read_obj)
        for row in csv_reader:
            if row['occurence'] == None:
                continue
            name_pop = int(row['occurence'])
            percent = name_pop/pop
            final.append((row['name'], row['sex'], percent))
    return final


def make_random_cities(path, num):
    pop =  _get_pop(path)
    weighted_list = _make_weighted(path, pop)
    weights = [x[3] for x in weighted_list]
    cities_zips = [(x[0], x[1], x[2]) for x in weighted_list]
    random_cities = random.choices(cities_zips, k= num, weights=weights)
    return random_cities

def make_random_first_names(path, num):
    pop = _get_pop_first_names(path)
    weighted_list =  _make_weighted_first_names(path, pop)
    weights = [x[2] for x in weighted_list]
    first_names_sex = [(x[0], x[1]) for x in weighted_list]
    random_names = random.choices(first_names_sex, k= num, weights=weights)
    return random_names

def make_random_surnames(path, num):
    weighted_list = []
    names = []
    with open(path, 'r') as read_obj:
        csv_reader = csv.DictReader(read_obj)
        for row in csv_reader:
            weighted_list.append(float(row['frequency']))
            names.append(row['name'])
    random_names = random.choices(names, k= num, weights=weighted_list)
    return random_names

def make_phone_numbers(num):
    d = {}
    for i in range(num):
        while True:
            x = '{f}-{s}'.format(f = random.randrange(100, 999), 
                    s = random.randrange(1000, 9999)
                    )
            if not d.get(x):
                d[x] = True
                break
    l = sorted(d.keys())
    return random.choices(l, k= num)

def _make_weighted_street_names(path, pop):
    final = []
    with open(path, 'r') as read_obj:
        csv_reader = csv.DictReader(read_obj)
        for row in csv_reader:
            if row['occurence'] == None:
                continue
            name_pop = int(row['occurence'])
            percent = name_pop/pop
            final.append((row['name'], percent))
    return final

def make_street_address(path, num):
    pop = _get_pop_first_names(path)
    weighted_list =  _make_weighted_street_names(path, pop)
    weights = [x[1] for x in weighted_list]
    first_names_sex = [x[0] for x in weighted_list]
    random_names = random.choices(first_names_sex, k= num, weights=weights)
    return random_names

def make_random_email_domains(path, num):
    weighted_list = []
    names = []
    with open(path, 'r') as read_obj:
        csv_reader = csv.DictReader(read_obj)
        for row in csv_reader:
            weighted_list.append(float(row['frequency']))
            names.append(row['domain'])
    random_names = random.choices(names, k= num, weights=weighted_list)
    return random_names

if __name__ == '__main__':
    path = 'data/wash_cities.csv'
    city_list=make_random_cities(path, num = 1000)
    print(city_list[0:10])
    x = make_random_first_names(path = 'data/first_names.csv', num = 1000)
    print(x[0:10])
    x = make_random_surnames(path = 'data/surnames.csv', num = 1000)
    print(x[0:10])
    x = make_phone_numbers(num = 1000)
    print(x[0:10])
    x = make_street_address(path = 'data/street_names.csv', num = 1000)
    print(x[0:10])
    x = make_random_email_domains(path = 'data/emails.csv', num = 1000)
    print(x[0:10])

