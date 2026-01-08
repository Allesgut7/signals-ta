import matplotlib
matplotlib.use("Agg") 

import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
import os

def plot_swing_analysis(df, fib_retr, fib_ext, trend, symbol="CHART"):
    fig, ax = mpf.plot(
        df,
        type="candle",
        style="yahoo",
        addplot=[
            mpf.make_addplot(df["MA_FAST"], color="blue"),
            mpf.make_addplot(df["MA_SLOW"], color="orange"),
        ],
        figsize=(14, 8),
        returnfig=True,
        volume=False,
        title=f"Swing Trading Analysis ({trend})",
    )

    price_ax = ax[0]

    # =========================
    # Fibonacci Retracement
    # =========================
    for k, v in fib_retr.items():
        price_ax.axhline(v, linestyle="--", alpha=0.7)
        price_ax.text(df.index[-1], v, f"Fib {k}", fontsize=9)

    # =========================
    # Fibonacci Extension (TP)
    # =========================
    for k, v in fib_ext.items():
        price_ax.axhline(v, linestyle=":", color="green", alpha=0.8)
        price_ax.text(df.index[-1], v, f"TP {k}", fontsize=9)

    # =========================
    # SAVE CHART (WAJIB)
    # =========================
    os.makedirs("charts", exist_ok=True)
    filepath = f"charts/{symbol}_swing_analysis.png"
    plt.tight_layout()
    plt.savefig(filepath, dpi=150)
    plt.close()

    print(f"📈 Chart saved: {filepath}")
