from config import *
from data_loader import load_data
from indicators import add_indicators
from levels import support_resistance_levels
from signal import generate_signal
import pandas as pd

def run(symbol=SYMBOL):
    df = load_data(symbol, PERIOD, INTERVAL)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = add_indicators(df, MA_FAST, MA_SLOW, RSI_PERIOD)

    supports, resistances = support_resistance_levels(
        df, SUP_RES_WINDOW, SUP_RES_COUNT
    )

    trade = generate_signal(df, supports, resistances)
    last = df.iloc[-1]

    print("\n📊 SWING TRADING ANALYSIS")
    print(f"Saham     : {symbol}")
    print(f"Close     : {last['Close']:.2f}")
    print(f"RSI       : {last['RSI']:.2f}")
    print(f"MA{MA_FAST}/MA{MA_SLOW} : {last['MA_FAST']:.2f}/{last['MA_SLOW']:.2f}")

    print("\n🧱 SUPPORT LEVELS")
    for i, s in enumerate(supports, 1):
        print(f"S{i} : {s}")

    print("\n🧱 RESISTANCE LEVELS")
    for i, r in enumerate(resistances, 1):
        print(f"R{i} : {r}")

    print("\n🎯 TRADE PLAN")
    for k, v in trade.items():
        print(f"{k.replace('_',' ').title()} : {v}")

if __name__ == "__main__":
    run()
