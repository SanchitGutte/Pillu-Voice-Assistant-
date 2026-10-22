
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(title="Hey Pillu AI Server")

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

class ChatRequest(BaseModel):
    messages: list[dict]
    model: str = "gpt-4o-mini"
    temperature: float = 0.7

@app.get("/")
async def home():
    return {"status": "Hey Pillu server ready"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/api/chat")
async def chat(request: ChatRequest):
    if not os.environ.get("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=500,
            detail="API key is not configured"
        )

    try:
        response = client.chat.completions.create(
            model=request.model,
            messages=request.messages,
            temperature=request.temperature
        )
        return {"reply": response.choices[0].message.content}
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="AI request failed"
        )
      
