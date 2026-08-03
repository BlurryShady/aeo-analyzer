import { useState, useRef } from 'react'
import SideRays from './components/SideRays'
import './App.css'
import AnalysisTab from './components/AnalysisTab'
import RecommendationsTab from './components/RecommendationsTab'
import MusicPlayer from './components/MusicPlayer'



function App() {
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [activeTab, setActiveTab] = useState('analysis')
  const resultsRef = useRef(null)

  const analyzeUrl = async () => {
    const normalizedUrl = url.startsWith('http') ? url : `https://${url}`
    setLoading(true)
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: normalizedUrl })
      })
      const data = await response.json()
      setResults(data)
          setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }, 100)
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
    {results && (
      <div className="results-section" ref={resultsRef}>
        <div className="tab-buttons">
          <button 
            className={activeTab === 'analysis' ? 'tab-active' : ''}
            onClick={() => setActiveTab('analysis')}
          >
            Analysis
          </button>
          <button
            className={activeTab === 'recommendations' ? 'tab-active' : ''}
            onClick={() => setActiveTab('recommendations')}
          >
            Recommendations
          </button>
        </div>

        {activeTab === 'analysis' && <AnalysisTab raw={results.raw} />}
        {activeTab === 'recommendations' && <RecommendationsTab recommendations={results.recommendations} />}
      </div>
    
    )}
    <MusicPlayer />
    </div>
  )
}

export default App