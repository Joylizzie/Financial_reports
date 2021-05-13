
set -e

cp intermediate_csv/pre_sales_orders.csv /tmp

psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f so_to_item/insert_so.sql


