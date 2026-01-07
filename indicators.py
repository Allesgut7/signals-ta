from ta.trend import SMAIndicator
from ta.momentum import RSIIndicator

def add_indicators(df, ma_fast, ma_slow, rsi_period):
    df["MA_FAST"] = SMAIndicator(df["Close"], ma_fast).sma_indicator()
    df["MA_SLOW"] = SMAIndicator(df["Close"], ma_slow).sma_indicator()
    df["RSI"] = RSIIndicator(df["Close"], rsi_period).rsi()
    return df
