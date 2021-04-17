
set -e

cp double_entries/je_item_capital.csv /tmp

psql --host=localhost -U joy2020 --dbname=pacific -a -f insert_je.sql
