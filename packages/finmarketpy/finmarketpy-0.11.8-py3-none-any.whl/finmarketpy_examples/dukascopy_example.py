from findatapy.market import Market, MarketDataRequest

md_request = MarketDataRequest(start_date='6 Jul 2018', finish_date='10 Jul 2018',
                                               fields=['ask','bid','askv','bidv'], freq='tick',
                                               data_source='dukascopy', tickers=["Brent"], vendor_tickers=['BRENTCMDUSD'])

df = Market().fetch_market(md_request)

print(df)