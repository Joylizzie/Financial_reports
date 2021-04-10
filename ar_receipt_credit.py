import os
import psycopg2
import random
import pandas as pd
import numpy as np
import csv


# get connection
def _get_conn(pw, user_str):
    conn = psycopg2.connect(host="localhost",
                            database = db,
                            user= user_str,
                            password=pw)
    conn.autocommit = False
    return conn
    
# before shipped products to individuals, money is collected from individual cutomers    
# in reality, money received in bank from customers, will be identified who sent the money, for what, like which sales invoice.
# here is just pretending Ocean Stream received the money and our cashier did all the reconciliations and confirmed the results can be booked to system.
def de_receipt(sql, con):
    df = pd.read_sql(sql, con)
    df['entry_type_id'] = df['entry_type_id'].replace(['RIE'], 'RRE')
    df['debit_credit'] = df['debit_credit'].replace(['debit'], 'credit')
    df.to_csv(os.path.join('data', 'ar_receipt_credit.csv'), index=False)    
    return df


if __name__ == '__main__':
    db = 'pacific'
    pw = os.environ['POSTGRES_PW']
    user_str = os.environ['POSTGRES_USER']
    con = _get_conn(pw, user_str)    
    
    sql = """select 
	            ai.company_code,
	            ar.entry_type_id,
	            ai.customer_id,
	            ar.date as transaction_date,
	            ai.rie_id,
	            ai.general_ledger_number,
	            ai.currency_id,
	            ai.debit_credit,
	            ai.amount
            from ar_invoice_item ai
            inner join ar_invoice ar
            on ai.rie_id = ar.rie_id
            where ai.company_code='US001' and debit_credit='debit'
            group by ai.company_code, ar.entry_type_id, ai.customer_id, ar.date,
		            ai.rie_id, ai.general_ledger_number, ai.currency_id,  ai.debit_credit, ai.amount
            order by ai.rie_id
        """
    de_receipt(sql, con)

         
