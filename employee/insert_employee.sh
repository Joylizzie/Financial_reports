
set -e

python employee/generate_employee_ids.py
python employee/generate_employee_names.py

cp intermediate_csv/pre_sales_orders_items_i_2021_03.csv /tmp
cp intermediate_csv/pre_sales_orders_items_b_2021_03.csv /tmp

psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f so_to_item/insert_so_item.sql
