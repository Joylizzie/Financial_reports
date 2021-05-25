set -e
#!/bin/sh

# This script is for creating sql functions, views

# function for trial_balance(level to general_ledger)
psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f reports/function_trial_balance_gl.sql

# function for trial_balance(level to bspl which is to balance sheet and profit/loss)
psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f reports/function_trial_balance_bspl.sql

# full accounting transaction list( posted in journal ledger, ap, ar)
psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f reports/function_transaction_list.sql

