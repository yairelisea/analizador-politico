import requests, re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def detect_platform(u: str) -> str:
    h = urlparse(u).netloc.lower()
    if "tiktok.com" in h: return "tiktok"
    if "instagram.com" in h: return "instagram"
    if "facebook.com" in h or "fb.watch" in h: return "facebook"
    if "x.com" in h or "twitter.com" in h: return "x"
    return "web" if h else "unknown"

def fetch_og(u: str) -> dict:
    r = requests.get(u, headers={"User-Agent":"Mozilla/5.0"}, timeout=20)
    r.raise_for_status()
    s = BeautifulSoup(r.text, "html.parser")
    def og(p):
        t = s.find("meta", property=p)
        return t.get("content") if t and t.get("content") else None
    title = og("og:title") or (s.title.string if s.title else None)
    desc = og("og:description")
    image = og("og:image")
    pub  = og("article:published_time") or og("og:updated_time")
    author = s.find("meta", attrs={"name":"author"})
    author_name = author.get("content") if author and author.get("content") else None
    return dict(title=title, description=desc, image=image, published_at=pub, author_name=author_name)
