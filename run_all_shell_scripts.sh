set -e
#!/bin/sh

bash database/create_db_local.sh
bash customers/insert_customer_n_a.sh
# sales order ids
bash so_to_item/insert_so.sh
# sales orders items
bash so_to_item/insert_so_item.sh
# sales invoice ids
bash sales_invoice/insert_sales_invoices.sh
# ar invoice ids
psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f ar_in_to_receipt/pre_ar_invoice_id.sql
# ar invoice items - debit side
psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f ar_in_to_receipt/insert_ar_invoice_items_debit.sql
# ar invoice items - credit side
psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f ar_in_to_receipt/insert_ar_invoice_items_credit.sql
# ar_receipt_item ids
psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f ar_in_to_receipt/pre_ar_receipt_id.sql
# ar_receipt_item double entries for both debit and credit side  
psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f ar_in_to_receipt/pre_ar_receipt_item.sql

# je double entry postings
bash je_double_entries/insert_je_capital.sh
bash je_double_entries/insert_je_2.sh

# ap invoice double entry postings
bash po_in_py/insert_po_in_ap.sh

# financial statement 
python reports/profit_loss.py
python reports/1_balance_sheet.py
python reports/2_balance_sheet.py
python reports/3_balance_sheet.py
python reports/4_balance_sheet.py
