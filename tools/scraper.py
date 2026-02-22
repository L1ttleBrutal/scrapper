import json
import urllib.request
import urllib.error
import time
import os
from datetime import datetime

# 1. Goal: Fetch 24h market data
# Target: BTC/USDT using Binance public API
SYMBOL = "BTCUSDT"
TMP_DIR = os.path.join(os.path.dirname(__file__), '..', '.tmp')
OUT_FILE = os.path.join(TMP_DIR, 'market_data.json')
PROGRESS_FILE = os.path.join(os.path.dirname(__file__), '..', 'progress.md')

def log_progress(msg):
    timestamp = datetime.now().isoformat()
    try:
        with open(PROGRESS_FILE, 'a') as f:
            f.write(f"\n- **{timestamp}**: {msg}")
    except:
        pass
    print(msg)

def fetch_data():
    os.makedirs(TMP_DIR, exist_ok=True)
    
    ticker_url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={SYMBOL}"
    depth_url = f"https://api.binance.com/api/v3/depth?symbol={SYMBOL}&limit=10"
    
    retries = 3
    for attempt in range(retries):
        try:
            # Fetch Ticker
            req1 = urllib.request.Request(ticker_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req1, timeout=10) as response:
                ticker_data = json.loads(response.read())
            
            # Fetch Depth
            req2 = urllib.request.Request(depth_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req2, timeout=10) as response:
                depth_data = json.loads(response.read())

            # Format to schema
            payload = {
                "timestamp": datetime.now().isoformat(),
                "symbol": SYMBOL,
                "price": float(ticker_data.get("lastPrice", 0)),
                "volume": float(ticker_data.get("volume", 0)),
                "priceChangePercent": float(ticker_data.get("priceChangePercent", 0)),
                "orderBook": {
                    "bids": [{"price": float(b[0]), "size": float(b[1])} for b in depth_data.get("bids", [])],
                    "asks": [{"price": float(a[0]), "size": float(a[1])} for a in depth_data.get("asks", [])]
                }
            }

            with open(OUT_FILE, 'w') as f:
                json.dump(payload, f, indent=2)
                
            log_progress(f"Scraper: Successfully fetched {SYMBOL} data. Saved to .tmp/market_data.json")
            return True

        except urllib.error.HTTPError as e:
            log_progress(f"Scraper Error: HTTP {e.code} - {e.reason}")
            if e.code == 429: # Rate limit
                time.sleep(5)
                continue
            break
        except Exception as e:
            log_progress(f"Scraper Exception: {str(e)}")
            break
            
    log_progress("Scraper: FAILED to fetch market data.")
    return False

if __name__ == "__main__":
    fetch_data()
