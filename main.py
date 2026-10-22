
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(title="Hey Pillu AI Server")

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

class ChatRequest(BaseModel):
    messages: list[dict]
    model: str = "openai/gpt-oss-20b"
    temperature: float = 0.7

@app.get("/")
async def home():
    return {"status": "Hey Pillu server ready"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/api/chat")
async def chat(request: ChatRequest):
    if not os.environ.get("GROQ_API_KEY"):
        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY is not configured"
        )

    try:
        response = client.chat.completions.create(
            model=request.model,
            messages=request.messages,
            temperature=request.temperature
        )
        return {"reply": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
        
