from pydantic import BaseModel, HttpUrl, Field
from typing import List, Literal, Optional

class Politician(BaseModel):
    name: str
    office: Optional[str] = None

class AnalyzeRequest(BaseModel):
    politician: Politician
    urls: List[HttpUrl] = Field(..., min_items=35)

class PostMeta(BaseModel):
    url: HttpUrl
    platform: Literal["tiktok","instagram","facebook","x","web","unknown"] = "unknown"
    title: Optional[str] = None
    description: Optional[str] = None
    published_at: Optional[str] = None
    author_name: Optional[str] = None
    thumbnail_url: Optional[str] = None

class PostAI(BaseModel):
    summary: str
    sentiment: Literal["positive","neutral","negative"]
    stance: Literal["attack","defense","endorsement","none"]
    topic: str
    entities: List[str] = []

class PostResult(BaseModel):
    meta: PostMeta
    ai: PostAI

class AnalyzeResponse(BaseModel):
    politician: Politician
    results: List[PostResult]
 
