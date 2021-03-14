import random
import datetime
from psycoConnection_ocean import get_connection

def randomdate(start_date, end_date):
    # calculate time between start_date and end_date, then convert the time to days    
    days_between_dates = (end_date - start_date).days
    # select random day in above days
    random_number_of_days = random.randrange(days_between_dates) 
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date


# below 3 lines feed the data and call the function to see if the function can achieven the expected result
'''
start_date = datetime.date(2021, 3, 1)
end_date = datetime.date(2021, 3, 31)
print(randomdate(start_date, end_date))
'''


# fetch existing data from database and close cursur
def retrieve_data(conn, sql_str):
    
    with conn.cursor() as curs:
        curs.execute(sql_str) #cursor closed after the execute action
        item_lst = []
        for row in curs.fetchall():
            item_lst.append(row)
    return item_lst   

# call the function to see if the function works
if __name__ == '__main__':
    conn = get_connection()
    sql_str = sql = """select customer_id from sales_orders where company_code='US001'
          """
    print(retrieve_data(conn, sql_str))
