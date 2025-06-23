# detector.py
# Identify trade patterns (volume spikes, wallet buys/sells, etc.)

def detect_volume_spike(current_volume, previous_volume, threshold=2.0):
    if previous_volume is None:
        return False, None
    if current_volume > previous_volume * threshold:
        return True, f"Volume spike detected: {current_volume:.2f} vs {previous_volume:.2f}"
    return False, None

def detect_liquidity_drop(current_liq, previous_liq, threshold=0.3):
    if previous_liq is None or current_liq is None:
        return False, None
    if current_liq < previous_liq * (1 - threshold):
        return True, f"Liquidity drop detected: {current_liq:.2f} vs {previous_liq:.2f}"
    return False, None

def detect_volume_spike(current_volume, previous_volume, threshold=2.0):
    if previous_volume is None:
        return False, None
    if current_volume > previous_volume * threshold:
        return True, f"Volume spike detected: {current_volume:.2f} vs {previous_volume:.2f}"
    return False, None