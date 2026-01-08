import numpy as np
# def count_touches(series, level, tolerance):
#     return sum(abs(series - level) <= tolerance)


# def support_resistance_levels(df, swings_high, swings_low, price, min_touch=1, tolerance_pct=0.005, max_levels=3):
#     supports = []
#     resistances = []

#     tolerance = price * tolerance_pct

#     # === SUPPORT ===
#     for _, low in swings_low:
#         if low < price:
#             touches = count_touches(df["Low"], low, tolerance)
#             if touches >= min_touch:
#                 supports.append((low, touches))

#     # === RESISTANCE ===
#     for _, high in swings_high:
#         if high > price:
#             touches = count_touches(df["High"], high, tolerance)
#             if touches >= min_touch:
#                 resistances.append((high, touches))

#     # Sort by closest to price
#     supports = sorted(supports, key=lambda x: abs(price - x[0]))[:max_levels]
#     resistances = sorted(resistances, key=lambda x: abs(price - x[0]))[:max_levels]

#     # Return level only
#     return [round(l[0], 2) for l in supports], [round(l[0], 2) for l in resistances]

# def cluster_prices(prices, zone_width):
#     clusters = []

#     for p in sorted(prices):
#         found = False
#         for c in clusters:
#             if abs(c["price"] - p) <= zone_width:
#                 c["prices"].append(p)
#                 c["price"] = sum(c["prices"]) / len(c["prices"])
#                 found = True
#                 break

#         if not found:
#             clusters.append({
#                 "price": p,
#                 "prices": [p],
#             })

#     return clusters

def support_resistance_levels(
    swings_high,
    swings_low,
    price,
    atr=None,
    max_levels=3,
    zone_pct=0.01,
):
    """
    Support & Resistance berbasis STRUCTURE + FALLBACK
    """

    # =========================
    # ZONE WIDTH
    # =========================
    zone_width = atr * 0.5 if atr else price * zone_pct

    # =========================
    # RAW SWING PRICES
    # =========================
    lows = [low for _, low in swings_low if low < price]
    highs = [high for _, high in swings_high if high > price]

    # =========================
    # CLUSTER FUNCTION
    # =========================
    def cluster(prices):
        clusters = []
        for p in sorted(prices):
            found = False
            for c in clusters:
                if abs(c["price"] - p) <= zone_width:
                    c["values"].append(p)
                    c["price"] = sum(c["values"]) / len(c["values"])
                    found = True
                    break
            if not found:
                clusters.append({"price": p, "values": [p]})
        return clusters

    support_clusters = cluster(lows)
    resistance_clusters = cluster(highs)

    # =========================
    # SCORING (TOUCH + DIST)
    # =========================
    def score(c):
        touch = len(c["values"])
        dist = abs(price - c["price"]) / price
        return touch * 2 - dist * 3

    support_clusters.sort(key=score, reverse=True)
    resistance_clusters.sort(key=score, reverse=True)

    supports = [c["price"] for c in support_clusters[:max_levels]]
    resistances = [c["price"] for c in resistance_clusters[:max_levels]]

    # =========================
    # FALLBACK (ANTI KOSONG)
    # =========================
    if not supports and lows:
        supports = [min(lows)]

    if not resistances and highs:
        resistances = [max(highs)]

    return supports, resistances