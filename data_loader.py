import yfinance as yf

def load_data(symbol, period, interval):
    df = yf.download(symbol, period=period, interval=interval)
    
    return df.dropna()

