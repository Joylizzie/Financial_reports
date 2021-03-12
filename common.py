# fetch existing data from database and close cursur
from psycoConnection_ocean import get_connection

def retrieve_data(conn, sql_str):
    
    with conn.cursor() as curs:
        curs.execute(sql_str) #cursor closed after the execute action
        item_lst = []
        for row in curs.fetchall():
            item_lst.append(row)
    return item_lst   

# call the function to see if the function works
conn = get_connection()
sql_str = sql = """select customer_id from sales_orders where company_code='US001'
      """
print(retrieve_data(conn, sql_str))
