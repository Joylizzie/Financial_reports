
set -e

cp data/sales_invoices.csv /tmp

psql --host=localhost -U joy2020 --dbname=pacific -a -f insert_so_invoices.sql
