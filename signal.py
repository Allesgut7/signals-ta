def generate_signal(df, supports, resistances):
    last = df.iloc[-1]

    buy = (
        last["Close"] > last["MA_FAST"]
        and last["MA_FAST"] > last["MA_SLOW"]
        and 40 < last["RSI"] < 65
        and last["Close"] <= supports[-1]
    )

    entry = last["Close"]
    stop_loss = supports[0] * 0.98
    take_profit = resistances[0]

    return {
        "signal": "BUY" if buy else "WAIT",
        "entry": round(entry, 2),
        "stop_loss": round(stop_loss, 2),
        "take_profit": round(take_profit, 2),
    }
