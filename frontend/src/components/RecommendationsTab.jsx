import './RecommendationsTab.css'

function RecommendationsTab({ recommendations }) {

return (
  <div className="recommendations-tab">
      {recommendations.map((rec, i) => (
        <div key={i} className={`rec-card priority-${rec.priority}`}>
          <span className="mono">{rec.priority.toUpperCase()} PRIORITY</span>
          <span className="mono">{rec.category}</span>
          <p>{rec.issue}</p>
          <p>{rec.fix}</p>
        </div>
      ))}
    </div>
  )
}
export default RecommendationsTab