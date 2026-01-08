def detect_bos_choch(swings_high, swings_low):
    if len(swings_high) < 2 or len(swings_low) < 2:
        return "SIDEWAYS", "NONE"

    sh1, sh2 = swings_high[-1][1], swings_high[-2][1]
    sl1, sl2 = swings_low[-1][1], swings_low[-2][1]

    hh = sh1 > sh2
    hl = sl1 > sl2
    lh = sh1 < sh2
    ll = sl1 < sl2

    # BOS
    if hh and hl:
        return "BULLISH", "BOS - Break of Structure"
    if lh and ll:
        return "BEARISH", "BOS - Break of Structure"

    # CHoCH
    if hh and not hl:
        return "BULLISH", "CHoCH - Change of Character"
    if ll and not lh:
        return "BEARISH", "CHoCH - Change of Character"

    return "SIDEWAYS", "NONE"
