
set -e

cp data/sales_orders.csv /tmp

psql --host=localhost -U joy2020 --dbname=pacific -a -f insert_so.sql
