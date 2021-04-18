

cp data/customer_names.csv /tmp
cp data/customer_addresses.csv /tmp
psql --host=localhost -U joy2020 --dbname=ocean_stream -a -f customers/insert_customer_n_a.sql



