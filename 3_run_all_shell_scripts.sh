set -e
#!/bin/sh

# This script is for creating sql functions, generating balance sheet, profit and loss, ar aging report,  profit and loss by pc visualizations

# function for trial_balance(level to general_ledger)
psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f reports/function_trial_balance_gl.sql

# function for trial_balance(level to bspl which is to balance sheet and profit/loss)
psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f reports/function_trial_balance_bspl.sql

# full accounting transaction list( posted in journal ledger, ap, ar)
psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f reports/function_transaction_list.sql

# generate financial statement

# profit and loss 
python reports/profit_loss.py
# balance sheets progressively achieved desired results
# v1 -v3 results inserted into desired places with different coa, subcoa and bs_pl_idx
#python reports/1_balance_sheet.py
#python reports/2_balance_sheet.py
#python reports/3_balance_sheet.py
# final results with total for different categories and balance sheet is balanced if plus the total amount of profit_loss
python reports/4_balance_sheet.py


# ar aging report
python reports/ar_aging.py
python reports/ar_aging_p_d.py

# profit and loss by profit centre
python reports/profit_loss_by_pc_1.py
# more formating with os path changed
python reports/profit_loss_by_pc_2.py

