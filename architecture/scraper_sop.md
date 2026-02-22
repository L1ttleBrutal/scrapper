# SOP: Market Data Scraper

## 1. Goal
Fetch 24h market data for a target cryptocurrency (e.g., BTC/USDT) to act as the primary Source of Truth.

## 2. Input
None (triggered by Cron or `trigger.py`).

## 3. Tool Logic (`tools/scraper.py`)
1. Determine target symbol (default: BTC).
2. Connect to a public API (e.g., Binance public API `https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT` and `https://api.binance.com/api/v3/depth?symbol=BTCUSDT&limit=10`).
3. Parse the data.
4. Format the data to strictly match the **Raw Market Data** schema defined in `gemini.md`.

## 4. Output
Write JSON to `.tmp/market_data.json`.

## 5. Edge Cases & Error Handling
*   **Rate Limits:** If API returns 429, wait 5 seconds and retry (max 3 times).
*   **Network Failure:** Catch `requests.exceptions.RequestException`, log to `progress.md`, and halt execution. Do not output a malformed JSON.
