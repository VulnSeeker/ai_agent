from fastapi import FastAPI
from pydantic import BaseModel
from verity import verify

app = FastAPI(title="Verity", version="0.1.0")


class ClaimRequest(BaseModel):
    claim: str


@app.post("/verify")
def verify_claim(req: ClaimRequest):
    return verify(req.claim)


@app.get("/health")
def health():
    return {"status": "ok", "service": "verity"}
