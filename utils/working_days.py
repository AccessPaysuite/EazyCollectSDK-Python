from pathlib import Path
from datetime import datetime
from settings import other
from settings import contracts as s_contracts
from settings import direct_debit_processing_days
from datetime import timedelta
from warnings import warn
from requests import get
from exceptions import InvalidStartDateError

base_path = Path(__file__).parent
bank_holidays_file = (base_path / '../includes/holidays.csv').resolve()


def check_working_days_in_future(number_of_days):
    """ Take a number of working days, and add those days from todays
    date. Return a number, which is the number of calendar days in the
    future. If the number is 0, this means the date is acceptable.
    """
    holidays = read_bank_holiday_file_and_check_if_update_needed()
    working_days = 0
    calendar_days = 0
    # Get query date details
    # Get todays date
    today_datetime = datetime.now()
    today_date = today_datetime.date()
    # We want to keep today_date constant for raising errors
    start_date = today_date

    # Check if today is a weekday, if it is not, go to next weekday
    if today_date.isoweekday() not in range(1, 6) or \
            str(today_date) in holidays:
        # Should never need 10 iterations. We want the next working day
        for i in range(10):
            iter = today_date + timedelta(i)
            if iter.isoweekday() in range(1, 5) and str(iter) not in holidays:
                start_date += timedelta(i)
                break
    while working_days <= (number_of_days - 1):
        working_date = start_date + timedelta(calendar_days)
        if working_date.isoweekday() in range(1, 5) \
                and str(working_date) not in holidays:
            working_days += 1
        calendar_days += 1

    final_date = start_date + timedelta(calendar_days)
    while final_date.isoweekday() in range(6,7)\
            or str(final_date) in holidays:
        final_date += timedelta(1)
        calendar_days += 1
    return final_date


def read_bank_holiday_file_and_check_if_update_needed():
    """ Read the bank holidays file, and call the function to
    update it if necessary.
    """
    # We need the datatime to access the year element
    today_datetime = datetime.now()
    today_date = today_datetime.date()
    holidays = []
    with open(bank_holidays_file, 'r') as f:
        # Check the first line of the file to check last update
        text_date = f.readline().strip('\n')

        # The file stores the date as a string. We need a Date object
        date_formatting = '%Y-%m-%d'
        last_update_date = datetime.strptime(text_date, date_formatting).date()
        date_difference = today_date - last_update_date
        day_difference = date_difference.days

        if day_difference >= other['bank_holidays_update_days']:
            print(
                'The bank holidays file has not been updated in over %s'
                ' days. Updating......' % day_difference
            )
            new_holidays = get('https://www.gov.uk/bank-holidays.json')
            holidays_json = new_holidays.json()['england-and-wales']['events']

            for date in holidays_json:
                # Add  bank holidays from or after the current year
                if int(date['date'][0:4]) >= today_datetime.year:
                    holidays.append(date['date'])
                else:
                    continue
                update_bank_holidays_file(holidays)
        else:
            for line in f:
                holidays.append(line.strip('\n'))

        return holidays


def update_bank_holidays_file(bank_holiday_list):
    with open(bank_holidays_file, 'w') as f:
        # Update the header
        f.write(str(datetime.now().date()))
        for date in bank_holiday_list:
            f.write('\n%s' % date)
    return 'Updated bank holidays file.'

