from search import search_web
from judge import judge_claim


def verify(claim: str) -> dict:
    """Verity entry point: claim → web search → LLM verdict → structured result."""
    evidence = search_web(claim)
    result = judge_claim(claim, evidence)

    return {
        "claim": claim,
        "verdict": result.get("verdict", "UNVERIFIABLE"),
        "confidence": float(result.get("confidence", 0.0)),
        "reasoning": result.get("reasoning", ""),
        "sources_used": result.get("sources_used", []),
        "all_sources": [{"title": e["title"], "url": e["url"]} for e in evidence],
        "evidence_count": len(evidence),
    }
