import json
from openai import OpenAI
from config import NVIDIA_API_KEY, NVIDIA_BASE_URL, NVIDIA_MODEL, MAX_EVIDENCE_CHARS

client = OpenAI(api_key=NVIDIA_API_KEY, base_url=NVIDIA_BASE_URL)

SYSTEM_PROMPT = """You are an evidence-based fact-checking assistant.
Given a claim and web search results, decide whether the claim is REAL, FAKE, or UNVERIFIABLE.

Rules:
1. Use only the evidence provided. Do not use outside knowledge.
2. If evidence supports the claim, return REAL.
3. If evidence refutes the claim, return FAKE.
4. If evidence is insufficient or conflicting, return UNVERIFIABLE.
5. Cite the source URLs you relied on.
6. Return strict JSON only — no markdown fences, no explanation outside the JSON.

Format:
{
  "verdict": "REAL" | "FAKE" | "UNVERIFIABLE",
  "confidence": 0.0 to 1.0,
  "reasoning": "one short paragraph",
  "sources_used": ["url1", "url2"]
}"""


def judge_claim(claim: str, evidence: list) -> dict:
    if not evidence:
        return {
            "verdict": "UNVERIFIABLE",
            "confidence": 0.0,
            "reasoning": "No evidence was retrieved from the web.",
            "sources_used": [],
        }

    evidence_text = ""
    for i, e in enumerate(evidence, 1):
        evidence_text += f"\n[{i}] {e['title']}\nURL: {e['url']}\nSnippet: {e['snippet']}\n"
    evidence_text = evidence_text[:MAX_EVIDENCE_CHARS]

    user_prompt = f"Claim: {claim}\n\nEvidence:\n{evidence_text}\n\nReturn JSON only."

    try:
        response = client.chat.completions.create(
            model=NVIDIA_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.1,
            max_tokens=500,
        )
        text = response.choices[0].message.content.strip()

        # Strip markdown fences if present
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text.strip())
    except Exception as e:
        return {
            "verdict": "UNVERIFIABLE",
            "confidence": 0.0,
            "reasoning": f"Judge error: {e}",
            "sources_used": [],
        }
