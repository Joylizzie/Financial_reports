
set -e

cp intermediate_csv/pre_sales_invoices_i_1.csv /tmp

psql --host=localhost -U joy2020 --dbname=ocean_stream -a -f sales_invoice/insert_sales_invoices.sql
