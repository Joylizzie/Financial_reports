import csv

def create_csv(path):
    with open(path, 'r') as read_obj, open('data/customer_names.csv', 'w') as write_obj:
        csv_reader = csv.DictReader(read_obj)
        csv_writer = csv.writer(write_obj)
        for i in csv_reader:
            fields = i['customer_name'].split(',')
            csv_writer.writerow([i['customer_id'], fields[0], fields[1]])


if __name__ == '__main__':
    create_csv('data/customers.csv')
