def generate_signal(df, fib, supports, resistances):
    last = df.iloc[-1]

    buy_signal = (
        last["Close"] > last["MA_FAST"]
        and last["MA_FAST"] > last["MA_SLOW"]
        and 40 < last["RSI"] < 70
        and last["MACD"] > last["MACD_SIGNAL"]
        and fib["0.382"] <= last["Close"] <= fib["0.5"]
    )

    entry = last["Close"]

    trade_plan = {
        "signal": "BUY" if buy_signal else "WAIT",
        "entry": round(entry, 2),
        "stop_loss": round(min(fib["0.618"], supports[0]) * 0.98, 2),
        "tp1": fib["0.618"],
        "tp2": fib["0.786"],
        "tp3": resistances[0],
    }

    return trade_plan
