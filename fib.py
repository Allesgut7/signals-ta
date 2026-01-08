from indicators import calculate_atr
def adaptive_lookback(df, min_lb=3, max_lb=10):
    df["ATR"] = calculate_atr(df)
    atr = df["ATR"].iloc[-1]
    avg_range = (df["High"] - df["Low"]).rolling(20).mean().iloc[-1]

    ratio = atr / avg_range if avg_range else 1
    lb = int(min_lb + (max_lb - min_lb) * min(1, ratio))

    return max(min_lb, min(lb, max_lb))
# =========================
# SWING DETECTION
# =========================
def detect_swings(df):
    """
    Detect swing highs and lows using pivot logic
    """
    lookback = adaptive_lookback(df)
    swing_highs = []
    swing_lows = []

    for i in range(lookback, len(df) - lookback):
        high = df["High"].iloc[i]
        low = df["Low"].iloc[i]

        # Swing High
        if high == max(df["High"].iloc[i - lookback:i + lookback + 1]):
            swing_highs.append((i, high))

        # Swing Low
        if low == min(df["Low"].iloc[i - lookback:i + lookback + 1]):
            swing_lows.append((i, low))

    return swing_highs, swing_lows


# =========================
# SELECT VALID SWING BASED ON TREND
# =========================
def get_valid_swing(df, trend):
    # lookback = adaptive_lookback(df)
    swing_highs, swing_lows = detect_swings(df)

    if not swing_highs or not swing_lows:
        return None, None

    if trend == "BULLISH":
        # Swing low terakhir sebelum swing high terakhir
        last_high_idx, last_high = swing_highs[-1]
        valid_lows = [l for l in swing_lows if l[0] < last_high_idx]
        if not valid_lows:
            return None, None
        swing_low_idx, swing_low = valid_lows[-1]
        return swing_low, last_high

    elif trend == "BEARISH":
        # Swing high terakhir sebelum swing low terakhir
        last_low_idx, last_low = swing_lows[-1]
        valid_highs = [h for h in swing_highs if h[0] < last_low_idx]
        if not valid_highs:
            return None, None
        swing_high_idx, swing_high = valid_highs[-1]
        return swing_high, last_low

    return None, None


# =========================
# FIBONACCI CALCULATION
# =========================
def fibonacci_levels(swing_low, swing_high, trend):
    """
    Returns retracement & extension levels
    """
    fib_retr = {}
    fib_ext = {}

    diff = swing_high - swing_low

    if trend == "BULLISH":
        fib_retr = {
            "0": swing_high - diff * 0,
            "0.382": swing_high - diff * 0.382,
            "0.5": swing_high - diff * 0.5,
            "0.618": swing_high - diff * 0.618,
            "1": swing_high - diff * 1,
        }
        fib_ext = {
            "1": swing_high + diff * 0.272,
            "2": swing_high + diff * 0.618,
            "3": swing_high + diff * 1.0,
        }

    elif trend == "BEARISH":
        fib_retr = {
            "0": swing_low + diff * 0,
            "0.382": swing_low + diff * 0.382,
            "0.5": swing_low + diff * 0.5,
            "0.618": swing_low + diff * 0.618,
            "1": swing_low + diff * 1,
        }
        fib_ext = {
            "1": swing_low - diff * 0.272,
            "2": swing_low - diff * 0.618,
            "3": swing_low - diff * 1.0,
        }

    return fib_retr, fib_ext
