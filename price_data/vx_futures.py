import datetime
import calendar
import calendar_tools
import holidays
import urllib.request
import urllib.error


def vx(start_date=datetime.date.today()):
    vx_expirations = []
    exch_holidays = [holiday[1] for holiday in holidays.Holidays().__dict__.items()]
    for month in range(11):
        spx_exp = calendar_tools.nth_day_of_month(start_date.year, start_date.month, 3, calendar.FRIDAY)
        vx_exp = spx_exp - datetime.timedelta(days=30)
        if vx_exp in exch_holidays:
            vx_exp = vx_exp - datetime.timedelta(days=1)
        vx_expirations.append(vx_exp)
        start_date = calendar_tools.next_month(start_date)
    if datetime.date.today() > vx_expirations[1]:
        return vx_expirations[2:]
    else:
        return vx_expirations[1:10]


for exp in vx():
    try:
        csvFile = urllib.request.urlretrieve(
                    'https://markets.cboe.com/us/futures/market_statistics/historical_data/products/csv/VX/' + str(exp) + '/',
                    'C:/Users/jmive/Google Drive/VIX/' + str(exp) + '.csv'
                )
        print(f'{exp} expiration saved.')
    except urllib.error.HTTPError:
        print(f'A csv could not be found for the {exp} expiration.')


#[print(f'VX Expiration: {exp}') for exp in vx()]
#[print(f'Holiday: {holiday[0]}; Date: {holiday[1]}') for holiday in holidays.Holidays().__dict__.items()]
