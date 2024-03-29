import random
import datetime
from psyco_connection_ocean import get_connection, get_args, run_program


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
        curs.execute(sql_str)  #cursor closed after the execute action
        item_lst = []
        for row in curs.fetchall():
            item_lst.append(row)
    return item_lst


def do_work(conn, sql_str):
    cur = conn.cursor()
    retrieve_data(conn, sql_str)


if __name__ == '__main__':

    # call the function with parameters to see if the function works#
    sql_str = """select customer_id from sales_orders where company_code='US001' """
    parms = {'sql_str': sql_str}

    run_program(do_work, parms)
