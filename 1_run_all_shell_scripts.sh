set -e
#!/bin/sh

# This script is for creating db, tables then inserting values

# create db, tables
bash database/create_db_local.sh
#insert customer names and addresses
bash customers/insert_customer_n_a.sh
# insert sales_order_id
bash so_to_item/insert_so.sh
# insert sales orders items
bash so_to_item/insert_so_item.sh
# insert sales invoice ids
bash sales_invoice/insert_sales_invoices.sh
# insert ar invoice ids
psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f ar_in_to_receipt/pre_ar_invoice_id.sql
# insert ar invoice items - debit side
psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f ar_in_to_receipt/insert_ar_invoice_items_debit.sql
# insert ar invoice items - credit side
psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f ar_in_to_receipt/insert_ar_invoice_items_credit.sql
# ar_receipt_item ids
cp ar_in_to_receipt/pre_ar_receipt_id.csv /tmp
psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f ar_in_to_receipt/pre_ar_receipt_id.sql
# ar_receipt_item double entries for both debit and credit side  
psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f ar_in_to_receipt/pre_ar_receipt_item.sql

# je double entry postings(insert je_id, then journal_entry_item)
bash je_double_entries/insert_je_capital.sh
bash je_double_entries/insert_je_2.sh

# insert ap invoice ids and its double entry postings
bash po_in_py/insert_po_in_ap.sh

# generate financial statement

# profit and loss 
python reports/profit_loss.py
# balance sheets progressively achieved desired results
# v1 -v3 results inserted into desired places with different coa, subcoa and bs_pl_idx
python reports/1_balance_sheet.py
python reports/2_balance_sheet.py
python reports/3_balance_sheet.py
# final results with total for different categories and balance sheet is balanced if plus the total amount of profit_loss
python reports/4_balance_sheet.py
