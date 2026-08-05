from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from .recommendations import generate_recommendations



limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="AEO Analyzer", version="1.0.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://analyzer.blurryshady.dev",
        ],
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
)


class AnalyzeRequest(BaseModel):
    url: str


@app.get("/")
def root():
    return {"status": "AEO Analyzer is running"}


@app.post("/api/analyze")
@limiter.limit("5/minute")
async def endpoint(request: Request, body: AnalyzeRequest):
    try:
        result = await generate_recommendations(body.url)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Analysis failed. Please try again.")