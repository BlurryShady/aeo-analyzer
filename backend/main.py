from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .recommendations import generate_recommendations

app = FastAPI(title="AEO Analyzer", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    url: str


@app.get("/")
def root():
    return {"status": "AEO Analyzer is running"}


@app.post("/api/analyze")
async def endpoint(request: AnalyzeRequest):
    return await generate_recommendations(request.url)
