
set search_path TO ocean_stream;

COPY grades(company_code,grade_code,grade_name)
FROM
    '/tmp/grades.csv' DELIMITER ',' CSV HEADER;
    
COPY employee_names(company_code,employee_id,employee_name, grade_code)
FROM
    '/tmp/employee_names.csv' DELIMITER ',' CSV HEADER;
    
COPY employee_salaries(company_code, employee_id, grade_code, currency_id, salary)
FROM
    '/tmp/employee_salaries.csv' DELIMITER ',' CSV HEADER;    

COPY employee_cost_centres(company_code,employee_id, cc_id)
FROM
    '/tmp/employee_cost_centres.csv' DELIMITER ',' CSV HEADER;   
