sudo -u postgres psql  -a -f create_db.sql
sudo -u postgres psql -d ocean_stream -a -f create_table.sql

