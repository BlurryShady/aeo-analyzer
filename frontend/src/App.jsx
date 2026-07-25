import { useState } from 'react'
import SideRays from './components/SideRays'
import './App.css'



function App() {
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)

  const analyzeUrl = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      })
      const data = await response.json()
      setResults(data)
    } catch (error) {
      console.error('Analysis failed:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
      <div className="app">
      <div className="hero">
      <SideRays
        rayColor1="#6366f1"
        rayColor2="#818cf8"
        origin="top-right"
      />
      <div className="hero-content">
        <h1>
          Welcome To AEO Analyzer
        </h1>
        <p>
          An app to analyze your site in aspect of AI agent capacities.
        </p>
        <input
          value={url}
          onChange={e => setUrl(e.target.value)}
          placeholder="https://example.com"
        />
        <button
          onClick={analyzeUrl}
          disabled={loading}
        >
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
        
      </div>
    </div>
    {results && <pre>{JSON.stringify(results, null, 2)}</pre>}
    </div>
  )
}

export default App