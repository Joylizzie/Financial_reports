SET search_path TO ocean_stream;

show search_path;

DROP ROLE IF EXISTS ocean_user;

CREATE USER ocean_user WITH PASSWORD 'stream'; 

GRANT ALL PRIVILEGES  ON DATABASE ocean_stream TO ocean_user;