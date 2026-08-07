# AEO Analyzer

A free AI-readiness analyzer that reveals how AI agents see your website.

🔗 **Live:** [analyzer.blurryshady.dev](https://analyzer.blurryshady.dev)



## What It Does

AEO Analyzer fetches any URL and evaluates it across four dimensions, returning prioritized recommendations for improving AI agent readiness.

- **Robots Access** — Checks robots.txt and classifies access status for 11 major AI crawlers (GPTBot, ClaudeBot, PerplexityBot, and more)
- **LLMs.txt Quality** — Evaluates llms.txt structure across headers, links and content length
- **Token Usage** — Estimates token consumption via OpenAI's tiktoken with range estimates for other agents
- **Content Structure** — Detects schema markup and heading hierarchy



## Tech Stack

**Backend:** Python, FastAPI, BeautifulSoup, tiktoken, slowapi  
**Frontend:** React, Vite, CSS  
**Deployed:** Render (backend), Cloudflare Pages (frontend)



## Information For Local Run

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn backend.main:app --reload
```



### Frontend
```bash
cd frontend
npm install
npm run dev
```



### Environment Variables

Backend: no environment variables required for V1.

Frontend — create `frontend/.env`:

VITE_API_URL=http://localhost:8000



## Project Structure
```
aeo-analyzer/
├── backend/
│   ├── main.py
│   ├── fetcher.py
│   ├── recommendations.py
│   └── analyzers/
│       ├── robots_checker.py
│       ├── llms_checker.py
│       ├── token_analyzer.py
│       └── content_analyzer.py
└── frontend/
    └── src/
        ├── App.jsx
        └── components/
            ├── AnalysisTab.jsx
            ├── RecommendationsTab.jsx
            ├── MusicPlayer.jsx
            └── SideRays.jsx
```


Note: Cloud's API call created for backend but no API is connected since it's a credential. Claude's token analyze requires an API key.



## License

MIT