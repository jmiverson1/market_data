from urllib.request import urlopen
import json
import pandas as pd

API_KEY = '8de05b1173c87fbb63d5afbd84448b49'
BASE_URL = 'https://financialmodelingprep.com/api/v3/'


class FMP:
    def __init__(self, endpoint: str=None, single_parm: str = None, **kwargs):
        if endpoint is not None:
            self.url = f'{BASE_URL}{endpoint}/'
        else:
            self.url = f'{BASE_URL}'
        if single_parm is not None:
            self.url += f'{single_parm}?'
        if kwargs:
            for key, value in kwargs.items():
                self.url += f'{key}={value}&'
        self.url += f'apikey={API_KEY}'

    def get_data(self, returnDF: bool=True) -> list:
        print(f'Calling {self.url}')
        response = urlopen(self.url)
        data = response.read().decode('utf-8')
        if returnDF:
            stocks = json.loads(data)
            out_df = pd.DataFrame()
            stock_ct = len(stocks)
            stock_num = 0
            for stock in stocks:
                stock_num += 1
                print(f'Writing stock {stock_num} of {stock_ct} to df...', end='\r')
                out_df = out_df.append(stock, ignore_index=True)
            print('\nFinished writing to df.')
            return out_df
        else:
            return json.loads(data)


if __name__ == '__main__':
    fmp = FMP(None, 'stock-screener',
              isEtf=False, isActivelyTrading=True, exchange='NYSE,NASDAQ,AMEX', country='US')
    us_stocks = fmp.get_data()
    us_stocks = us_stocks.loc[(((us_stocks.marketCap > 0) & (us_stocks.volume > 0)) | (us_stocks.marketCap > 0))]
    us_stocks = us_stocks.loc[(~us_stocks.industry.str.contains('N/A|Shell Companies|REIT') &
                              (us_stocks.industry.str.len() != 0) &
                              (~us_stocks.sector.str.contains('N/A')) &
                              (us_stocks.sector.str.len() != 0))]