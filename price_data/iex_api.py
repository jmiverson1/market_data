tickers = [
            'JPM',
            'BAC',
            'C',
            'WFC',
            'GS',
            ]

# Create an empty string called `ticker_string` that we'll add tickers and commas to
ticker_string = ''

# Loop through every element of `tickers` and add them and a comma to ticker_string
for ticker in tickers:
    ticker_string += ticker
    ticker_string += ','

# Drop the last comma from `ticker_string`
ticker_string = ticker_string[:-1]

#Create the endpoint and years strings
endpoints = 'charts'
years = '10'
#IEX_API_Key = 'sk_a55db1138a2d4c34858ba0605c4b6c2e' #prod
IEX_API_Key = 'Tpk_1ea2caa4c14a4615b3d0d1d6e5a871e1' #test

#Interpolate the endpoint strings into the HTTP_request string
HTTP_request = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols=aapl,fb&types=chart&range=1m&last=5&token={IEX_API_Key}'

import pandas as pd
bank_data = pd.read_json(HTTP_request, orient='records', typ='series')
for sym, calls in bank_data.items():
    print(sym, end='\n')
    for callType, data in calls.items():
        for item in data:
            for key, value in item.items():
                print('%s: %s' % (key, value))
    #    print('\t %s' % key, end=': ')
    #    for item in value:
    #            print(item)
        #print('\t%s: %s' % (key, value), end='\n')