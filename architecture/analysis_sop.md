# SOP: Analysis and Signal Generation

## 1. Goal
Analyze raw market data to detect the current market regime, assess breakout readiness, calculate order flow signals, and generate a final Execution Payload.

## 2. Input
Read `.tmp/market_data.json`.

## 3. Tool Logic (`tools/analyzer.py`)
1. **Regime Detection:** 
    * Calculate price change percentage.
    * If absolute change > 3%:
        * If price change > 0, regime = "TRENDING UP".
        * Else, regime = "TRENDING DOWN".
    * If absolute change < 1%, regime = "RANGING".
    * Else, regime = "VOLATILE".
2. **Order Flow Signal:**
    * Analyze the top 10 bids vs top 10 asks from the order book.
    * Calculate Bid/Ask volume ratio. Map ratio to a -1 to 1 score.
3. **Breakout Readiness:**
    * True if Regime is VOLATILE and Order Flow absolute score > 0.5.
4. **Execution Decision:**
    * Combine signals. Provide action (BUY, SELL, HOLD), calculate a mock position size based on confidence.

## 4. Output
Write JSON to `.tmp/execution_payload.json` matching the schema in `gemini.md`.
Copy this payload to the UI directory (e.g., `ui/public/data.json`) for the dashboard to read.

## 5. Edge Cases & Error Handling
*   **Missing Input:** If `.tmp/market_data.json` is missing or malformed, log error and halt. Do not generate a payload.
