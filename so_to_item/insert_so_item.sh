
set -e

python so_to_item/pre_sales_orders_items_i.py
python so_to_item/pre_sales_orders_items_b.py

cp intermediate_csv/pre_sales_orders_items_i_2021_03.csv /tmp
cp intermediate_csv/pre_sales_orders_items_b_2021_03.csv /tmp

psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f so_to_item/insert_so_item.sql
