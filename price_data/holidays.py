import datetime
import calendar
import calendar_tools


def _easter(year):
    a = int(year % 19)
    b = int(year / 100)
    c = int(year % 100)
    d = int(b / 4)
    e = int(b % 4)
    f = int((b + 8) / 25)
    g = int((b - f + 1) / 3)
    h = int(((19 * a) + b - d - g + 15) % 30)
    i = int(c / 4)
    k = int(c % 4)
    l = int((32 + (2 * e) + (2 * i) - h - k) % 7)
    m = int((a + (11 * h) + (22 * l)) / 451)
    month = (h + l - (7 * m) + 114) / 31
    day = ((h + l - (7 * m) + 114) % 31) + 1
    return datetime.date(year, int(month), int(day) - 2)


def _fixed_holiday(holiday_date):
    if holiday_date.weekday() == calendar.SATURDAY:
        observed_date = holiday_date - datetime.timedelta(days=1)
    elif holiday_date.weekday() == calendar.SUNDAY:
        observed_date = holiday_date + datetime.timedelta(days=1)
    else:
        observed_date = holiday_date
    return observed_date


def _holiday_test(start_date, month, nth_day, day):
    if calendar_tools.nth_day_of_month(start_date.year, month, nth_day, day) < start_date:
        return calendar_tools.nth_day_of_month(start_date.year + 1, month, nth_day, day)
    else:
        return calendar_tools.nth_day_of_month(start_date.year, month, nth_day, day)


class Holidays:
    def __init__(self, start_date=datetime.date.today()):
        self.newYears = _fixed_holiday(datetime.datetime(start_date.year + 1, 1, 1))
        self.mlk = _holiday_test(start_date, 1, 3, calendar.MONDAY)
        self.washingtonBD = _holiday_test(start_date, 2, 3, calendar.MONDAY)
        if _easter(start_date.year) < start_date:
            self.easter = _easter(start_date.year + 1)
        else:
            self.easter = _easter(start_date.year)
        if calendar_tools.max_day(start_date.year, 5, calendar.MONDAY) < start_date:
            self.memorialDay = calendar_tools.max_day(start_date.year + 1, 5, calendar.MONDAY)
        else:
            self.memorialDay = calendar_tools.max_day(start_date.year, 5, calendar.MONDAY)
        if _fixed_holiday(datetime.date(start_date.year, 7, 4)) < start_date:
            self.independenceDay = _fixed_holiday(datetime.date(start_date.year + 1, 7, 4))
        else:
            self.independenceDay = _fixed_holiday(datetime.date(start_date.year, 7, 4))
        self.laborDay = _holiday_test(start_date, 9, 1, calendar.MONDAY)
        self.thanksgiving = _holiday_test(start_date, 11, 4, calendar.THURSDAY)
        if _fixed_holiday(datetime.date(start_date.year, 12, 25)) < start_date:
            self.christmas = _fixed_holiday(datetime.date(start_date.year + 1, 12, 25))
        else:
            self.christmas = _fixed_holiday(datetime.date(start_date.year, 12, 25))
