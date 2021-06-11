set -e
#!/bin/sh
# insert employee id,name, cost centre employee belong to, salary

#python employee/generate_employee_ids.py
#python employee/generate_employee_names.py
#python employee/generate_employee_salary.py
#python employee/employee_cost_centre.py
#
cp data/grades.csv /tmp
cp data/employee_ids.csv /tmp
cp data/employee_names.csv /tmp
cp data/employee_salaries.csv /tmp
cp data/employee_cost_centres.csv /tmp

psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f employee/insert_employee.sql
