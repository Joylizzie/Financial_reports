import random
import datetime
random.seed(5)


def randomdate(start_date, end_date):
    # calculate time between start_date and end_date, then convert the time to days
    days_between_dates = (end_date - start_date).days
    # select random day in above days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date

if __name__ == '__main__':
    # below 3 lines feed the data and call the function to see if the function can achieven the expected result
    start_date = datetime.date(2021, 3, 1)
    end_date = datetime.date(2021, 3, 31)
    print(randomdate(start_date, end_date))



