import matplotlib
matplotlib.use("Agg") 

import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
import os

# def plot_swing_analysis(df, fib_retr, fib_ext, trend, symbol="CHART"):
#     fig, ax = mpf.plot(
#         df,
#         type="candle",
#         style="yahoo",
#         addplot=[
#             mpf.make_addplot(df["MA_FAST"], color="blue"),
#             mpf.make_addplot(df["MA_SLOW"], color="orange"),
#         ],
#         figsize=(14, 8),
#         returnfig=True,
#         volume=False,
#         title=f"Swing Trading Analysis ({trend})",
#     )

#     price_ax = ax[0]

#     # =========================
#     # Fibonacci Retracement
#     # =========================
#     for k, v in fib_retr.items():
#         price_ax.axhline(v, linestyle="--", alpha=0.7)
#         price_ax.text(df.index[-1], v, f"Fib {k}", fontsize=9)

#     # =========================
#     # Fibonacci Extension (TP)
#     # =========================
#     for k, v in fib_ext.items():
#         price_ax.axhline(v, linestyle=":", color="green", alpha=0.8)
#         price_ax.text(df.index[-1], v, f"TP {k}", fontsize=9)

#     # =========================
#     # SAVE CHART (WAJIB)
#     # =========================
#     os.makedirs("charts", exist_ok=True)
#     filepath = f"charts/{symbol}_swing_analysis.png"
#     plt.tight_layout()
#     plt.savefig(filepath, dpi=150)
#     plt.close()

#     print(f"📈 Chart saved: {filepath}")



def plot_swing_analysis(
    df,
    fib_retr,
    fib_ext,
    trend,
    supports=None,
    resistances=None,
    symbol="CHART",
):
    fig, ax = mpf.plot(
        df,
        type="candle",
        style="yahoo",
        addplot=[
            mpf.make_addplot(df["MA_FAST"], color="blue", width=1),
            mpf.make_addplot(df["MA_SLOW"], color="orange", width=1),
        ],
        figsize=(14, 8),
        returnfig=True,
        volume=False,
        title=f"{symbol} | Swing Trading Analysis ({trend})",
        xrotation=0,
        tight_layout=True,
    )

    price_ax = ax[0]

    # =========================
    # REMOVE LEFT & RIGHT PADDING
    # =========================
    # price_ax.set_xlim(df.index[0], df.index[-1])

    # =========================
    # FIBONACCI RETRACEMENT
    # =========================
    for k, v in fib_retr.items():
        price_ax.axhline(v, linestyle="--", alpha=0.6, linewidth=1)
        price_ax.text(
            0.995, v,
            f"Fib {k}",
            transform=price_ax.get_yaxis_transform(),
            ha="right",
            va="center",
            fontsize=9,
        )

    # =========================
    # FIBONACCI EXTENSION (TP)
    # =========================
    for k, v in fib_ext.items():
        price_ax.axhline(v, linestyle=":", color="green", alpha=0.8, linewidth=1.2)
        price_ax.text(
            0.995, v,
            f"TP {k}",
            transform=price_ax.get_yaxis_transform(),
            ha="right",
            va="center",
            fontsize=9,
            color="green",
        )

    # =========================
    # SUPPORT LEVELS
    # =========================
    if supports:
        for s in supports:
            price_ax.axhline(
                s,
                linestyle="--",
                color="green",
                alpha=0.7,
                linewidth=1,
            )
            price_ax.text(
                0.005, s,
                f"Support {round(s,2)}",
                transform=price_ax.get_yaxis_transform(),
                ha="left",
                va="center",
                fontsize=9,
                color="green",
            )

    # =========================
    # RESISTANCE LEVELS
    # =========================
    if resistances:
        for r in resistances:
            price_ax.axhline(
                r,
                linestyle="--",
                color="red",
                alpha=0.7,
                linewidth=1,
            )
            price_ax.text(
                0.005, r,
                f"Resistance {round(r,2)}",
                transform=price_ax.get_yaxis_transform(),
                ha="left",
                va="center",
                fontsize=9,
                color="red",
            )

    # =========================
    # SAVE CHART
    # =========================
    os.makedirs("charts", exist_ok=True)
    filepath = f"charts/{symbol}_swing_analysis.png"
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"📈 Chart saved: {filepath}")
