set -e
psql --host=localhost -U joy2020 --dbname=postgres  -a -f create_db.sql
psql --host=localhost -U joy2020  --dbname=ocean_stream -a -f create_table.sql
cp data/customers.csv /tmp
cp data/customer_names.csv /tmp
cp data/sales_orders.csv /tmp
psql --host=localhost -U joy2020 --dbname=ocean_stream -d ocean_stream -a -f insert_csv.sql

