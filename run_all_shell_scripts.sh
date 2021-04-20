set -e
#!/bin/sh

bash database/create_db_local.sh
bash je_double_entries/insert_je_capital.sh
bash customers/insert_customer_n_a.sh
bash so_to_item/insert_so.sh
bash so_to_item/insert_so_item.sh
bash sales_invoice/insert_sales_invoices.sh
psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f ar_in_to_receipt/pre_ar_invoice_id.sql
psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f ar_in_to_receipt/insert_ar_invoice_items_debit.sql
bash ar_in_to_receipt/insert_ar_invoice_credit.sh
psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f ar_in_to_receipt/pre_ar_receipt_id.sql
psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f ar_in_to_receipt/pre_ar_receipt_item.sql
python profit_loss.py
