import './AnalysisTab.css'



function AnalysisTab({ raw }) {
  const { robots, llms, tokens, content } = raw

  return (
    <div className="analysis-tab">
      <section className="panel">
        <h2>AI Robots Access</h2>
        {Object.entries(robots).map(([agent, status]) => (
          <div key={agent} className={`agent-row status-${status}`}>
            <span>{agent}</span>
            <span>{status}</span>
          </div>
        ))}
      </section>

      <section className="panel">
        <h2>LLMs.txt Quality</h2>
        <div className={`agent-row status-${llms.header_status}`}>
          <span>Headers</span>
          <span>{llms.header_message}</span>
        </div>
        <div className={`agent-row status-${llms.link_status}`}>
          <span>Links</span>
          <span>{llms.link_message}</span>
        </div>
        <div className={`agent-row status-${llms.length_status}`}>
          <span>Length</span>
          <span>{llms.length_message}</span>
        </div>
      </section>

    <section className="panel">
      <h2>Token Usage</h2>
      <div className="agent-row">
        <span>OpenAI Token Count</span>
        <span>{tokens.openai_token_count}</span>
      </div>
      <div className="agent-row">
        <span>Claude Token Count</span>
        <span>{tokens.claude_token_count ?? 'unavailable'}</span>
      </div>
      <div className="agent-row">
        <span>Estimated Range (Other Agents)</span>
        <span>{tokens.minimum_usage} - {tokens.maximum_usage}</span>
      </div>
      <div className="agent-row">
        <span>Word Count</span>
        <span>{tokens.word_count}</span>
      </div>
      <div className="agent-row">
        <span>JS Dependent</span>
        <span>{tokens.js_dependent ? 'Yes' : 'No'}</span>
      </div>
      {tokens.disclaimer && (
        <div className="agent-row">
          <span>Warning</span>
          <span>{tokens.disclaimer}</span>
        </div>
      )}
    </section>
      
    <section className="panel">
      <h2>Content Analysis</h2>
      <div className="agent-row">
        <span>H1 Count</span>
        <span>{content.h1_count}</span>
      </div>
      <div className="agent-row">
        <span>H2 Count</span>
        <span>{content.h2_count}</span>
      </div>
      <div className="agent-row">
        <span>H3 Count</span>
        <span>{content.h3_count}</span>
      </div>
      <div className="agent-row">
        <span>Schema Markup</span>
        <span>{content.schema_found ? '✓ Found' : '✗ Not found'}</span>
      </div>
      {content.schema_message && (
        <div className="agent-row">
          <span>Schema Note</span>
          <span>{content.schema_message}</span>
        </div>
      )}
      {content.headings.length > 0 && (
        <div className="headings-list">
          <p>Headings Found:</p>
          {content.headings.map((h, i) => (
            <div key={i} className="agent-row">
              <span>{h.level.toUpperCase()}</span>
              <span>{h.text}</span>
            </div>
          ))}
        </div>
      )}
    </section>
    </div>
  )
}



export default AnalysisTab