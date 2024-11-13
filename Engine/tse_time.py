# -*- coding: utf-8 -*-
""""
in tabe baraye sakhtane string zaman hastesh ke baraye estekhraje etelaat az tse
va zakhire sazi zaman dar database estefade mishe
"""

# Import Section Start

import datetime
from datetime import date
import my_sql


# Import Section End


# START

def datetime_type_check(obj):
    try:
        if type(obj) is datetime.datetime:
            return True
        else:
            return False
    except:
        my_sql.log.error_write('')
        return False

def current_time_str():
    now = datetime.datetime.now()
    current_time = now.strftime("%H%M%S")
    return current_time


def today_str(history=False):
    now = date.today()
    now = int_db_form(now)
    if history is True:
        date_time = str(now - 1)
        pass
    else:
        date_time = str(now)
    return date_time


def day_subtract(days_number, holiday_check):
    error_count: int = 0
    error_message = ""
    previous_date = None
    while error_count < 3:
        try:
            previous_date = datetime.datetime.today() - datetime.timedelta(days=days_number)
            day_name = previous_date.strftime("%A")
            if day_name == "Friday":
                previous_date = datetime.datetime.today() - datetime.timedelta(days=(days_number - 2))
                pass
            elif day_name == "Saturday":
                previous_date = datetime.datetime.today() - datetime.timedelta(days=(days_number - 1))
                pass
            else:
                pass
            return int(previous_date.strftime("%Y%m%d"))
        except:
            error_count += 1
            pass
        pass
    if error_count > 3:
        print(error_message)
        return previous_date
    else:
        return previous_date
    pass


def today_int():
    today = today_str()
    return int(today)


def string_db_form(self):
    return self.strftime("%Y%m%d")


def int_db_form(self):
    return int(string_db_form(self))


def latest_ten_minutes():
    time = datetime.datetime.now() - datetime.timedelta(minutes=10)
    return str(time.strftime("%H%M%S"))


def six_month():
    today = date.today()
    temp_date = datetime.timedelta(180)
    six_month = today - temp_date
    six_month = str(six_month.strftime("%Y%m%d"))
    return six_month


def date_calculate_int(sub_day):
    return int((date.today() - datetime.timedelta(days=sub_day)).strftime("%Y%m%d"))


def date_calculate_str(sub_day):
    return (date.today() - datetime.timedelta(days=sub_day)).strftime("%Y%m%d")
