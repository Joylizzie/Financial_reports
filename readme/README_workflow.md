<h2>workflow</h2>

<h3>1.create database(db)</h3>

create database
    |
    |---> Psql from command line, PgAdmin GUI
    |------> db name, user name, password as variables, save in bashrc file or provide when call function
    |------> sql code needed for kill connections with db only allow current connection 
    |------> in early stage, db will be erased and recreated MANY times
    |
create table in db (more details below)
    |
    |---> store scripts for creating tables in the same file
    |---> in early stage, tables will be drppoed and recreated MANY times
    |---> the sequence of tables to be created matters.
    |------> table determinded by other tables should be placed after its depedant
    |----> constraints should be in place
    | 
upload values to db - stage 1
    |-> via psycopg2 - NOT RECOMMEND(slower and other reasons)
    |-> via Psql
    |---> store values in csv files
    |------> manually predefine values for tables created
    |------> using python to create desired random values 
    |---> create sql scripts for copy csv files save in *.sql file
    |---> create bash file to cope the above csv file *.sh file
    |---> the order of tables to be created matters
    |---> run above *.sh file in command line
    |
retrieve data from db
    |
    |---> psycopg2 connect to db to retrieve data - tupples
    |---> write above tupples to csv file if needed
    |
create data based on above existing data in db
    |
    |---> use python or sql code to create more desired data
    |---> write above data to csv file
    |
upload values to db - stage 2
    |
    |---> repeate upload values to db - stage 1
    


<h3>1.sales_orders, sales_orders_items, sales_invoices, ar_invoice</h3>

sales_orders
    |
    |---> place sales orders for customers
    |
sales_orders_items
    |
    |---> a sales order can  have one or multiple items(product, service)
    |
sales_invoices
    |
    |---> a sales invoice correspodants to one sales order number for item(s) shipped
    |
ar_invoice(double entry)
    |
    |---> post this double entry to reflect sales invoice in financial statement
    


more to be added