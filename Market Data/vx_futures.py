import calendar
import datetime


def vx_exp(start_date=None):
    months = []
    for i in range(9):
        months.append(datetime.date(start_date.year, start_date.month, 1))
        day_delta = calendar.monthrange(start_date.year, start_date.month)[1]
        start_date = datetime.timedelta(days=day_delta)
        month_arr = calendar.Calendar(4).monthdatescalendar(datetime.date(2020, i+1, 1).year, datetime.date(2020, i+1, 1).month)
        if month_arr[0][0].day == 1:
            spx_exp = month_arr[2][0]
        else:
            spx_exp = month_arr[3][0]
        print(spx_exp)
