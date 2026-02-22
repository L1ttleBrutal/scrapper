# Project Constitution (gemini.md)

## North Star
Create a clean and interactive dashboard to collect crypto market data, detect regime, get the best strategy, check breakout readiness, get order flow signals, combine into a final signal, execute with position sizing, and log results for adaptation.

## Data Schemas

### 1. Raw Market Data (Input)
```json
{
  "timestamp": "ISO8601",
  "symbol": "string",
  "price": "number",
  "volume": "number",
  "orderBook": {
    "bids": [{"price": "number", "size": "number"}],
    "asks": [{"price": "number", "size": "number"}]
  }
}
```

### 2. Market State & Regime
```json
{
  "timestamp": "ISO8601",
  "regime": "string (e.g., TRENDING, RANGING, VOLATILE)",
  "volatility": "number",
  "trendStrength": "number"
}
```

### 3. Strategy & Signal
```json
{
  "strategyName": "string",
  "breakoutReady": "boolean",
  "orderFlowSignal": "number (-1 to 1)",
  "combinedSignal": "number (-1 to 1)"
}
```

### 4. Execution Payload (Output)
```json
{
  "signalId": "string",
  "timestamp": "ISO8601",
  "action": "string (BUY, SELL, HOLD)",
  "positionSize": "number",
  "confidence": "number",
  "logDetails": "string"
}
```

## Behavioral Rules
*   **Design:** Clean and modern interactive dashboard.
*   **Storage:** Data saved locally on the website initially (Supabase integration later). Refreshing the page brings saved data forward.
*   **Execution Frequency:** The data pipeline and execution trigger runs every 24 hours. Show new data if available, else do nothing.
*   **Prioritize reliability over speed.**

## Architectural Invariants
*   Deterministic, self-healing automation using B.L.A.S.T protocol and A.N.T. 3-layer architecture.
*   No code written until Data Schema is defined (Done).
*   Changes to logic must be updated in `architecture/` before code.
