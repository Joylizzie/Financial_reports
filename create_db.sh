sudo -u postgres psql  -a -f create_db.sql
sudo -u postgres psql -d ocean_stream -a -f create_table.sql
cp data/customers.csv /tmp
sudo -u postgres psql -d ocean_stream -a -f insert_customers.sql

