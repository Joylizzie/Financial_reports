<h2>Postgres install and authentication</h2>

<h3>To Install Posgres on Linux:</h3> 

Assuming all the below code will be input in the same path /home/project/Financial_reports

    sudo apt update
    sudo apt install postgresql postgresql-contrib

bash test_conn.sh

    sudo -u postgres createuser --interactive at promt, say user is ocean_user; 

if allow for super user

    sudo -u postgres psql

connection parameters: 
    psql --host=localhost --dbname=test_conn --username ocean_user
    psql --host=localhost --dbname=ocean_stream --username ocean_user

Example run create_table.sql use user 'postgres'
    sudo -u postgres psql -d -a -f createTable.sql
    

Example run create_table.sql use user 'ocean_user' in linux command line
    psql -h localhost -U ocean_user -db='ocean_stream' -c'create_table.sql'
    press enter
    input ocean_user password
    
Example run create_table.sql use user 'ocean_user' in linux command line by bash
    psql -h localhost -U ocean_user -db='ocean_stream' -c'create_table.sql'
    press enter
    input ocean_user password
        
It is tedious to input password for so many times. I am showing 2 ways to reduce the times of password input.
    in .bashrc file, in new line, input:
    export POSTGRES_PW='**' ** should be your own password to login Postgres
    export POSTGRES_USER='ocean_user'
    
    in home directory, create .pgpass file, in the file input:
    localhost:5432:ocean_stream:ocean_user:** 
    note: ** is ocean_user password to login Postgres as above
    



