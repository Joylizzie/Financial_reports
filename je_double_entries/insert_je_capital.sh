

cp double_entries/je_item_capital.csv /tmp
psql --host=localhost -U joy2020 --dbname=ocean_stream -a -f insert_je_capital.sql


