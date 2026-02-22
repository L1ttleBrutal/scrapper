import { useState, useEffect } from 'react'
import './index.css'
import { FloatingPaths } from './components/ui/background-paths'

function App() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [lastUpdate, setLastUpdate] = useState(null)

  const fetchData = async () => {
    setLoading(true)
    try {
      // Add timestamp to foil cache
      const response = await fetch(`/data.json?t=${new Date().getTime()}`)
      if (!response.ok) throw new Error('Data not found')
      const payload = await response.json()

      setData(payload)
      setLastUpdate(new Date().toLocaleString())
      // Save state to local storage to persist on refresh
      localStorage.setItem('marketflow_dashboard_data', JSON.stringify({
        payload,
        timestamp: new Date().toLocaleString()
      }))
    } catch (error) {
      console.error('Fetch error, falling back to local storage', error)
      const stored = localStorage.getItem('marketflow_dashboard_data')
      if (stored) {
        const parsed = JSON.parse(stored)
        setData(parsed.payload)
        setLastUpdate(parsed.timestamp + ' (Cached)')
      }
    } finally {
      setTimeout(() => setLoading(false), 500) // smooth transition
    }
  }

  useEffect(() => {
    // Attempt initial load
    const stored = localStorage.getItem('marketflow_dashboard_data')
    if (stored) {
      const parsed = JSON.parse(stored)
      setData(parsed.payload)
      setLastUpdate(parsed.timestamp + ' (Local Storage)')
      setLoading(false)
    } else {
      fetchData()
    }

    // Simulate Trigger every 24h by fetching periodically (every 5 mins for demo)
    const interval = setInterval(fetchData, 300000)
    return () => clearInterval(interval)
  }, [])

  if (!data && loading) {
    return <div className="loader"></div>
  }

  if (!data) {
    return <div>No market data available. Please run the MarketFlow pipeline first.</div>
  }

  const { state, strategy, execution } = data
  const isBuy = execution.action === 'BUY'
  const isSell = execution.action === 'SELL'

  const actionClass = isBuy ? 'action-buy' : (isSell ? 'action-sell' : 'action-hold')
  const actionColor = isBuy ? 'value-green' : (isSell ? 'value-red' : '')

  return (
    <>
      <div style={{ position: 'fixed', inset: 0, overflow: 'hidden', zIndex: 0, pointerEvents: 'none' }}>
        <FloatingPaths position={1} />
        <FloatingPaths position={-1} />
      </div>
      <div className="dashboard-container" style={{ position: 'relative', zIndex: 10 }}>
        <header>
          <h1>⚡ MarketFlow</h1>
          <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
            <div className="status-badge">System Active</div>
            <button className="refresh-btn" onClick={fetchData}>
              {loading ? <div className="loader" style={{ width: '14px', height: '14px', borderWidth: '2px' }} /> : 'Refresh Sync'}
            </button>
          </div>
        </header>

        <div className="timestamp">
          Last Sync: {lastUpdate}
        </div>

        <div className="grid">
          {/* Market State Card */}
          <div className="card">
            <div className="card-title">🌐 Market State | {state.symbol}</div>
            <div className="metric-row">
              <span>Current Price</span>
              <span style={{ fontWeight: 600 }}>${state.price.toLocaleString(undefined, { minimumFractionDigits: 2 })}</span>
            </div>
            <div className="metric-row">
              <span>Market Regime</span>
              <span style={{ fontWeight: 600, color: 'var(--accent-blue)' }}>{state.regime}</span>
            </div>
            <div className="metric-row">
              <span>24h Volatility</span>
              <span>{state.volatility.toFixed(2)}%</span>
            </div>
          </div>

          {/* Strategy Engine Card */}
          <div className="card">
            <div className="card-title">⚙️ Strategy Engine</div>
            <div className="metric-row">
              <span>Active Strategy</span>
              <span style={{ fontWeight: 600 }}>{strategy.name}</span>
            </div>
            <div className="metric-row">
              <span>Breakout Ready</span>
              <span style={{ fontWeight: 600, color: strategy.breakoutReady ? 'var(--success)' : 'var(--text-muted)' }}>
                {strategy.breakoutReady ? 'YES' : 'NO'}
              </span>
            </div>
            <div className="metric-row">
              <span>Order Flow Signal</span>
              <span className={strategy.orderFlowSignal > 0 ? 'value-green' : (strategy.orderFlowSignal < 0 ? 'value-red' : '')}>
                {strategy.orderFlowSignal.toFixed(2)}
              </span>
            </div>
          </div>

          {/* Execution Payload Card */}
          <div className={`card ${actionClass}`}>
            <div className="card-title">🚀 Execution Payload</div>
            <div className={`card-value ${actionColor}`} style={{ marginBottom: '1rem' }}>
              {execution.action}
            </div>
            <div className="metric-row">
              <span>Position Size</span>
              <span style={{ fontWeight: 600 }}>{(execution.positionSize * 100).toFixed(2)}%</span>
            </div>
            <div className="metric-row">
              <span>Confidence Score</span>
              <span>{(execution.confidence * 100).toFixed(1)}%</span>
            </div>
            <div style={{ marginTop: '1rem', fontSize: '0.875rem', color: 'var(--text-muted)', fontStyle: 'italic' }}>
              "{execution.logDetails}"
            </div>
          </div>
        </div>
      </div>
    </>
  )
}

export default App
