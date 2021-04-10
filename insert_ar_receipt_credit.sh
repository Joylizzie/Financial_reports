
set -e

cp data/ar_receipt_credit.csv /tmp

psql --host=localhost -U joy2020 --dbname=pacific -a -f insert_ar_receipt_credit.sql
