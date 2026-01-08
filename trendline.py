import numpy as np

def calculate_trendline(df, lookback=30):
    data = df.tail(lookback).reset_index(drop=True)
    y = data["Close"].values
    x = np.arange(len(y))

    slope, intercept = np.polyfit(x, y, 1)
    trendline_value = slope * (len(y) - 1) + intercept

    return slope, trendline_value

def trend_status(df, lookback=30, threshold=0.05):
    slope, trend_price = calculate_trendline(df, lookback)
    current_price = df["Close"].iloc[-1]

    if slope > threshold and current_price > trend_price:
        return "BULLISH"
    elif slope < -threshold and current_price < trend_price:
        return "BEARISH"
    else:
        return "SIDEWAYS"
