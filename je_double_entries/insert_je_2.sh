
# je double entry postings
# get a je_id
python je_double_entries/pre_je_id_se.py

cp je_double_entries/je_item_2.csv /tmp
psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f je_double_entries/insert_je_2.sql

# get a je_id
python je_double_entries/pre_je_id_se.py
psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f je_double_entries/insert_je_3_salary.sql


