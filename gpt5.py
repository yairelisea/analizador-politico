import os, json
from openai import OpenAI

USE_MOCK = os.getenv("GPT5_MOCK","1") == "1"  # por defecto mock ON
_client = None

def client():
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _client

def analyze_snippet(politician_name: str, url: str, platform: str, title: str|None, desc: str|None) -> dict:
    """Devuelve dict con: summary, sentiment, stance, topic, entities."""
    base = (desc or title or "")[:1000]
    if USE_MOCK:
        # Heurística tontita para demo
        txt = base or "Sin texto visible."
        sentiment = "neutral"
        if any(w in txt.lower() for w in ["logro","apoya","aprob","felicita","bien"]): sentiment="positive"
        if any(w in txt.lower() for w in ["critica","corrup","ataque","denuncia","mal"]): sentiment="negative"
        return {
            "summary": txt[:220],
            "sentiment": sentiment,
            "stance": "none",
            "topic": "campaña",
            "entities": [politician_name],
        }

    sys = (
        "Eres un analista de comunicación política. Devuelve SOLO JSON válido con claves: "
        "summary, sentiment (positive|neutral|negative), stance (attack|defense|endorsement|none), "
        "topic (string), entities (lista de strings). Sé breve y específico."
    )
    up = f"""
URL: {url}
Plataforma: {platform}
Título: {title}
Descripción/Texto visible: {desc}

Personaje: {politician_name}

Tarea:
1) resume en 2-3 líneas (neutral),
2) sentimiento y postura hacia el personaje,
3) tema principal,
4) 3-5 entidades.
Devuelve SOLO JSON.
"""
    r = client().chat.completions.create(
        model="gpt-5",
        messages=[{"role":"system","content":sys},{"role":"user","content":up}],
        temperature=0.2, max_tokens=400
    )
    return json.loads(r.choices[0].message.content)
