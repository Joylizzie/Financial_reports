
# je double entry id
python je_double_entries/pre_je_id_se.py

cp je_double_entries/je_item_capital.csv /tmp
psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f je_double_entries/insert_je_capital.sql


