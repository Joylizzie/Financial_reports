
set -e

python so_to_item/pre_sales_orders.py
cp intermediate_csv/pre_sales_orders.csv /tmp


psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f so_to_item/insert_so.sql


