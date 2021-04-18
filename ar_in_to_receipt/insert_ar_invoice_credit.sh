
set -e

cp data/ar_item_credit.csv /tmp

psql --host=localhost -U joy2020 --dbname=pacific -a -f insert_ar_invoice_credit.sql
