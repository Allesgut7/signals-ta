import numpy as np

def support_resistance_levels(df, window=20, count=3):
    supports = []
    resistances = []

    lows = df["Low"].rolling(window).min()
    highs = df["High"].rolling(window).max()

    last_low = lows.iloc[-1]
    last_high = highs.iloc[-1]

    step = (last_high - last_low) / (count + 1)

    for i in range(1, count + 1):
        supports.append(round(last_low + step * (i - 1), 2))
        resistances.append(round(last_high - step * (i - 1), 2))

    return supports, resistances
