"""
Entry-point to program for retrieving prices and adding technical indicators.
"""

import yfinance as yf
import pandas as pd
import numpy as np

CLOSE_FIELD = 'Close'

def get_px_history(symbol: str, period: str) -> pd.DataFrame:
    """

    :param:
        symbol: ticker symbol
        period: lookback period
    :return pd.Dataframe: price history
    """
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period)
    """
    :Parameters:
        period : str
            Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            Either Use period parameter or use start and end
        interval : str
            Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            Intraday data cannot extend last 60 days
        start: str
            Download start date string (YYYY-MM-DD) or _datetime.
            Default is 1900-01-01
        end: str
            Download end date string (YYYY-MM-DD) or _datetime.
            Default is now
        prepost : bool
            Include Pre and Post market data in results?
            Default is False
        auto_adjust: bool
            Adjust all OHLC automatically? Default is True
        back_adjust: bool
            Back-adjusted data to mimic true historical prices
        repair: bool or "silent"
            Detect currency unit 100x mixups and attempt repair.
            If True, fix & print summary. If "silent", just fix.
            Default is False
        keepna: bool
            Keep NaN rows returned by Yahoo?
            Default is False
        proxy: str
            Optional. Proxy server URL scheme. Default is None
        rounding: bool
            Round values to 2 decimal places?
            Optional. Default is False = precision suggested by Yahoo!
        timeout: None or float
            If not None stops waiting for a response after given number of
            seconds. (Can also be a fraction of a second e.g. 0.01)
            Default is 10 seconds.
        debug: bool
            If passed as False, will suppress
            error message printing to console.
        raise_errors: bool
            If True, then raise errors as
            exceptions instead of printing to console.
    """
    hist['daily_return'] = (hist.Close / hist.Close.shift(periods=1)) - 1
    print(f'{hist.daily_return.isna().sum()} NA rows dropped from {symbol}.')
    hist = hist.dropna(subset=['daily_return'])
    return hist

def add_peak_trough_trend(px_hist: pd.DataFrame) -> pd.DataFrame:
    """

    :param px_hist:
    """
    px_hist['trough'] = np.nan
    px_hist['peak'] = np.nan

    trough_idx_0 = px_hist[CLOSE_FIELD].idxmin()
    trough_px_0 = px_hist[CLOSE_FIELD].min()
    px_hist.loc[trough_idx_0, 'trough'] = trough_px_0
    trough_idx_1 = px_hist.loc[px_hist.index > trough_idx_0, CLOSE_FIELD].idxmin()
    trough_px_1 = px_hist.loc[px_hist.index > trough_idx_0, CLOSE_FIELD].min()

    trough_slope = (trough_px_1 - trough_px_0)/(trough_idx_1 - trough_idx_0).days
    for px in px_hist.loc[px_hist.index > trough_idx_0].itertuples():
        px_hist.loc[px.Index, 'trough'] = trough_px_1 + (trough_slope * (px.Index - trough_idx_1).days)

    peak_px_0 = px_hist.loc[trough_idx_0, CLOSE_FIELD]
    peak_idx_1 = px_hist.loc[px_hist.index > trough_idx_0, CLOSE_FIELD].idxmax()
    peak_px_1 = px_hist.loc[px_hist.index > trough_idx_0, CLOSE_FIELD].max()
    px_hist.loc[trough_idx_0, 'peak'] = peak_px_0

    peak_slope = (peak_px_1 - peak_px_0) / (peak_idx_1 - trough_idx_0).days
    for px in px_hist.loc[px_hist.index > trough_idx_0].itertuples():
        px_hist.loc[px.Index, 'peak'] = peak_px_1 + (peak_slope * (px.Index - peak_idx_1).days)

    return px_hist

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    si = get_px_history('SI', '1mo')
    si = add_peak_trough_trend(si)
    si.loc[:, ['Close', 'trough', 'peak']].plot.line()

    '''
    spx = get_px_history('^GSPC')
    vix = get_px_history('^VIX')
    df = spx[['Close', 'daily_return']].join(vix[['Close', 'daily_return']],
                                             how='inner',
                                             lsuffix='_spx',
                                             rsuffix='_vix')
    dates = df.index[(df.daily_return_spx > 0.01) & (df.daily_return_vix > 0.05)].tolist()
    output = pd.DataFrame()
    for dt in dates:
        temp = df.iloc[df.index.get_loc(dt):].head(11)
        temp['cum_return'] = (1 + temp.daily_return_spx).cumprod() - 1
        output = output.append(temp)
    '''
