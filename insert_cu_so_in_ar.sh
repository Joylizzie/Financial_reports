
set -e

cp data/sales_orders.csv /tmp
cp data/sales_orders_items_i.csv /tmp
cp data/sales_invoices_i_1.csv /tmp
cp data/ar_item_credit.csv /tmp

psql --host=localhost -U joy2020 --dbname=pacific -a -f insert_so.sql
psql --host=localhost -U joy2020 --dbname=pacific -a -f insert_so_item.sql
psql --host=localhost -U joy2020 --dbname=pacific -a -f insert_so_invoices.sql
psql --host=localhost -U joy2020 --dbname=pacific -a -f insert_ar_invoices.sql
psql --host=localhost -U joy2020 --dbname=pacific -a -f insert_ar_invoice_items_debit.sql
psql --host=localhost -U joy2020 --dbname=pacific -a -f insert_ar_invoice_items_credit.sql
