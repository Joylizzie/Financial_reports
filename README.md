<h1>Financial_reports automation</h1>

<h2>General information</h2> 

This project is for trying to demonstrate automation techniques for generating financal reports.

There is no actual data available from a real company, therefore fictional data will be 
generated via Python random functions and stored in a PostgreSQL database.

The fictional company called Ocean Stream, provides Managed Services(MS), Software Sales(SI), 
 and Consulting Services(CO). It also has in-house software development. 

Ocean Stream currently operates in the US, but is begining to expand to other countries.

Ocean Stream provides obligatory financial reports following IFRS, US GAAP to its investors and 
external stakeholders. Equally importantly it must generate ad hoc reports for its 
internal stakeholders including the Board Directors, Business Unit owners and Profit centre owners, 
to better suport timely decision making.

Ocean Stream currently has 3 Business Units(BU), an ever increasing number of Profit Centres, Cost
Centres. It has 3 new products under developement which require an increasing number of WBS(Work 
Breakdown Structure) codes. 

This project will show step by step, designing and creating a financial database, populating that database
with random financial data, and performing a variety of financial analyses using tools such as Excel,
Tableau, and custom Python code. I will emphasize using automation to reduce repetitious manual work.

<h2> Technical Environment</h2>

1.Database: Postgresql
2.Client:PgAdmin4 - currently host in local laptop
3.Python 3.6
4.Pandas
5.Numpy
6.Bokeh
7.Tkinter

<h2>How To</h2>

More details to be added.

Ocean Stream financial reporting team
Lizzie Zhou
2021-03-01

To Install Posgres on Linux:

    sudo apt update
    sudo apt install postgresql postgresql-contrib

bash test_conn.sh

sudo -u postgres createuser --interactive at promt, say user is financial_user; allow for super user sudo -u postgres psql

connection parameters: psql --host=localhost --dbname=test_conn --username financial_user

sudo -u postgres psql -d -a -f createTable.sql

psql --host=localhost --dbname=ocean_stream --username financial_user
