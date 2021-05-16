set -e
#!/bin/sh

# This script is for creating sql functions, views

# function for trial_balance
psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f reports/function_trial_balance.sql

