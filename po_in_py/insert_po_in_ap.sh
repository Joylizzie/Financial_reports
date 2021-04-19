
set -e
:'
cp data/vendors.csv /tmp
cp data/vendor_addresses.csv /tmp

psql --host=localhost -U joy2020 --dbname=pacific -a -f insert_ap.sql
'
