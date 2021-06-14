import os
import pandas as pd
import csv
import random


from generate_employee_ids import employee_ids
import make_random_data

random.seed(5)


def generate_employee_names(data_file):
    
    df = pd.read_csv('data/employee_ids.csv', usecols=['employee_id'])
    employee_ids_lst = df['employee_id'].values.tolist()
    n = len(employee_ids_lst)
    # employee name
    employee_surnames = make_random_data.make_random_surnames(path = 'data/surnames.csv', num = n)
    employee_first_names = make_random_data.make_random_first_names(path = 'data/first_names.csv', num = n)
    # grades
    grade = [1,2,3]
    grade_weights = [10, 1500, 1490]
    
    
    return [('US001',
            employee_ids_lst[i], 
            (employee_surnames[i] + ',' + employee_first_names[i][0]),
            random.choices(grade, weights=grade_weights,k=1)[0]) for i in range(n)]


def create_csv(data_file, tup_gen, header,out_file):
    tups = tup_gen(data_file)
    with open(os.path.join('data', out_file), 'w') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(header)
        for i in range(len(tups)):
            csv_writer.writerow(tups[i])
        print('Done writing.')    
    

if __name__ == '__main__':
    data_file = '/home/lizhi/projects/joylizzie/Financial_reports/data/list-cities-washington-198j.csv'
    generate_employee_names(data_file)
    create_csv(data_file = data_file,
            out_file = '/home/lizhi/projects/joylizzie/Financial_reports/data/employee_names.csv',
            tup_gen = generate_employee_names,
            header = ['company_code','employee_id','employee_name', 'grade_code'])
