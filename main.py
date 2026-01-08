from config import *
from data_loader import load_data
from indicators import add_indicators
from levels import support_resistance_levels
from signal import generate_signal, macd_case_narrative
from fib import fibonacci_levels
from trendline import trend_status
from visualisasi import plot_swing_analysis
import pandas as pd

def run(symbol=SYMBOL):
    df = load_data(symbol, PERIOD, INTERVAL)
    if df is None or df.empty or len(df) < 50:
        print(f"❌ Data tidak tersedia / tidak cukup untuk {symbol}")
        return
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = add_indicators(df, MA_FAST, MA_SLOW, RSI_PERIOD, MACD_FAST, MACD_SLOW, MACD_SIGNAL)

    supports, resistances = support_resistance_levels(df, SUP_RES_WINDOW, SUP_RES_COUNT)
    trend = trend_status(df)
    fib_retr, fib_ext = fibonacci_levels(df, trend)
    trade = generate_signal(df, fib_retr, fib_ext, trend)
    last = df.iloc[-1]
    narrative = macd_case_narrative(df, symbol)
    plot_swing_analysis(
        df=df,
        fib_retr=fib_retr,
        fib_ext=fib_ext,
        trend=trend,
        symbol=symbol
    )


    

    print("\n📊 SWING TRADING ANALYSIS")
    print(f"Saham : {symbol}")
    print(f"Close : {last['Close']:.2f}")
    print(f"RSI   : {last['RSI']:.2f}")
    print(f"MACD  : {last['MACD']:.4f} > {last['MACD_SIGNAL']:.4f}")
    print(f"MA20/MA50 : {last['MA_FAST']:.2f}/{last['MA_SLOW']:.2f}")
    print("\n📈 TREND STATUS")
    print(f"Trend : {trend}")
    print("\n📝 INTEPRETASI MACD")
    print(narrative)


    print("\n🧱 SUPPORT")
    for i, s in enumerate(supports, 1):
        print(f"S{i} : {s}")

    print("\n🧱 RESISTANCE")
    for i, r in enumerate(resistances, 1):
        print(f"R{i} : {r}")

    print("\n📐 FIBONACCI RETRACEMENT (ENTRY / SUPPORT / SL)")
    for k, v in fib_retr.items():
        print(f"Fib {k} : {v}")

    print("\n📐 FIBONACCI EXTENSION (MULTI TAKE PROFIT)")
    for k, v in fib_ext.items():
        print(f"Ext {k} : {v}")

    print("\n🎯 TRADE PLAN")
    for k, v in trade.items():
        print(f"{k.upper()} : {v}")

if __name__ == "__main__":
    run()
