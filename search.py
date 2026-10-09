from duckduckgo_search import DDGS
from config import MAX_SEARCH_RESULTS


def search_web(claim: str, max_results: int = MAX_SEARCH_RESULTS):
    """Search the web for evidence related to a claim."""
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(claim, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", ""),
                })
    except Exception as e:
        print(f"[search] error: {e}")
    return results


if __name__ == "__main__":
    hits = search_web("Petrol price reduced in Pakistan 2024")
    for h in hits:
        print(h["title"], "—", h["url"])
