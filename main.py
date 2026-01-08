from config import *
from data_loader import load_data
from indicators import add_indicators, calculate_atr
from levels import support_resistance_levels
from signal import generate_signal, macd_case_narrative
from fib import get_valid_swing, fibonacci_levels, detect_swings
from trendline import trend_status
from visualisasi import plot_swing_analysis
from market_structure import detect_bos_choch
import pandas as pd


def run(symbol=SYMBOL):
    # =========================
    # 1️⃣ LOAD DATA
    # =========================
    df = load_data(symbol, PERIOD, INTERVAL)
    if df is None or df.empty or len(df) < 50:
        print(f"❌ Data tidak tersedia / tidak cukup untuk {symbol}")
        return
    df["ATR"] = calculate_atr(df)

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # =========================
    # 2️⃣ ADD INDICATORS
    # =========================
    df = add_indicators(df, MA_FAST, MA_SLOW, RSI_PERIOD, MACD_FAST, MACD_SLOW, MACD_SIGNAL)
    # 3️⃣ SUPPORT & RESISTANCE
    # =========================
    swing_highs, swing_lows = detect_swings(df)
    supports, resistances = support_resistance_levels(
        swing_highs,
        swing_lows,
        price=df['Close'].iloc[-1],
        atr=df["ATR"].iloc[-1]
    )
    # =========================
    # 4️⃣ TREND STATUS
    # =========================
    # trend = trend_status(df)
    trend, structure_signal = detect_bos_choch(swing_highs, swing_lows)
    
    # =========================
    # 5️⃣ AUTO SWING & FIBONACCI
    # =========================
    swing_low, swing_high = get_valid_swing(df, trend)
    if not swing_low or not swing_high:
        print("❌ Tidak ditemukan swing valid untuk Fibonacci")
        return

    fib_retr, fib_ext = fibonacci_levels(swing_low, swing_high, trend)

    # =========================


    # =========================
    # 6️⃣ SIGNAL GENERATION
    # =========================
    trade = generate_signal(df, fib_retr, fib_ext, trend)

    # =========================
    # 7️⃣ MACD NARRATIVE
    # =========================
    narrative = macd_case_narrative(df, symbol)

    # =========================
    # 8️⃣ PLOT VISUALISASI
    # =========================
    plot_swing_analysis(
        df=df,
        fib_retr=fib_retr,
        fib_ext=fib_ext,
        trend=trend,
        supports=supports,
        resistances=resistances,
        symbol=symbol
    )
    
    

    # =========================
    # 9️⃣ OUTPUT KE CONSOLE
    # =========================
    last = df.iloc[-1]
    print("\n📊 SWING TRADING ANALYSIS")
    print(f"Saham      : {symbol}")
    print(f"Close      : {last['Close']:.2f}")
    print(f"RSI        : {last['RSI']:.2f}")
    print(f"MACD       : {last['MACD']:.4f} > {last['MACD_SIGNAL']:.4f}")
    print(f"MA20/MA50  : {last['MA_FAST']:.2f}/{last['MA_SLOW']:.2f}")
    print(f"Swings Low : {swing_low}")
    print(f"Swing High : {swing_high}")
    print(f"Market Structure : {structure_signal}")

    print("\n📈 TREND STATUS")
    print(f"Trend      : {trend}")

    print("\n📝 INTERPRETASI MACD")
    print(narrative)

    print("\n🧱 SUPPORT LEVELS")
    for i, s in enumerate(supports, 1):
        print(f"S{i} : {s}")

    print("\n🧱 RESISTANCE LEVELS")
    for i, r in enumerate(resistances, 1):
        print(f"R{i} : {r}")

    print("\n📐 FIBONACCI RETRACEMENT (ENTRY / SUPPORT / SL)")
    for k, v in fib_retr.items():
        print(f"Fib {k} : {v:.2f}")

    print("\n📐 FIBONACCI EXTENSION (MULTI TAKE PROFIT)")
    for k, v in fib_ext.items():
        print(f"Ext {k} : {v:.2f}")

    print("\n🎯 TRADE PLAN")
    for k, v in trade.items():
        if isinstance(v, list):
            v = ", ".join([str(x) for x in v])
        print(f"{k.upper():<12} : {v}")


if __name__ == "__main__":
    run()
