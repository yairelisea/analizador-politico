import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import AnalyzeRequest, AnalyzeResponse, PostMeta, PostAI, PostResult
from og import fetch_og, detect_platform
from gpt5 import analyze_snippet

app = FastAPI(title="Percepción Digital (simple JSON)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

@app.get("/health")
def health(): return {"ok": True}

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(req: AnalyzeRequest):
    if len(req.urls) < 35:
        raise HTTPException(400, detail=f"Se requieren ≥35 URLs; recibidas: {len(req.urls)}")

    async def process(u: str):
        # OG (bloqueante) -> correr en thread pool
        import functools
        og = await asyncio.to_thread(fetch_og, u)
        plat = detect_platform(u)
        ai_dict = await asyncio.to_thread(
            analyze_snippet,
            req.politician.name, u, plat, og.get("title"), og.get("description")
        )
        meta = PostMeta(
            url=u, platform=plat, title=og.get("title"), description=og.get("description"),
            published_at=og.get("published_at"), author_name=og.get("author_name"),
            thumbnail_url=og.get("image")
        )
        ai = PostAI(**ai_dict)
        return PostResult(meta=meta, ai=ai)

    tasks = [process(str(u)) for u in req.urls[:max(35, len(req.urls))]]
    results = await asyncio.gather(*tasks)
    return AnalyzeResponse(politician=req.politician, results=results)
