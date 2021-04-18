

cp data/customer_names.csv /tmp
cp data/customer_addresses.csv /tmp
psql --host=localhost -U joy2020 --dbname=pacific -a -f insert_customer_n_a.sql



