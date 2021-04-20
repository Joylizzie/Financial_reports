
set -e

cp intermediate_csv/pre_sales_orders_items_i.csv /tmp

psql --host=localhost -U ocean_user --dbname=pacific -a -f so_to_item/insert_so_item.sql
