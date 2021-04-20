
set -e

cp data/sales_orders_items_i.csv /tmp

psql --host=localhost -U ocean_user --dbname=pacific -a -f insert_so_item.sql
