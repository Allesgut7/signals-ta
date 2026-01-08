from ta.trend import SMAIndicator, MACD
from ta.momentum import RSIIndicator
import pandas as pd

def add_indicators(df, ma_fast, ma_slow, rsi_period, macd_fast, macd_slow, macd_signal):
    df["MA_FAST"] = SMAIndicator(df["Close"], ma_fast).sma_indicator()
    df["MA_SLOW"] = SMAIndicator(df["Close"], ma_slow).sma_indicator()
    df["RSI"] = RSIIndicator(df["Close"], rsi_period).rsi()
    
    macd = MACD(
        close=df["Close"],
        window_fast=macd_fast,
        window_slow=macd_slow,
        window_sign=macd_signal
    )
    df["MACD"] = macd.macd()
    df["MACD_SIGNAL"] = macd.macd_signal()
    
    return df

def calculate_atr(df, period=14):
    high = df["High"]
    low = df["Low"]
    close = df["Close"]

    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low - close.shift()).abs()
    ], axis=1).max(axis=1)

    atr = tr.rolling(period).mean()
    return atr