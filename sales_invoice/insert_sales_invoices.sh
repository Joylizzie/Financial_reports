
set -e

cp intermediate_csv/sales_invoices_i_1.csv /tmp

psql --host=localhost -U joy2020 --dbname=ocean_stream -a -f sales_invoice/insert_so_invoices.sql
