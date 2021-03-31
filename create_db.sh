set -e
python create_customer.py
python create_sales_orders.py
sudo -u postgres psql  -a -f create_db.sql
sudo -u postgres psql -d ocean_stream -a -f create_table.sql
cp data/customers.csv /tmp
cp data/customer_names.csv /tmp
cp data/sales_orders.csv /tmp
sudo -u postgres psql -d ocean_stream -a -f insert_csv.sql

