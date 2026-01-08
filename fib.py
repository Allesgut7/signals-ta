def fibonacci_levels(df, trend):
    swing_high = df["High"].max()
    swing_low = df["Low"].min()
    diff = swing_high - swing_low

    # =====================
    # BULLISH TREND
    # =====================
    if trend == "BULLISH":
        retracement = {
            "0.382": round(swing_high - diff * 0.382, 2),
            "0.5": round(swing_high - diff * 0.5, 2),
            "0.618": round(swing_high - diff * 0.618, 2),
        }

        extension = {
            "1.272": round(swing_high + diff * 0.272, 2),
            "1.618": round(swing_high + diff * 0.618, 2),
            "2.0": round(swing_high + diff * 1.0, 2),
        }

    # =====================
    # BEARISH TREND
    # =====================
    else:
        retracement = {
            "0.382": round(swing_low + diff * 0.382, 2),
            "0.5": round(swing_low + diff * 0.5, 2),
            "0.618": round(swing_low + diff * 0.618, 2),
        }

        extension = {
            "1.272": round(swing_low - diff * 0.272, 2),
            "1.618": round(swing_low - diff * 0.618, 2),
            "2.0": round(swing_low - diff * 1.0, 2),
        }

    return retracement, extension
