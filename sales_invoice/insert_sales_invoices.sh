
set -e

python sales_invoice/pre_sales_invoices.py
cp intermediate_csv/pre_sales_invoices_i_1.csv /tmp

psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f sales_invoice/insert_sales_invoices.sql
