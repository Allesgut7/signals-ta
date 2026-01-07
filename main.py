from config import *
from data_loader import load_data
from indicators import add_indicators
from levels import support_resistance_levels
from signal import generate_signal
from fib import fibonacci_levels
import pandas as pd

def run(symbol=SYMBOL):
    df = load_data(symbol, PERIOD, INTERVAL)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = add_indicators(df, MA_FAST, MA_SLOW, RSI_PERIOD, MACD_FAST, MACD_SLOW, MACD_SIGNAL)

    supports, resistances = support_resistance_levels(df, SUP_RES_WINDOW, SUP_RES_COUNT)
    fib = fibonacci_levels(df)
    trade = generate_signal(df, fib, supports, resistances)
    last = df.iloc[-1]

    print("\n📊 SWING TRADING ANALYSIS")
    print(f"Saham : {symbol}")
    print(f"Close : {last['Close']:.2f}")
    print(f"RSI   : {last['RSI']:.2f}")
    print(f"MACD  : {last['MACD']:.4f} > {last['MACD_SIGNAL']:.4f}")
    print(f"MA20/MA50 : {last['MA_FAST']:.2f}/{last['MA_SLOW']:.2f}")

    print("\n🧱 SUPPORT")
    for i, s in enumerate(supports, 1):
        print(f"S{i} : {s}")

    print("\n🧱 RESISTANCE")
    for i, r in enumerate(resistances, 1):
        print(f"R{i} : {r}")

    print("\n📐 FIBONACCI")
    for k, v in fib.items():
        print(f"{k} : {v}")

    print("\n🎯 TRADE PLAN")
    for k, v in trade.items():
        print(f"{k.upper()} : {v}")

if __name__ == "__main__":
    run()
