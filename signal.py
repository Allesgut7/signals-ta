def generate_signal(df, fib_retr, fib_ext):
    last = df.iloc[-1]
    price = last["Close"]

    # ENTRY ZONE
    entry_zone = fib_retr["0.382"] <= price <= fib_retr["0.5"]

    # BUY CONFIRMATION
    buy_signal = (
        price > last["MA_FAST"]
        and last["MA_FAST"] > last["MA_SLOW"]
        and 40 < last["RSI"] < 65
        and last["MACD"] > last["MACD_SIGNAL"]
        and entry_zone
    )

    entry = price
    support = fib_retr["0.618"]
    stop_loss = round(fib_retr["0.618"] * 0.97, 2)

    return {
        "signal": "BUY" if buy_signal else "WAIT",
        "entry": round(entry, 2),
        "support": support,
        "stop_loss": stop_loss,
        "tp1": fib_ext["1.272"],
        "tp2": fib_ext["1.618"],
        "tp3": fib_ext["2.0"],
    }


def macd_case_narrative(df, symbol):
    last = df.iloc[-1]
    prev = df.iloc[-2]

    close_now = round(last["Close"], 2)
    close_prev = round(prev["Close"], 2)

    macd_now = last["MACD"]
    signal_now = last["MACD_SIGNAL"]
    macd_prev = prev["MACD"]
    signal_prev = prev["MACD_SIGNAL"]

    recent_low = round(df["Low"].rolling(10).min().iloc[-1], 2)

    # Case 1: Bullish crossover
    if macd_prev < signal_prev and macd_now > signal_now:
        return (
            f"Saham {symbol} sebelumnya berada dalam tekanan jual dan sempat "
            f"turun hingga area {recent_low}. Setelah fase penurunan tersebut, "
            f"harga mulai bergerak naik dan saat ini berada di {close_now}. "
            f"Pada level ini, MACD line menembus signal line dari bawah, "
            f"yang menunjukkan bahwa momentum bearish telah berakhir dan "
            f"momentum bullish mulai terbentuk. "
            f"Kondisi ini sering menjadi indikasi awal dimulainya tren naik baru, "
            f"sehingga saham ini mulai menarik untuk dipertimbangkan sebagai "
            f"peluang buy untuk skenario swing trading."
        )

    # Case 2: Early reversal (belum crossover)
    if macd_now < signal_now and macd_now > macd_prev:
        return (
            f"Saham {symbol} sebelumnya mengalami tren turun dan harga sempat "
            f"menyentuh area {recent_low}. Namun dalam beberapa hari terakhir, "
            f"penurunan mulai melambat dan harga bergerak stabil di sekitar "
            f"{close_now}. MACD line masih berada di bawah signal line, "
            f"namun arahnya mulai berbalik ke atas. "
            f"Hal ini mengindikasikan bahwa tekanan jual mulai melemah "
            f"dan potensi pembalikan tren mulai terbentuk. "
            f"Jika dikonfirmasi oleh kenaikan harga selanjutnya, kondisi ini "
            f"dapat menjadi sinyal buy awal bagi swing trader."
        )

    # Case 3: Momentum melemah
    if macd_now > signal_now and (macd_now - signal_now) < (macd_prev - signal_prev):
        return (
            f"Saham {symbol} saat ini masih bergerak dalam tren naik, "
            f"dengan harga berada di sekitar {close_now}. "
            f"MACD line masih berada di atas signal line, "
            f"namun jarak keduanya mulai menyempit. "
            f"Kondisi ini menandakan momentum kenaikan mulai melemah, "
            f"sehingga trader perlu lebih berhati-hati dan mulai "
            f"mempertimbangkan pengamanan profit atau menunggu konfirmasi lanjutan."
        )

    # Case 4: Bearish crossover
    if macd_prev > signal_prev and macd_now < signal_now:
        return (
            f"Saham {symbol} sebelumnya sempat mengalami kenaikan, "
            f"namun di sekitar harga {close_now}, MACD line menembus "
            f"signal line dari atas ke bawah. "
            f"Sinyal ini menunjukkan bahwa momentum naik mulai berakhir "
            f"dan tekanan jual mulai mendominasi. "
            f"Dalam kondisi seperti ini, risiko koreksi meningkat "
            f"sehingga kurang ideal untuk membuka posisi buy."
        )

    # Default
    return (
        f"Saham {symbol} saat ini bergerak stabil di sekitar harga {close_now} "
        f"dan MACD belum menunjukkan perubahan momentum yang signifikan. "
        f"Tren yang sedang berlangsung masih berpotensi berlanjut "
        f"hingga muncul sinyal baru dari pergerakan MACD."
    )
