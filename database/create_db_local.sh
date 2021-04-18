
set -e
psql --host=localhost -U joy2020 --dbname=postgres  -a -f create_db.sql
psql --host=localhost -U joy2020  --dbname=ocean_stream -a -f create_table.sql
cp data/companies.csv /tmp
cp data/business_type.csv /tmp
cp data/entry_type.csv /tmp
cp data/currencies.csv /tmp
cp data/coa_categories.csv /tmp
cp data/chart_of_accounts.csv /tmp
cp data/profit_centres.csv /tmp
cp data/cost_centres.csv /tmp
cp data/product_categories.csv /tmp
cp data/products.csv /tmp
cp data/tax.csv /tmp
cp data/wbs.csv /tmp
cp data/area_code.csv /tmp
psql --host=localhost -U joy2020 --dbname=ocean_stream -a -f create_table_values.sql