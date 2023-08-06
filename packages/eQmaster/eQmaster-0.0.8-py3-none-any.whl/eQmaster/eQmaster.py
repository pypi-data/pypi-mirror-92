import pandas

def get(stock_list, from_date, to_date):

    df = None 

    for stock_symbol in stock_list:

        if df is None:
            df = pandas.read_parquet(f's3://ephod-tech.trading-advisor.auto-trade.tw.data/stock/stock_symbol={stock_symbol}/stock_price.parquet.gzip')
        else:
            df = df.append(pandas.read_parquet(f's3://ephod-tech.trading-advisor.auto-trade.tw.data/stock/stock_symbol={stock_symbol}/stock_price.parquet.gzip'))
    
    df['Date'] = df['mdate'].apply(lambda x: x[:10])
    df.rename(
        columns = {
            'open_d':'Open', 
            'high_d':'High', 
            'close_d':'Close', 
            'volume': 'Volumn', 
            'close_adj': 'Adj Close', 
            'stockno': 'Outstanding Share',
            'pe_ratio': 'PER',
            'pb_ratio': 'PBR',
            'cdiv_ratio': 'CDIVR',
            'open_adj': 'Open Adj',
            'high_adj': 'High Adj',
            'low_adj': 'Low Adj',
            'open_adj': 'Open Adj'}, 
        inplace = True
    )

    mask = ((df['Date'] >= from_date) & (df['Date'] <= to_date))
    
    return df.loc[mask][['Date','Open','High','Close','Volumn','Adj Close','Outstanding Share','PER','PBR','CDIVR','Open Adj','High Adj','Low Adj','Open Adj']]


