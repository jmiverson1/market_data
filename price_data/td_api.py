import requests
import pandas as pd

BASE_URL = 'https://api.tdameritrade.com/v1'
API_FILE = 'td_apikey.txt'


def get_apikey(path: str):
    with open(path, 'r') as file:
        apikey = file.read()
    return apikey.strip()


class MarketData:
    def __init__(self, api_key: str, symbol: str):
        self._api_key = api_key
        self._symbol = symbol
        self._url = f'{BASE_URL}/marketdata/{symbol}'

    def price_history(self, period_type: str, period: str = None, frequency_type: str = None, frequency: str = None):
        url = f'{self._url}/pricehistory?apikey={self._api_key}'

        period_type_values = ['day', 'month', 'year', 'ytd']
        if period_type not in period_type_values:
            raise ValueError(f'Valid values for period_type include: {period_type_values}.')
        else:
            url += f'&periodType={period_type}'

        if period is not None:
            period_values = {'day': [1, 2, 3, 4, 5, 10], 'month': [1, 2, 3, 6],
                             'year': [1, 2, 3, 5, 10, 15, 20], 'ytd': [1]}
            if period not in period_values[period_type]:
                raise ValueError(f'''Valid values for period with period_type = {period_type} 
                                     include: {period_values[period_type]}.''')
            else:
                url += f'&period={str(period)}'

        if frequency_type is not None:
            ft_values = {'day': ['minute'],
                         'month': ['daily', 'weekly'],
                         'year': ['daily', 'weekly', 'monthly'],
                         'ytd': ['daily', 'weekly']}
            if frequency_type not in ft_values[period_type]:
                raise ValueError(f'''Valid values for frequency_type with period_type = {period_type}
                                     include: {ft_values[period_type]}.''')
            else:
                url += f'&frequencyType={frequency_type}'

            if frequency is not None:
                frequency_values = {'minute': [1, 5, 10, 15, 30], 'daily': [1], 'weekly': [1], 'monthly': [1]}
                if frequency not in frequency_values[frequency_type]:
                    raise ValueError(f'''Valid values for frequency with frequency_type = {frequency_type}
                                         include: {frequency_values[frequency_type]}.''')
                else:
                    url += f'&frequency={str(frequency)}'

        print(url)
        payload = requests.get(url)
        df = pd.DataFrame.from_dict(payload.json()['candles'])
        df['datetime'] = pd.to_datetime(df['datetime'], utc=True, unit='ms').dt.tz_convert('US/Central')
        df['symbol'] = self._symbol
        df = df[['symbol', 'datetime', 'open', 'high', 'low', 'close', 'volume']]

        return df


if __name__ == '__main__':
    apikey = get_apikey(API_FILE)
    aapl = MarketData(apikey, 'AAPL')
    aapl_history = aapl.price_history('day', period=1, frequency_type='minute', frequency=30)
    aapl_history.to_csv('aapl_test.csv', index=False)
