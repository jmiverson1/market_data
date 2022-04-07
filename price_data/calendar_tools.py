import calendar
import datetime


def next_month(start_date):
    if start_date.month == 12:
        return datetime.date(start_date.year + 1, 1, start_date.day)
    elif start_date.day > 28:
        if start_date.year % 4 == 0 & start_date.month == 1:
            return datetime.date(start_date.year, 2, 29)
        else:
            return datetime.date(start_date.year, start_date.month + 1,
                                 calendar.monthrange(start_date.year, start_date.month + 1)[1])
    else:
        return datetime.date(start_date.year, start_date.month + 1, start_date.day)


def nth_day_of_month(year, month, nth_day, day):
    month_arr = calendar.Calendar(day).monthdatescalendar(year, month)
    if month_arr[0][0].day == 1:
        target_date = month_arr[nth_day - 1][0]
    else:
        target_date = month_arr[nth_day][0]
    return target_date


def max_day(year, month, day):
    return calendar.Calendar(day).monthdatescalendar(year, month)[-1][day]