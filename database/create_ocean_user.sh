# ocean_user need to be created manaually due to the password issue
psql --host=localhost -U postgres --dbname=ocean_stream  -a -f database/create_ocean_user.sql