
set -e
psql --host=localhost -U postgres --dbname=postgres  -a -f database/create_db.sql