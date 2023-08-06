from findatapy.market import MarketDataRequest, Market, MarketDataGenerator

md_request = MarketDataRequest(start_date='6 July 2019', finish_date='23 Dec 2020',
                               category='fx', fields=['ask', 'bid', 'askv', 'bidv'], freq='tick',
                               data_source='dukascopy', tickers=["EURUSD"])

df = Market(market_data_generator=MarketDataGenerator()).fetch_market(md_request)

print(df)