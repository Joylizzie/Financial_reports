

cp double_entries/je_item_capital.csv /tmp
psql --host=localhost -U joy2020 --dbname=pacific -a -f insert_je_capital.sql



# get filenames
#IMPFILES=(data/customer_n_import/customer_names.csv, data/customer_n_import/customer_addresses.csv)

# import the files
#for i in ${IMPFILES[@]}
#    do
#        psql -U joy2020 -d pacific -c "\copy TABLE_NAME from '$i' DELIMITER ';' CSV HEADER"
#        # move the imported file
 #       mv $i /data/customer_imported/
#    done
