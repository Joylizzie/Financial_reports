

cp je_double_entries/je_item_2.csv /tmp
psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f je_double_entries/insert_je_2.sql


