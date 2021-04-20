
set -e

cp intermediate_csv/pre_ar_invoices_credit_i_3.csv /tmp

psql --host=localhost -U ocean_user --dbname=ocean_stream -a -f ar_in_to_receipt/insert_ar_invoice_credit.sql
