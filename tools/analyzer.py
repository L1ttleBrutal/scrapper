import json
import os
import uuid
from datetime import datetime

TMP_DIR = os.path.join(os.path.dirname(__file__), '..', '.tmp')
IN_FILE = os.path.join(TMP_DIR, 'market_data.json')
OUT_FILE = os.path.join(TMP_DIR, 'execution_payload.json')
UI_DIR = os.path.join(os.path.dirname(__file__), '..', 'ui', 'public')
UI_OUT_FILE = os.path.join(UI_DIR, 'data.json')
PROGRESS_FILE = os.path.join(os.path.dirname(__file__), '..', 'progress.md')

def log_progress(msg):
    timestamp = datetime.now().isoformat()
    try:
        with open(PROGRESS_FILE, 'a') as f:
            f.write(f"\n- **{timestamp}**: {msg}")
    except:
        pass
    print(msg)

def calculate_order_flow(bids, asks):
    bid_vol = sum(b['price'] * b['size'] for b in bids)
    ask_vol = sum(a['price'] * a['size'] for a in asks)
    total_vol = bid_vol + ask_vol
    if total_vol == 0:
        return 0
    
    # Map to -1 (heavy sell pressure) to 1 (heavy buy pressure)
    ratio = bid_vol / total_vol # 0.5 is neutral
    score = (ratio - 0.5) * 2
    return score

def analyze():
    if not os.path.exists(IN_FILE):
        log_progress("Analyzer Error: market_data.json not found. Halting.")
        return
        
    try:
        with open(IN_FILE, 'r') as f:
            data = json.load(f)
    except Exception as e:
        log_progress(f"Analyzer Error: Could not read input data: {e}")
        return

    # 1. Regime Detection
    price_change = data.get("priceChangePercent", 0)
    abs_change = abs(price_change)
    if abs_change > 3.0:
        regime = "TRENDING UP" if price_change > 0 else "TRENDING DOWN"
    elif abs_change < 1.0:
        regime = "RANGING"
    else:
        regime = "VOLATILE"

    # 2. Order Flow Signal
    bids = data.get("orderBook", {}).get("bids", [])
    asks = data.get("orderBook", {}).get("asks", [])
    order_flow_signal = calculate_order_flow(bids, asks)

    # 3. Breakout Readiness
    breakout_ready = (regime == "VOLATILE" and abs(order_flow_signal) > 0.5)

    # 4. Strategy Combiner & Execution Decision
    # Simple logic
    confidence = abs(order_flow_signal)
    if breakout_ready and order_flow_signal > 0.5:
        action = "BUY"
        pos_size = confidence * 0.1 # Max 10% risk
    elif regime == "TRENDING UP" and order_flow_signal > 0.2:
        action = "BUY"
        pos_size = confidence * 0.15
    elif regime == "TRENDING DOWN" and order_flow_signal < -0.2:
        action = "SELL"
        pos_size = confidence * 0.15
    else:
        action = "HOLD"
        pos_size = 0.0

    # Output execution payload
    payload = {
        "signalId": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "state": {
            "symbol": data.get("symbol"),
            "price": data.get("price"),
            "regime": regime,
            "volatility": abs_change,
            "trendStrength": price_change
        },
        "strategy": {
            "name": "MarketFlow Engine",
            "breakoutReady": breakout_ready,
            "orderFlowSignal": round(order_flow_signal, 4),
            "combinedSignal": round(order_flow_signal, 4)
        },
        "execution": {
            "action": action,
            "positionSize": round(pos_size, 4),
            "confidence": round(confidence, 4),
            "logDetails": f"Condition met for {action} action during {regime} regime."
        }
    }

    with open(OUT_FILE, 'w') as f:
        json.dump(payload, f, indent=2)

    # Ensure UI dir exists and copy
    os.makedirs(UI_DIR, exist_ok=True)
    with open(UI_OUT_FILE, 'w') as f:
        json.dump(payload, f, indent=2)

    log_progress(f"Analyzer: Generated {action} signal. Payload saved to .tmp and ui/public.")

if __name__ == "__main__":
    analyze()
